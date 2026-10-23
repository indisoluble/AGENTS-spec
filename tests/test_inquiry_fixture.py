"""Independently qualify the unregistered event-export fixture, without agents.

Output expectations use literal wire-format construction, not exporter helpers.
Instrumentation verifies measurement boundaries and full lazy consumption.
Fresh-process measurements qualify only the interpreter running these tests:
twofold headroom is a fixture-qualification gate, not an application requirement
or a portable memory peak. It does not prescribe which implementation wins.
Supplied text additionally needs semantic review for contract isolation.
"""

import ast
import gc
import hashlib
import json
import os
import platform
import runpy
import subprocess
import sys
import tracemalloc
import unittest
from unittest.mock import patch

from evals import inquiry_fixture as fixture
from evals.workspace import CONTRACT_PATH, prepare_workspace, snapshot_workspace


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


class ExportFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files=fixture.FIXTURE_FILES))
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
        self.assertEqual(set(fixture.FIXTURE_FILES), {"batcher.py", "probe.py", "README.md"})
        self.assertEqual(set(snapshot_workspace(self.workspace)),
                         {".", "AGENTS.md", "batcher.py", "probe.py", "README.md"})
        self.assertEqual((self.workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())
        self.assertIn("whether the existing buffered event exporter can be retained", fixture.PROMPT)
        for name, contents in fixture.FIXTURE_FILES.items():
            self.assertIsInstance(contents, bytes)
            self.assertEqual((self.workspace / name).read_bytes(), contents)
        # This catches accidental policy copying; semantic isolation is also
        # reviewed, rather than inferred from a blacklist passing.
        supplied = fixture.PROMPT + "\n" + "\n".join(
            contents.decode("utf-8") for contents in fixture.FIXTURE_FILES.values()
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
        self.assertIn(EXPECTED_DIGEST, fixture.FIXTURE_FILES["README.md"].decode("utf-8"))
        self.assertIn("1,048,576 bytes", fixture.FIXTURE_FILES["README.md"].decode("utf-8"))

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
            ast.parse(fixture.FIXTURE_FILES[name].decode("utf-8"), filename=name, feature_version=(3, 11))
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


if __name__ == "__main__":
    unittest.main()
