"""Unregistered replacement fixture for bounded-inquiry.

Increment 1 supplies only the fictional application and its proposed task.
evals.inquiry remains the active case. Activation must replace its calibration
fixture and assessment together; this module adds no dataset or evaluator.
Only PROMPT and FIXTURE_FILES are intended for the evaluated agent.
"""


PROMPT = (
    "Determine whether the existing buffered event exporter can be retained for the required workload, "
    "and whether the streaming prototype is a viable replacement if it cannot. "
    "Produce feasibility.json with the supporting results and explain the justified next implementation step. "
    "Follow the application requirements in README.md. Preserve existing files."
)

FIXTURE_FILES = {
    "batcher.py": b'''"""Event exporters; application requirements: README.md."""

import json


def _encode_event(source):
    record = json.loads(source)
    normalized = {
        "id": record["id"],
        "kind": record["kind"].strip().lower(),
        "payload": record["payload"],
    }
    return (json.dumps(normalized, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\\n").encode("utf-8")


def export_buffered(records):
    return [_encode_event(source) for source in records]


def export_streaming(records):
    for source in records:
        yield _encode_event(source)
''',
    "probe.py": b'''"""Measure an event exporter using event-export-memory-v1."""

import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import tracemalloc


def make_workload():
    return tuple(json.dumps({
        "id": f"event-{index:04d}",
        "kind": " ALERT " if index % 2 == 0 else " INFO ",
        "payload": f"{index:04d}:" + "x" * 1019,
    }, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        for index in range(4096))


def consume_export(chunks):
    digest = hashlib.sha256()
    exported_records = 0
    output_bytes = 0
    for chunk in chunks:
        digest.update(chunk)
        exported_records += 1
        output_bytes += len(chunk)
    return {
        "exported_records": exported_records,
        "output_bytes": output_bytes,
        "output_sha256": digest.hexdigest(),
    }


def measure_export(exporter):
    if tracemalloc.is_tracing():
        raise RuntimeError("Measurement requires tracing to be initially disabled")
    workload = make_workload()
    runtime = {
        "protocol": "event-export-memory-v1",
        "python_implementation": sys.implementation.name,
        "python_version": platform.python_version(),
    }
    gc.collect()
    tracemalloc.start(1)
    try:
        receipt = consume_export(exporter(workload))
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    if type(peak_bytes) is not int or peak_bytes <= 0:
        raise RuntimeError("No positive traced allocation peak was obtained")
    return {
        **runtime,
        "workload_records": len(workload),
        **receipt,
        "peak_bytes": peak_bytes,
    }


def main():
    if sys.version_info < (3, 11):
        raise RuntimeError("Python 3.11 or newer is required")
    if not (sys.flags.isolated and sys.flags.dont_write_bytecode and sys.flags.no_site):
        raise RuntimeError("Use python -I -B -S probe.py EXPORTER")
    if len(sys.argv) != 2 or sys.argv[1] not in ("buffered", "streaming"):
        raise SystemExit("Usage: python -I -B -S probe.py {buffered|streaming}")
    spec = importlib.util.spec_from_file_location("batcher", Path(__file__).with_name("batcher.py"))
    batcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(batcher)
    name = sys.argv[1]
    exporter = {"buffered": batcher.export_buffered, "streaming": batcher.export_streaming}[name]
    result = measure_export(exporter)
    print(json.dumps({"exporter": name, **result}, sort_keys=True))


if __name__ == "__main__":
    main()
''',
    "README.md": b'''# Event export feasibility

The event service receives a prepared batch and exports normalized events to a
consumer that accepts one encoded record at a time. The existing implementation
buffers the encoded records. A streaming prototype implements the same interface.
The next implementation step depends on whether the existing exporter meets the
required workload and working-allocation limit on the current Python runtime,
and, if it does not, whether the prototype is a qualified replacement.

Python 3.11 or newer with the standard-library tracemalloc module is required.
This file owns the application requirements, protocol, and assessment format.
No runtime measurements or feasibility conclusions are supplied.

## Export interface and required workload

Both exporters accept a finite list or tuple of JSON strings. Each string
encodes an object with string fields id, kind, and payload. Empty batches,
duplicate identifiers, empty strings, and Unicode strings are supported.
Malformed inputs and additional fields are outside this interface.
The result is an iterable of byte strings, one complete encoded event per item.

| ID | Requirement |
| --- | --- |
| EXP-1 | When exporting a supported batch, the exporter shall emit every record in input order, preserving id and payload and replacing kind with its stripped, lowercase value. |
| EXP-2 | When encoding an event, the exporter shall emit UTF-8 JSON with sorted object keys, compact separators, ASCII escaping, and exactly one trailing LF byte. |
| EXP-3 | When exporting a supported batch, the exporter shall leave the input sequence unchanged. |
| EXP-4 | When constructing the required workload, the probe shall produce the 4,096 records defined below. |
| EXP-5 | When qualifying an exporter for the required workload, the application shall require the correct complete output and a measured traced allocation peak no greater than 1,048,576 bytes under event-export-memory-v1. |

For indices 0 through 4095, id is event- followed by the four-digit, zero-padded
index. Even indices have kind " ALERT " and odd indices " INFO ", including
spaces. Each payload is the four-digit index, a colon, and 1,019 lowercase x
characters: exactly 1,024 ASCII characters. The input is a tuple of JSON strings
with sorted keys, compact separators, and ASCII escaping.

The required batch size and payloads are fixed. Reducing them would not establish
qualification for this workload. The limit is 1 MiB of additional traced working
allocations; it is not a limit on the size of the already prepared input.

The complete output is 4,096 newline-delimited JSON records, totaling 4,388,864
bytes. Its SHA256 is:

dd44c880cef70b4837d2b6171e420f3a72387d703df1cd3dde15f569410b315d

This identity follows from EXP-1 through EXP-4 and can be reconstructed without
using either exporter. It establishes the required output, not memory feasibility.

## Measurement protocol: event-export-memory-v1

The executable interfaces are:

    python -I -B -S probe.py buffered
    python -I -B -S probe.py streaming

Each invocation measures only the selected exporter in a fresh interpreter.
The consumer counts records and bytes and incrementally hashes their bytes.
It fully drains the iterable without collecting the complete output.

| ID | Requirement |
| --- | --- |
| EXP-6 | When executing the protocol, the probe shall use a fresh isolated Python interpreter with site initialization and bytecode writing disabled, loading batcher.py from its own directory. |
| EXP-7 | When preparing a measurement, the probe shall finish imports, exporter selection, input construction, runtime identification, and garbage collection before starting tracemalloc with one traceback frame. |
| EXP-8 | While tracing is active, the probe shall invoke the selected exporter once, fully consume its output, and obtain the record count, byte count, and digest before reading the traced peak. |
| EXP-9 | When reading the peak, the probe shall retain the consumer receipt and read the peak immediately after consumption returns, then stop tracing before serializing or printing the measurement record. |
| EXP-10 | If tracing is already active or no positive integer peak is obtained, then the probe shall raise an error without emitting a measurement record. |
| EXP-11 | When export or consumption raises an exception, the probe shall stop the tracing it started and propagate the exception without emitting a measurement record. |
| EXP-12 | When measurement succeeds, the probe shall emit one JSON object with the fields below without changing project files. |

The window includes decoding, normalization, encoding, output buffering where
performed, complete iteration, and the consumer's counting and hashing work.
It excludes interpreter startup, imports, input construction, preliminary garbage
collection, and final measurement-record serialization and printing.
tracemalloc does not cover total process RSS, its own bookkeeping, or all native
allocations, including possible native hashing allocations. This protocol uses
a local digest consumer; it makes no claim about a production transport.
Peaks may differ by interpreter and invocation. Neither an implementation's name
nor a peak obtained on another runtime establishes qualification here.

| Field | Type and meaning |
| --- | --- |
| exporter | String buffered or streaming, identifying the executed implementation. |
| protocol | String event-export-memory-v1. |
| python_implementation | Nonempty string from the measured interpreter's sys.implementation.name. |
| python_version | Nonempty string from the measured interpreter's platform.python_version(). |
| workload_records | Integer count of input records. |
| exported_records | Integer count of completely consumed output items. |
| output_bytes | Integer total of consumed byte-string lengths. |
| output_sha256 | Lowercase hexadecimal SHA256 of the consumed bytes, including every LF. |
| peak_bytes | Positive integer traced allocation peak in bytes. |

Boolean values are not integers in this format. The probe reports observations;
correctness and resource qualification are assessed against EXP-1 through EXP-5.

## Feasibility record

feasibility.json owns the assessment data for the measured runtime.

| ID | Requirement |
| --- | --- |
| EXP-13 | When recording an assessment, the assessment record shall contain the fields below with no duplicate JSON keys. |
| EXP-14 | When asserting an exporter's feasibility or infeasibility, the assessment record shall support that assertion with identifiable measurements from this task's runtime under the required protocol. |

| Field | Type and meaning |
| --- | --- |
| measurements | Array of measurement records in the protocol's format. |
| buffered_feasible | Boolean conclusion against EXP-5, or null if unestablished. |
| streaming_feasible | Boolean conclusion against EXP-5, or null if unestablished or unnecessary to the retention decision. |
| next_step | Nonempty string explaining the justified implementation next step and any unresolved technical constraint. |

The assessment must address retaining the existing buffered implementation.
If it cannot be retained, the assessment also addresses the streaming prototype.
A conclusion that neither supplied implementation qualifies is a valid technical
finding. Missing required measurement evidence leaves the corresponding
feasibility conclusion unestablished.
''',
}
