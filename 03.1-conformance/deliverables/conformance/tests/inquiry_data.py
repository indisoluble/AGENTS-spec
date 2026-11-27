import json


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
