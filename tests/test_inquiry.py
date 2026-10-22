"""Validate the trusted calibration fixture, without grading agent behavior.

Expected records, digest, and arithmetic examples are independent of fixture
implementation. Instrumented unit calls check measurement boundaries; the
unmodified probe also runs in a real isolated subprocess without a fixed peak.
Contract isolation additionally requires semantic review of all supplied text.
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
import weakref

from evals import inquiry as case
from evals.workspace import CONTRACT_PATH, prepare_workspace, snapshot_workspace


EXPECTED_DIGEST = "d88f124d57f3f1d7e00bca38de8699de70cfd1ca3eb5430b709ef14be38382d9"


def expected_json_records(*, normalized):
    # Explicit ASCII serialization is independent of the probe's JSON encoder
    # and the batcher's decoder/normalizer. All field contents are fixed here.
    kinds = ("alert", "info") if normalized else (" ALERT ", " INFO ")
    return tuple(
        '{"id":"event-%04d","kind":"%s","payload":"%04d:%s"}'
        % (index, kinds[index % 2], index, "x" * 1019)
        for index in range(256)
    )


class InquiryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files=case.FIXTURE_FILES))
        self.batcher = runpy.run_path(str(self.workspace / "batcher.py"))
        self.probe = runpy.run_path(str(self.workspace / "probe.py"))

    def test_exact_prompt_and_initial_files_supply_no_calibration_result(self):
        self.assertEqual(case.PROMPT,
                         "Produce `calibration.json` for this Python runtime using the policy in `README.md`. "
                         "Preserve existing files.")
        self.assertEqual(set(case.FIXTURE_FILES), {"batcher.py", "probe.py", "README.md"})
        self.assertEqual(set(snapshot_workspace(self.workspace)),
                         {".", "AGENTS.md", "batcher.py", "probe.py", "README.md"})
        self.assertEqual((self.workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())
        for name, contents in case.FIXTURE_FILES.items():
            with self.subTest(path=name):
                self.assertIsInstance(contents, bytes)
                self.assertEqual((self.workspace / name).read_bytes(), contents)

    def test_importing_supplied_scripts_does_not_measure_or_emit_a_result(self):
        with patch("tracemalloc.start", side_effect=AssertionError("Unexpected measurement")), \
                patch("builtins.print", side_effect=AssertionError("Unexpected output")):
            for name in ("batcher.py", "probe.py"):
                namespace = runpy.run_path(str(self.workspace / name))
                self.assertNotIn("peak_bytes", namespace)
                self.assertNotIn("recommended_batch_size", namespace)

    def test_workload_matches_all_independently_specified_records(self):
        workload = self.probe["make_workload"]()

        self.assertIsInstance(workload, tuple)
        self.assertEqual(workload, expected_json_records(normalized=False))
        self.assertEqual(len(workload), 256)
        self.assertTrue(all(len(json.loads(record)["payload"]) == 1024 for record in workload))

    def test_normalization_preserves_order_payloads_identifiers_and_input(self):
        sources = expected_json_records(normalized=False)
        expected = [json.loads(record) for record in expected_json_records(normalized=True)]
        for records in (sources, list(sources)):
            with self.subTest(sequence=type(records).__name__):
                original = records[:]

                normalized = self.batcher["normalize_batch"](records)

                self.assertIsInstance(normalized, list)
                self.assertEqual(normalized, expected)
                self.assertEqual(records, original)

    def test_empty_batch_has_empty_output_and_unchanged_input(self):
        records = []
        self.assertEqual(self.batcher["normalize_batch"](records), [])
        self.assertEqual(records, [])

    def test_independent_canonical_output_establishes_documented_digest(self):
        encoded = ("[" + ",".join(expected_json_records(normalized=True)) + "]").encode("ascii")
        self.assertEqual(len(encoded), 274305)
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), EXPECTED_DIGEST)
        self.assertIn(EXPECTED_DIGEST, case.FIXTURE_FILES["README.md"].decode("utf-8"))

    def test_calibration_arithmetic_covers_cap_rounding_and_zero_candidate(self):
        for peak, expected in ((1, 4096), (262144, 4096), (262145, 4095),
                               (300000, 3579), (524288, 2048),
                               (1073741824, 1), (1073741825, 0)):
            with self.subTest(peak=peak):
                actual = self.batcher["recommend_batch_size"](peak)
                self.assertIs(type(actual), int)
                self.assertEqual(actual, expected)

    def test_calibration_rejects_nonpositive_and_noninteger_peaks(self):
        for peak in (0, -1, True, False, 1.5, "1024", None, [], {}, float("inf"), float("nan")):
            with self.subTest(peak=peak):
                with self.assertRaises(ValueError):
                    self.batcher["recommend_batch_size"](peak)

    def test_measurement_window_excludes_setup_and_serialization_and_retains_output(self):
        measure = self.probe["measure_batch"]
        make_workload = measure.__globals__["make_workload"]
        real_collect, real_dumps = gc.collect, json.dumps
        real_peak, real_hash = tracemalloc.get_traced_memory, hashlib.sha256
        observed = {"calls": 0}

        class Records(list):
            pass

        def build_workload():
            self.assertFalse(tracemalloc.is_tracing())
            observed["workload"] = make_workload()
            return observed["workload"]

        def collect():
            self.assertFalse(tracemalloc.is_tracing())
            self.assertIn("workload", observed)
            observed["collected"] = True
            return real_collect()

        def normalize(records):
            self.assertIs(records, observed["workload"])
            self.assertTrue(observed["collected"])
            self.assertTrue(tracemalloc.is_tracing())
            self.assertEqual(tracemalloc.get_traceback_limit(), 1)
            observed["calls"] += 1
            result = Records(self.batcher["normalize_batch"](records))
            observed["result"] = weakref.ref(result)
            return result

        def read_peak():
            self.assertTrue(tracemalloc.is_tracing())
            self.assertIsNotNone(observed["result"]())
            current, peak = real_peak()
            observed["peak"] = peak
            return current, peak

        def serialize(value, **options):
            self.assertFalse(tracemalloc.is_tracing())
            return real_dumps(value, **options)

        def digest(encoded):
            self.assertFalse(tracemalloc.is_tracing())
            self.assertEqual(encoded, ("[" + ",".join(expected_json_records(normalized=True)) + "]").encode("ascii"))
            return real_hash(encoded)

        with patch.dict(measure.__globals__, {"make_workload": build_workload}), \
                patch("gc.collect", collect), patch("json.dumps", serialize), \
                patch("tracemalloc.get_traced_memory", read_peak), patch("hashlib.sha256", digest):
            result = measure(normalize)

        self.assertFalse(tracemalloc.is_tracing())
        self.assertEqual(observed["calls"], 1)
        self.assertEqual(result["peak_bytes"], observed["peak"])
        self.assertEqual(result["output_sha256"], EXPECTED_DIGEST)

    def test_normalization_failure_stops_tracing_without_returning_measurement(self):
        def fail(records):
            raise ValueError("Unusable batch")

        with self.assertRaisesRegex(ValueError, "Unusable batch"):
            self.probe["measure_batch"](fail)
        self.assertFalse(tracemalloc.is_tracing())

    def test_existing_tracing_is_rejected_without_stopping_its_owner(self):
        tracemalloc.start()
        try:
            with self.assertRaisesRegex(RuntimeError, "initially disabled"):
                self.probe["measure_batch"](self.batcher["normalize_batch"])
            self.assertTrue(tracemalloc.is_tracing())
        finally:
            tracemalloc.stop()

    def test_unavailable_positive_peak_is_rejected_without_a_measurement(self):
        with patch("tracemalloc.get_traced_memory", return_value=(0, 0)):
            with self.assertRaisesRegex(RuntimeError, "No positive traced allocation peak"):
                self.probe["measure_batch"](self.batcher["normalize_batch"])
        self.assertFalse(tracemalloc.is_tracing())

    def test_real_isolated_probe_emits_valid_metadata_and_preserves_all_files(self):
        initial = snapshot_workspace(self.workspace)
        completed = subprocess.run(
            [sys.executable, "-I", "-B", "-S", "probe.py"], cwd=self.workspace,
            env={**os.environ, "PYTHONTRACEMALLOC": "5", "PYTHONPATH": "/nonexistent"},
            capture_output=True, text=True, timeout=10,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(completed.stderr, "")
        self.assertEqual(snapshot_workspace(self.workspace), initial)
        pairs = json.loads(completed.stdout, object_pairs_hook=list)
        result = dict(pairs)
        self.assertEqual(len(pairs), len(result), "Duplicate output keys")
        self.assertEqual(set(result), {"protocol", "python_implementation", "python_version",
                                       "sample_records", "peak_bytes", "output_sha256"})
        self.assertEqual(result["protocol"], "batch-memory-v1")
        self.assertEqual(result["python_implementation"], sys.implementation.name)
        self.assertEqual(result["python_version"], platform.python_version())
        self.assertIs(type(result["sample_records"]), int)
        self.assertEqual(result["sample_records"], 256)
        self.assertIs(type(result["peak_bytes"]), int)
        self.assertGreater(result["peak_bytes"], 0)
        self.assertEqual(result["output_sha256"], EXPECTED_DIGEST)

    def test_command_rejects_missing_isolation_or_site_or_bytecode_flags(self):
        for flags in (("-B", "-S"), ("-I", "-S"), ("-I", "-B")):
            with self.subTest(flags=flags):
                completed = subprocess.run(
                    [sys.executable, *flags, "probe.py"], cwd=self.workspace,
                    env={key: value for key, value in os.environ.items() if not key.startswith("PYTHON")},
                    capture_output=True, text=True, timeout=10,
                )
                self.assertNotEqual(completed.returncode, 0)
                self.assertEqual(completed.stdout, "")
                self.assertIn("Use python -I -B -S probe.py", completed.stderr)

    def test_scripts_use_python_311_syntax(self):
        # Syntax compatibility is separate from the actual interpreter used by
        # the subprocess test; this does not claim execution on every version.
        for name in ("batcher.py", "probe.py"):
            with self.subTest(path=name):
                ast.parse(case.FIXTURE_FILES[name].decode("utf-8"), filename=name, feature_version=(3, 11))


if __name__ == "__main__":
    unittest.main()
