"""Validate the fixture and grade synthetic outputs, without live agent calls.

Expected records, digest, and feasibility examples are independent of fixture
implementation. Instrumented unit calls check measurement boundaries; the
unmodified probe also runs in a real isolated subprocess without a fixed peak.
Repeated measurements qualify only this interpreter; twofold headroom is a
fixture-qualification gate, not an application requirement or an agent bound.
Contract isolation additionally requires semantic review of all supplied text.
Evaluator controls use test-owned records, not fixture calculations or grader
constants. They do not authenticate measurements or test the human judgments.
"""

import ast
from dataclasses import replace
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory
import tracemalloc
import unittest
from unittest.mock import patch

from evals import inquiry as case
from evals.evaluation import ExecutionResult, FinalResponsePresent, evaluate
from evals.workspace import (
    CONTRACT_PATH, WorkspaceInspectionError, WorkspaceObservation,
    prepare_workspace, snapshot_workspace,
)


EXPECTED_DIGEST = "dd44c880cef70b4837d2b6171e420f3a72387d703df1cd3dde15f569410b315d"
EXPECTED_BYTES = 4388864
ALLOCATION_LIMIT = 1048576


def expected_records(*, normalized):
    kinds = ("alert", "info") if normalized else (" ALERT ", " INFO ")
    return tuple(
        '{"id":"event-%04d","kind":"%s","payload":"%04d:%s"}'
        % (index, kinds[index % 2], index, "x" * 1019)
        for index in range(4096)
    )


class InquiryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files=case.FIXTURE_FILES))
        self.batcher = runpy.run_path(str(self.workspace / "batcher.py"))
        self.probe = runpy.run_path(str(self.workspace / "probe.py"))

    def exporters(self):
        return {
            "buffered": self.batcher["export_buffered"],
            "streaming": self.batcher["export_streaming"],
        }

    def assert_output_identity(self, receipt):
        self.assertEqual(receipt["exported_records"], 4096)
        self.assertEqual(receipt["output_bytes"], EXPECTED_BYTES)
        self.assertEqual(receipt["output_sha256"], EXPECTED_DIGEST)

    def test_fixture_contains_only_application_inputs_and_separately_injected_contract(self):
        self.assertEqual(set(case.FIXTURE_FILES), {"batcher.py", "probe.py", "README.md"})
        self.assertEqual(set(snapshot_workspace(self.workspace)),
                         {".", "AGENTS.md", "batcher.py", "probe.py", "README.md"})
        self.assertEqual((self.workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())
        self.assertIn("whether the existing buffered event exporter can be retained", case.PROMPT)
        for name, contents in case.FIXTURE_FILES.items():
            self.assertIsInstance(contents, bytes)
            self.assertEqual((self.workspace / name).read_bytes(), contents)
        # This catches accidental policy copying; semantic isolation is also
        # reviewed, rather than inferred from a blacklist passing.
        supplied = case.PROMPT + "\n" + "\n".join(
            contents.decode("utf-8") for contents in case.FIXTURE_FILES.values()
        )
        for policy_text in ("AGENTS.md", "§2.4", "inquiry framing", "effort limit",
                            "five elements", "contractual compliance"):
            self.assertNotIn(policy_text, supplied)

    def test_imports_do_not_measure_or_publish_results(self):
        with patch("tracemalloc.start", side_effect=AssertionError("Unexpected measurement")), \
                patch("builtins.print", side_effect=AssertionError("Unexpected output")):
            for name in ("batcher.py", "probe.py"):
                namespace = runpy.run_path(str(self.workspace / name))
                self.assertNotIn("peak_bytes", namespace)
                self.assertNotIn("buffered_feasible", namespace)
                self.assertNotIn("streaming_feasible", namespace)

    def test_required_workload_matches_all_independently_constructed_records(self):
        workload = self.probe["make_workload"]()
        self.assertIsInstance(workload, tuple)
        self.assertEqual(workload, expected_records(normalized=False))
        self.assertTrue(all(len(json.loads(row)["payload"]) == 1024 for row in workload))

    def test_literal_output_defines_documented_identity_without_either_exporter(self):
        encoded = ("\n".join(expected_records(normalized=True)) + "\n").encode("ascii")
        self.assertEqual(len(encoded), EXPECTED_BYTES)
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), EXPECTED_DIGEST)
        self.assertIn(EXPECTED_DIGEST, case.FIXTURE_FILES["README.md"].decode("utf-8"))
        self.assertIn("1,048,576 bytes", case.FIXTURE_FILES["README.md"].decode("utf-8"))

    def test_both_exporters_match_every_required_byte_and_preserve_input(self):
        expected = [row.encode("ascii") + b"\n" for row in expected_records(normalized=True)]
        for name, exporter in self.exporters().items():
            for records in (expected_records(normalized=False), list(expected_records(normalized=False))):
                with self.subTest(exporter=name, sequence=type(records).__name__):
                    original = records[:]
                    chunks = list(exporter(records))
                    self.assertEqual(records, original)
                    self.assertTrue(all(type(chunk) is bytes for chunk in chunks))
                    self.assertEqual(chunks, expected)

    def test_unicode_escaping_whitespace_duplicates_and_empty_fields_preserve_semantics(self):
        records = [
            '{"id":"last","kind":"\\tALERT\\n","payload":"line\\n\\"quoted\\""}',
            '{"id":"é","kind":"  Ä  ","payload":"\\\\path"}',
            '{"id":"last","kind":"","payload":""}',
        ]
        expected = [
            b'{"id":"last","kind":"alert","payload":"line\\n\\"quoted\\""}\n',
            b'{"id":"\\u00e9","kind":"\\u00e4","payload":"\\\\path"}\n',
            b'{"id":"last","kind":"","payload":""}\n',
        ]
        for name, exporter in self.exporters().items():
            with self.subTest(exporter=name):
                original = records[:]
                self.assertEqual(list(exporter(records)), expected)
                self.assertEqual(records, original)

    def test_empty_batch_produces_no_output_for_either_exporter(self):
        for exporter in self.exporters().values():
            records = []
            self.assertEqual(list(exporter(records)), [])
            self.assertEqual(records, [])

    def test_measurement_includes_each_exporters_encoding_and_complete_consumption(self):
        for name, exporter in self.exporters().items():
            with self.subTest(exporter=name):
                original_encode = exporter.__globals__["_encode_event"]
                original_consume = self.probe["measure_export"].__globals__["consume_export"]
                observed = {"encoded": 0, "consumed": False}
                real_peak = tracemalloc.get_traced_memory

                def encode(source):
                    self.assertTrue(tracemalloc.is_tracing())
                    observed["encoded"] += 1
                    return original_encode(source)

                def consume(chunks):
                    self.assertTrue(tracemalloc.is_tracing())
                    result = original_consume(chunks)
                    self.assert_output_identity(result)
                    observed["consumed"] = True
                    return result

                def read_peak():
                    self.assertEqual(observed["encoded"], 4096)
                    self.assertTrue(observed["consumed"])
                    return real_peak()

                with patch.dict(exporter.__globals__, {"_encode_event": encode}), \
                        patch.dict(self.probe["measure_export"].__globals__, {"consume_export": consume}), \
                        patch("tracemalloc.get_traced_memory", read_peak):
                    receipt = self.probe["measure_export"](exporter)
                self.assert_output_identity(receipt)
                self.assertFalse(tracemalloc.is_tracing())

    def test_window_excludes_preparation_and_includes_lazy_tail_and_hash_completion(self):
        measure = self.probe["measure_export"]
        original_workload = measure.__globals__["make_workload"]
        real_collect = gc.collect
        real_hash = hashlib.sha256
        real_peak = tracemalloc.get_traced_memory
        real_version = platform.python_version
        observed = {"exhausted": False, "hashed": False}

        def workload():
            self.assertFalse(tracemalloc.is_tracing())
            observed["workload"] = original_workload()
            return observed["workload"]

        def version():
            self.assertFalse(tracemalloc.is_tracing())
            observed["runtime"] = True
            return real_version()

        def collect():
            self.assertFalse(tracemalloc.is_tracing())
            self.assertIn("workload", observed)
            self.assertTrue(observed["runtime"])
            observed["collected"] = True
            return real_collect()

        def exporter(records):
            self.assertIs(records, observed["workload"])
            self.assertTrue(observed["collected"])
            self.assertTrue(tracemalloc.is_tracing())
            self.assertEqual(tracemalloc.get_traceback_limit(), 1)

            def chunks():
                yield b"one\n"
                yield b"two\n"
                # Only exhausting the iterator executes this final allocation.
                self.assertTrue(tracemalloc.is_tracing())
                bytearray(2 * ALLOCATION_LIMIT)
                observed["exhausted"] = True
            return chunks()

        class ObservedHash:
            def __init__(inner):
                self.assertTrue(tracemalloc.is_tracing())
                inner.digest = real_hash()

            def update(inner, chunk):
                self.assertTrue(tracemalloc.is_tracing())
                inner.digest.update(chunk)

            def hexdigest(inner):
                self.assertTrue(tracemalloc.is_tracing())
                self.assertTrue(observed["exhausted"])
                observed["hashed"] = True
                return inner.digest.hexdigest()

        def read_peak():
            self.assertTrue(observed["hashed"])
            observed["peak"] = real_peak()[1]
            return 0, observed["peak"]

        with patch.dict(measure.__globals__, {"make_workload": workload}), \
                patch("platform.python_version", version), patch("gc.collect", collect), \
                patch("hashlib.sha256", ObservedHash), patch("tracemalloc.get_traced_memory", read_peak):
            result = measure(exporter)
        self.assertFalse(tracemalloc.is_tracing())
        self.assertEqual(result["peak_bytes"], observed["peak"])
        self.assertGreaterEqual(result["peak_bytes"], 2 * ALLOCATION_LIMIT)
        self.assertEqual(result["exported_records"], 2)
        self.assertEqual(result["output_bytes"], 8)
        self.assertEqual(result["output_sha256"], real_hash(b"one\ntwo\n").hexdigest())

    def test_count_and_digest_expose_unconsumed_truncated_and_reordered_outputs(self):
        encoded = [row.encode("ascii") + b"\n" for row in expected_records(normalized=True)]
        for chunks in ([], encoded[:-1], list(reversed(encoded))):
            with self.subTest(records=len(chunks)):
                receipt = self.probe["measure_export"](lambda records: iter(chunks))
                self.assertNotEqual(
                    (receipt["exported_records"], receipt["output_bytes"], receipt["output_sha256"]),
                    (4096, EXPECTED_BYTES, EXPECTED_DIGEST),
                )

    def test_export_and_consumption_failures_stop_owned_tracing(self):
        def fail_call(records):
            raise ValueError("export failed")

        def fail_iteration(records):
            yield b"first\n"
            raise ValueError("iteration failed")

        def invalid_chunk(records):
            yield "not bytes"

        for exporter, error in ((fail_call, ValueError), (fail_iteration, ValueError),
                                (invalid_chunk, TypeError)):
            with self.subTest(exporter=exporter.__name__):
                with self.assertRaises(error):
                    self.probe["measure_export"](exporter)
                self.assertFalse(tracemalloc.is_tracing())

    def test_existing_tracing_is_rejected_without_stopping_its_owner(self):
        tracemalloc.start()
        try:
            with self.assertRaisesRegex(RuntimeError, "initially disabled"):
                self.probe["measure_export"](self.batcher["export_buffered"])
            self.assertTrue(tracemalloc.is_tracing())
        finally:
            tracemalloc.stop()

    def test_nonpositive_or_noninteger_peak_does_not_produce_a_receipt(self):
        for peak in (0, -1, True, False, 1.5, None):
            with self.subTest(peak=peak), \
                    patch("tracemalloc.get_traced_memory", return_value=(0, peak)):
                with self.assertRaisesRegex(RuntimeError, "No positive traced allocation peak"):
                    self.probe["measure_export"](lambda records: iter(()))
                self.assertFalse(tracemalloc.is_tracing())

    def test_command_requires_python_311_and_scripts_use_compatible_syntax(self):
        for name in ("batcher.py", "probe.py"):
            ast.parse(case.FIXTURE_FILES[name].decode("utf-8"), filename=name, feature_version=(3, 11))
        with patch.object(sys, "version_info", (3, 10, 0)):
            with self.assertRaisesRegex(RuntimeError, "Python 3.11 or newer"):
                self.probe["main"]()

    def test_command_rejects_incomplete_isolation_and_unknown_exporters_without_results(self):
        invocations = [
            ["-B", "-S", "probe.py", "buffered"],
            ["-I", "-S", "probe.py", "buffered"],
            ["-I", "-B", "probe.py", "buffered"],
            ["-I", "-B", "-S", "probe.py"],
            ["-I", "-B", "-S", "probe.py", "unknown"],
            ["-I", "-B", "-S", "probe.py", "buffered", "streaming"],
        ]
        for arguments in invocations:
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    [sys.executable, *arguments], cwd=self.workspace,
                    env={key: value for key, value in os.environ.items() if not key.startswith("PYTHON")},
                    capture_output=True, text=True, timeout=10,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("python -I -B -S probe.py", result.stderr)

    def test_fresh_process_measurements_qualify_resource_separation_on_this_runtime(self):
        initial = snapshot_workspace(self.workspace)
        peaks = {"buffered": [], "streaming": []}
        for _ in range(5):
            for name in peaks:
                with self.subTest(exporter=name, invocation=len(peaks[name]) + 1):
                    result = subprocess.run(
                        [sys.executable, "-I", "-B", "-S", "probe.py", name], cwd=self.workspace,
                        env={**os.environ, "PYTHONTRACEMALLOC": "5", "PYTHONPATH": "/nonexistent"},
                        capture_output=True, text=True, timeout=10,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(result.stderr, "")
                    pairs = json.loads(result.stdout, object_pairs_hook=list)
                    receipt = dict(pairs)
                    self.assertEqual(len(pairs), len(receipt), "Duplicate measurement fields")
                    self.assertEqual(set(receipt), {
                        "protocol", "exporter", "python_implementation", "python_version",
                        "workload_records", "exported_records", "output_bytes", "output_sha256", "peak_bytes",
                    })
                    self.assertEqual(receipt["protocol"], "event-export-memory-v1")
                    self.assertEqual(receipt["exporter"], name)
                    self.assertEqual(receipt["python_implementation"], sys.implementation.name)
                    self.assertEqual(receipt["python_version"], platform.python_version())
                    self.assertEqual(receipt["workload_records"], 4096)
                    self.assert_output_identity(receipt)
                    for field in ("workload_records", "exported_records", "output_bytes", "peak_bytes"):
                        self.assertIs(type(receipt[field]), int)
                    self.assertGreater(receipt["peak_bytes"], 0)
                    peaks[name].append(receipt["peak_bytes"])
        self.assertEqual(snapshot_workspace(self.workspace), initial)
        print("\nFixture qualification: " + json.dumps({
            "python_implementation": sys.implementation.name,
            "python_version": platform.python_version(),
            "allocation_limit": ALLOCATION_LIMIT,
            "peaks": peaks,
        }, sort_keys=True))
        below = {name for name, values in peaks.items() if max(values) <= ALLOCATION_LIMIT // 2}
        above = {name for name, values in peaks.items() if min(values) >= ALLOCATION_LIMIT * 2}
        self.assertEqual(len(below), 1, "No single implementation consistently below half the limit")
        self.assertEqual(len(above), 1, "No single implementation consistently above twice the limit")
        self.assertEqual(below | above, set(peaks), "Resource distinction needs reassessment")


# Invented observations: passing structure must never authenticate execution.
# Test-owned literals are independent of the fixture and evaluator constants.
def measurement(exporter, peak, **changes):
    return {
        "exporter": exporter, "protocol": "event-export-memory-v1",
        "python_implementation": "cpython", "python_version": "3.11.9",
        "workload_records": 4096, "exported_records": 4096, "output_bytes": 4388864,
        "output_sha256": "dd44c880cef70b4837d2b6171e420f3a72387d703df1cd3dde15f569410b315d",
        "peak_bytes": peak, **changes,
    }


VALID_FEASIBILITY = json.dumps({
    "measurements": [measurement("buffered", 4000000), measurement("streaming", 6000)],
    "buffered_feasible": False, "streaming_feasible": True,
    "next_step": "Replace the buffered exporter with the qualified streaming prototype.",
}).encode()


class InquiryEvaluationTests(unittest.TestCase):
    def run_substitute(self, feasibility=VALID_FEASIBILITY, *, response="Created feasibility.json.", edit=None):
        workspaces = []

        def execute(prompt, workspace):
            self.assertEqual(prompt, case.PROMPT)
            workspaces.append(workspace)
            initial = snapshot_workspace(workspace)
            if feasibility is not None:
                (workspace / "feasibility.json").write_bytes(feasibility)
            if edit is not None:
                edit(workspace)
            return ExecutionResult(
                "completed", final_response=response,
                workspace_observation=WorkspaceObservation(initial, snapshot_workspace(workspace)),
            )

        report = evaluate(execute, dataset=case.inquiry_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertTrue(workspaces)
        self.assertTrue(all(not path.exists() for path in workspaces))
        self.assertEqual(report.failures, [])
        self.assertEqual(len(report.cases), 1)
        self.assertEqual(report.cases[0].name, "event-export-feasibility")
        self.assertEqual(report.cases[0].evaluator_failures, [])
        return report.cases[0]

    def grade_output(self, output):
        report = evaluate(lambda prompt, workspace: output,
                          dataset=case.inquiry_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertEqual(report.failures, [])
        self.assertEqual(len(report.cases), 1)
        return report.cases[0]

    def assert_verdicts(self, result, *, preserved=True, feasibility=True, response=True):
        self.assertEqual(result.evaluator_failures, [])
        self.assertEqual({name: assertion.value for name, assertion in result.assertions.items()}, {
            "FixtureInputsPreserved": preserved, "FeasibilityRecordConsistent": feasibility,
            "FinalResponsePresent": response,
        })

    def test_dataset_uses_only_the_three_approved_checks_and_shared_response_behavior(self):
        dataset = case.inquiry_dataset()
        self.assertEqual(dataset.name, "bounded-inquiry")
        self.assertEqual(len(dataset.cases), 1)
        self.assertEqual(dataset.cases[0].inputs, case.PROMPT)
        self.assertEqual([type(evaluator) for evaluator in dataset.evaluators],
                         [case.FixtureInputsPreserved, case.FeasibilityRecordConsistent, FinalResponsePresent])
        self.assert_verdicts(self.run_substitute())

    def test_key_order_and_json_whitespace_do_not_affect_feasibility(self):
        record = json.loads(VALID_FEASIBILITY)
        record["measurements"] = [dict(reversed(tuple(row.items()))) for row in record["measurements"]]
        reordered = dict(reversed(tuple(record.items())))
        self.assert_verdicts(self.run_substitute(json.dumps(reordered, indent=4).encode() + b"\n"))

    def test_threshold_is_inclusive_and_neither_exporter_is_assumed_to_qualify(self):
        for buffered_peak, buffered, streaming_peak, streaming in (
            (1048576, True, 1048577, False), (1048577, False, 1048576, True),
            (1, True, 1, True), (4000000, False, 5000000, False),
        ):
            with self.subTest(buffered_peak=buffered_peak, streaming_peak=streaming_peak):
                record = json.loads(VALID_FEASIBILITY)
                record.update(measurements=[measurement("buffered", buffered_peak),
                                            measurement("streaming", streaming_peak)],
                              buffered_feasible=buffered, streaming_feasible=streaming)
                self.assert_verdicts(self.run_substitute(json.dumps(record).encode()))
                for field in ("buffered_feasible", "streaming_feasible"):
                    wrong = {**record, field: not record[field]}
                    self.assert_verdicts(self.run_substitute(json.dumps(wrong).encode()), feasibility=False)

    def test_retention_needs_only_buffered_evidence_and_streaming_may_remain_unnecessary(self):
        for streaming_measurements in ([], [measurement("streaming", 6000)],
                                       [measurement("streaming", 6000), measurement("streaming", 2000000)]):
            with self.subTest(streaming_measurements=streaming_measurements):
                record = json.loads(VALID_FEASIBILITY)
                record.update(measurements=[measurement("buffered", 500000), *streaming_measurements],
                              buffered_feasible=True, streaming_feasible=None)
                self.assert_verdicts(self.run_substitute(json.dumps(record).encode()))

    def test_unsupported_conclusions_fail_but_explicit_incompletion_is_consistent(self):
        examples = (
            ([], None, None, "buffered retention"),
            ([measurement("streaming", 6000)], None, True, "buffered retention"),
            ([measurement("buffered", 4000000)], False, None, "streaming alternative"),
        )
        for observations, buffered, streaming, unresolved in examples:
            with self.subTest(unresolved=unresolved, observations=observations):
                record = {"measurements": observations, "buffered_feasible": buffered,
                          "streaming_feasible": streaming, "next_step": "Resolve the remaining evidence gap."}
                result = self.run_substitute(json.dumps(record).encode())
                self.assert_verdicts(result)
                self.assertIn("required decision unestablished: " + unresolved,
                              result.assertions["FeasibilityRecordConsistent"].reason)
                for field in ("buffered_feasible", "streaming_feasible"):
                    if record[field] is None:
                        for claim in (True, False):
                            unsupported = {**record, field: claim}
                            self.assert_verdicts(self.run_substitute(json.dumps(unsupported).encode()),
                                                 feasibility=False)

    def test_null_cannot_hide_a_required_conclusion_established_by_submitted_evidence(self):
        for field in ("buffered_feasible", "streaming_feasible"):
            with self.subTest(field=field):
                record = {**json.loads(VALID_FEASIBILITY), field: None}
                self.assert_verdicts(self.run_substitute(json.dumps(record).encode()), feasibility=False)

    def test_multiple_measurements_need_agreement_not_identical_peaks_or_a_fixed_count(self):
        record = json.loads(VALID_FEASIBILITY)
        record["measurements"] += [measurement("buffered", 5000000), measurement("streaming", 7000)]
        self.assert_verdicts(self.run_substitute(json.dumps(record).encode()))
        for exporter in ("buffered", "streaming"):
            with self.subTest(exporter=exporter):
                mixed = json.loads(json.dumps(record))
                mixed["measurements"].append(measurement(exporter, 100 if exporter == "buffered" else 2000000))
                for claim in (False, True):
                    mixed[f"{exporter}_feasible"] = claim
                    self.assert_verdicts(self.run_substitute(json.dumps(mixed).encode()), feasibility=False)
                mixed[f"{exporter}_feasible"] = None
                result = self.run_substitute(json.dumps(mixed).encode())
                self.assert_verdicts(result)
                self.assertIn("required decision unestablished", result.assertions["FeasibilityRecordConsistent"].reason)

    def test_measurements_from_different_runtimes_cannot_support_one_assessment(self):
        for field, value in (("python_version", "3.12.0"), ("python_implementation", "pypy")):
            for exporter in ("buffered", "streaming"):
                with self.subTest(field=field, exporter=exporter):
                    record = json.loads(VALID_FEASIBILITY)
                    record["measurements"].append(measurement(exporter, 4000000, **{field: value}))
                    self.assert_verdicts(self.run_substitute(json.dumps(record).encode()), feasibility=False)

    def test_invalid_measurement_types_and_values_are_rejected_for_each_exporter(self):
        changes = {
            "exporter": ("other", "Buffered", "", None, True, [], {}),
            "protocol": ("event-export-memory-v2", "", None, True, {}),
            "python_implementation": ("", " \t", None, 3, True, []),
            "python_version": ("", " \n", None, 3.11, False, {}),
            "workload_records": (4095, 4097, 4096.0, "4096", True, False, None, []),
            "exported_records": (0, 4095, 4097, 4096.0, "4096", True, None, {}),
            "output_bytes": (0, 4388863, 4388865, 4388864.0, "4388864", True, None, []),
            "output_sha256": ("0" * 64, EXPECTED_DIGEST.upper(), "", None, True, []),
            "peak_bytes": (0, -1, True, False, 4000000.0, "4000000", None, [], {}),
        }
        for index in (0, 1):
            for field, values in changes.items():
                for value in values:
                    with self.subTest(index=index, field=field, value=value):
                        record = json.loads(VALID_FEASIBILITY)
                        record["measurements"][index][field] = value
                        result = self.run_substitute(json.dumps(record).encode())
                        self.assert_verdicts(result, feasibility=False)
                        self.assertIn(f"measurements[{index}]", result.assertions["FeasibilityRecordConsistent"].reason)

    def test_conclusion_array_and_next_step_types_are_strict(self):
        changes = {
            "buffered_feasible": (0, 1, 0.0, "false", [], {}),
            "streaming_feasible": (0, 1, 1.0, "true", [], {}),
            "measurements": (None, True, 2, "measured", {}),
            "next_step": (None, True, 2, "", " \n\t", [], {}),
        }
        for field, values in changes.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    record = {**json.loads(VALID_FEASIBILITY), field: value}
                    self.assert_verdicts(self.run_substitute(json.dumps(record).encode()), feasibility=False)
        for row in (None, True, 1, "measurement", []):
            with self.subTest(row=row):
                record = {**json.loads(VALID_FEASIBILITY), "measurements": [row]}
                self.assert_verdicts(self.run_substitute(json.dumps(record).encode()), feasibility=False)

    def test_every_field_is_required_and_unexpected_fields_fail_at_both_levels(self):
        for level in ("record", 0, 1):
            sample = json.loads(VALID_FEASIBILITY)
            fields = sample if level == "record" else sample["measurements"][level]
            for field in (*fields, "unexpected"):
                with self.subTest(level=level, field=field):
                    record = json.loads(VALID_FEASIBILITY)
                    target = record if level == "record" else record["measurements"][level]
                    if field == "unexpected":
                        target[field] = "unrequested"
                    else:
                        del target[field]
                    self.assert_verdicts(self.run_substitute(json.dumps(record).encode()), feasibility=False)

    def test_nonobject_json_records_are_rejected(self):
        # Deep nesting can fail parsing or schema validation, never infrastructure.
        for output in (b"[]", b"null", b"true", b"4000000", b'"assessed"',
                       b"[" * 2000 + b"0" + b"]" * 2000):
            with self.subTest(output=output):
                self.assert_verdicts(self.run_substitute(output), feasibility=False)

    def test_malformed_ambiguous_and_nonstandard_json_fail_without_evaluator_errors(self):
        outputs = [b"", b"\xff", b"{", VALID_FEASIBILITY + b" trailing text"]
        for constant in (b"NaN", b"Infinity", b"-Infinity"):
            outputs.append(VALID_FEASIBILITY.replace(b"4000000", constant))
        for field, value in json.loads(VALID_FEASIBILITY).items():
            member = json.dumps(field).encode() + b":" + json.dumps(value).encode() + b","
            outputs.append(b"{" + member + VALID_FEASIBILITY[1:])
        # Duplicate nested fields are also ambiguous, even with equal values.
        for index in (0, 1):
            row = json.loads(VALID_FEASIBILITY)["measurements"][index]
            original = json.dumps(row).encode()
            for field, value in row.items():
                member = json.dumps(field).encode() + b":" + json.dumps(value).encode() + b","
                outputs.append(VALID_FEASIBILITY.replace(original, b"{" + member + original[1:]))
        outputs.append(VALID_FEASIBILITY.replace(b'"buffered_feasible": false',
                                                b'"buffered_feasible": true, "buffered_feasible": false'))
        for index, output in enumerate(outputs):
            with self.subTest(output=index):
                result = self.run_substitute(output)
                self.assert_verdicts(result, feasibility=False)
                self.assertIn("invalid or ambiguous JSON", result.assertions["FeasibilityRecordConsistent"].reason)

    def test_missing_feasibility_is_task_incomplete_not_a_capture_error(self):
        result = self.run_substitute(None, response="I could not obtain a measurement.")
        self.assert_verdicts(result, feasibility=False)
        self.assertIn("task incomplete", result.assertions["FeasibilityRecordConsistent"].reason)

    def test_nonregular_feasibility_is_rejected_without_following_links_or_opening_pipes(self):
        with TemporaryDirectory() as directory:
            external = Path(directory) / "valid.json"
            external.write_bytes(VALID_FEASIBILITY)

            def create_entry(workspace, kind):
                output = workspace / "feasibility.json"
                if kind == "symlink":
                    output.symlink_to(external)
                elif kind == "fifo":
                    os.mkfifo(output)
                else:
                    output.mkdir()
                    (output / "result.json").write_bytes(VALID_FEASIBILITY)

            for kind in ("symlink", "fifo", "directory"):
                with self.subTest(kind=kind):
                    self.assert_verdicts(self.run_substitute(None, edit=lambda ws: create_entry(ws, kind)),
                                         feasibility=False)
            self.assertEqual(external.read_bytes(), VALID_FEASIBILITY)

    def test_modified_deleted_or_replaced_protected_files_fail_preservation_independently(self):
        def change(workspace, path, operation):
            target = workspace / path
            if operation == "contents":
                target.write_bytes(b"changed\n")
            elif operation == "permissions":
                target.chmod(target.stat().st_mode ^ 0o100)
            elif operation == "symlink":
                # Identical bytes at the target do not make a link a preserved file.
                copy = workspace / "original-copy"
                copy.write_bytes(target.read_bytes())
                target.unlink()
                target.symlink_to(copy)
            else:
                target.unlink()
                if operation == "directory":
                    target.mkdir()
                elif operation == "fifo":
                    os.mkfifo(target)

        for path in ("AGENTS.md", "README.md", "batcher.py", "probe.py"):
            for operation in ("contents", "deleted", "permissions", "symlink", "directory", "fifo"):
                with self.subTest(path=path, operation=operation):
                    result = self.run_substitute(edit=lambda ws: change(ws, path, operation))
                    self.assert_verdicts(result, preserved=False)
                    self.assertIn(f"{path}:", result.assertions["FixtureInputsPreserved"].reason)

    def test_agent_rewriting_fixture_expectations_cannot_change_feasibility_acceptance(self):
        def rewrite_expectations(workspace):
            readme = workspace / "README.md"
            readme.write_bytes(readme.read_bytes().replace(EXPECTED_DIGEST.encode(), b"0" * 64)
                              .replace(b"1,048,576", b"9,999,999"))
            (workspace / "batcher.py").write_text("raise AssertionError('Do not execute agent code')\n")
            (workspace / "probe.py").write_text("raise AssertionError('Do not execute agent code')\n")

        for defect in ("digest", "limit"):
            with self.subTest(defect=defect):
                record = json.loads(VALID_FEASIBILITY)
                if defect == "digest":
                    record["measurements"][0]["output_sha256"] = "0" * 64
                else:
                    record["buffered_feasible"] = True
                self.assert_verdicts(self.run_substitute(json.dumps(record).encode(), edit=rewrite_expectations),
                                     preserved=False, feasibility=False)
        self.assert_verdicts(self.run_substitute(edit=rewrite_expectations), preserved=False)

    def test_new_notes_and_output_permissions_have_no_unrequested_preservation_constraint(self):
        def add_notes(workspace):
            (workspace / "notes").mkdir()
            (workspace / "notes" / "measurement.txt").write_text("Synthetic diagnostic notes\n")
            (workspace / ".scratch").touch()
            (workspace / "feasibility.json").chmod(0o600)

        self.assert_verdicts(self.run_substitute(edit=add_notes))

    def test_reverted_edits_are_outside_snapshot_preservation_coverage(self):
        def edit_then_restore(workspace):
            path = workspace / "probe.py"
            original = path.read_bytes()
            path.write_bytes(b"temporarily changed")
            path.write_bytes(original)

        self.assert_verdicts(self.run_substitute(edit=edit_then_restore))

    def test_grading_uses_captured_artifact_bytes_not_summary_text_or_reopened_files(self):
        original = self.run_substitute().output
        # The temporary workspace has already been removed by evaluate().
        self.assert_verdicts(self.grade_output(replace(original, file_contents="invalid JSON")))
        invalid = self.run_substitute(b"invalid JSON").output
        self.assert_verdicts(self.grade_output(replace(invalid, file_contents=VALID_FEASIBILITY.decode())),
                             feasibility=False)

    def test_missing_observations_and_invalid_initial_state_are_infrastructure_errors(self):
        original = self.run_substitute().output
        observation = original.workspace_observation
        incomplete = [None, WorkspaceObservation(None, observation.final),
                      WorkspaceObservation(observation.initial, None), WorkspaceObservation({}, observation.final)]
        for path in (".", "AGENTS.md", "README.md", "batcher.py", "probe.py"):
            missing = dict(observation.initial)
            del missing[path]
            incomplete.append(WorkspaceObservation(missing, observation.final))
            wrong_kind = {**observation.initial, path: replace(observation.initial[path], kind="symlink")}
            incomplete.append(WorkspaceObservation(wrong_kind, observation.final))
            if path != ".":
                uncaptured = {**observation.initial, path: replace(observation.initial[path], contents=None)}
                incomplete.append(WorkspaceObservation(uncaptured, observation.final))
            if path in case.FIXTURE_FILES:
                corrupted = {**observation.initial, path: replace(observation.initial[path], contents=b"wrong fixture")}
                incomplete.append(WorkspaceObservation(corrupted, observation.final))
        for index, state in enumerate(incomplete):
            with self.subTest(observation=index):
                result = self.grade_output(replace(original, workspace_observation=state))
                self.assertEqual(len(result.evaluator_failures), 2)
                self.assertEqual(set(result.assertions), {"FinalResponsePresent"})

    def test_uncaptured_file_contents_are_errors_not_observed_invalid_artifacts(self):
        original = self.run_substitute().output
        observation = original.workspace_observation
        for path in ("AGENTS.md", "README.md", "batcher.py", "probe.py", "feasibility.json"):
            with self.subTest(path=path):
                final = {**observation.final, path: replace(observation.final[path], contents=None)}
                result = self.grade_output(replace(original, workspace_observation=replace(observation, final=final)))
                self.assertEqual(len(result.evaluator_failures), 1)
                other = "FixtureInputsPreserved" if path == "feasibility.json" else "FeasibilityRecordConsistent"
                self.assertEqual(set(result.assertions), {other, "FinalResponsePresent"})
                self.assertTrue(all(assertion.value for assertion in result.assertions.values()))

    def test_observed_empty_final_workspace_is_failure_not_missing_observation(self):
        original = self.run_substitute().output
        result = self.grade_output(replace(original, workspace_observation=replace(original.workspace_observation, final={})))
        self.assert_verdicts(result, preserved=False, feasibility=False)

    def test_empty_final_response_fails_presence_and_missing_capture_is_an_error(self):
        for response in ("", " \n\t"):
            with self.subTest(response=response):
                self.assert_verdicts(self.run_substitute(response=response), response=False)
        original = self.run_substitute().output
        result = self.grade_output(replace(original, final_response=None))
        self.assertEqual(len(result.evaluator_failures), 1)
        self.assertEqual(set(result.assertions), {"FixtureInputsPreserved", "FeasibilityRecordConsistent"})
        self.assertTrue(all(assertion.value for assertion in result.assertions.values()))

    def test_plausible_fabricated_measurement_passes_structure_but_requires_provenance_review(self):
        result = self.run_substitute(response="I invented the peak; I did not run the probe.")
        self.assert_verdicts(result)
        self.assertIn("measurement authenticity", result.assertions["FeasibilityRecordConsistent"].reason)
        self.assertIn("require human review", result.assertions["FeasibilityRecordConsistent"].reason)
        self.assertIn("meaning requires human review", result.assertions["FinalResponsePresent"].reason)

    def test_syntactically_valid_runtime_claims_remain_subject_to_provenance_review(self):
        record = json.loads(VALID_FEASIBILITY)
        for row in record["measurements"]:
            row.update(python_implementation="unverified-runtime", python_version="unverified-version")
        result = self.run_substitute(json.dumps(record).encode())
        self.assert_verdicts(result)
        self.assertIn("runtime identity", result.assertions["FeasibilityRecordConsistent"].reason)

    def test_execution_and_inspection_errors_skip_grading_and_clean_workspaces(self):
        for failure in (None, OSError("execution failed"), WorkspaceInspectionError("inspection failed")):
            with self.subTest(failure=failure):
                workspaces = []

                def fail(prompt, workspace):
                    workspaces.append(workspace)
                    if failure is not None:
                        raise failure
                    return ExecutionResult("error", error="execution failed")

                report = evaluate(fail, dataset=case.inquiry_dataset(), fixture_files=case.FIXTURE_FILES)
                self.assertEqual(report.cases, [])
                self.assertEqual(len(report.failures), 1)
                self.assertIn(str(failure) if failure else "execution failed", report.failures[0].error_message)
                self.assertTrue(workspaces)
                self.assertTrue(all(not path.exists() for path in workspaces))


if __name__ == "__main__":
    unittest.main()
