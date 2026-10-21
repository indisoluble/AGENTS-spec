"""Original importer fixture and requested change for contract-change-followthrough."""


PROMPT = """Change import_records(store, records) to reject a batch containing repeated
record IDs by raising ValueError, without changing the store or input records.
Add appropriate regression tests for this change.

Duplicate IDs are case-sensitive: "A" and "a" are distinct. Repeated IDs with
identical values are still duplicates. An ID already present in the store is a
valid update if it appears only once in the incoming batch. On rejection, the
entire store must equal its pre-call contents, including entries that earlier
records might otherwise have inserted or updated.

Preserve the other supported behavior: unique batches insert or update entries,
leave unrelated store entries unchanged, and return None; empty batches leave
the store unchanged and return None. Input records must remain unchanged on
both success and rejection. A ValueError subclass is acceptable, and exception
wording is unrestricted.

Supported inputs remain a dictionary and a finite list of well-formed records
containing string IDs and values. Malformed records, generators, concurrency,
crash recovery, and persistent storage are outside this interface. The guarantee
concerns the observable state when the call exits; choose any implementation
that satisfies it.

Keep work limited to this importer change, its tests, and affected project
documentation. Use only the Python standard library, preserve the public
function and documented test command, and leave AGENTS.md unchanged.
"""

FIXTURE_FILES = {
    "importer.py": b'''"""Import records into a caller-owned store; contract: docs/importer.md."""


def import_records(store, records):
    for record in records:
        store[record["id"]] = record["value"]
''',
    "test_importer.py": b'''from copy import deepcopy
import unittest

from importer import import_records


class ImportRecordsTests(unittest.TestCase):
    def test_inserts_updates_and_preserves_unrelated_entries_and_input(self):
        store = {"existing": "old", "untouched": "keep"}
        records = [
            {"id": "new", "value": "added"},
            {"id": "existing", "value": "updated"},
        ]
        original_records = deepcopy(records)

        result = import_records(store, records)

        self.assertIsNone(result)
        self.assertEqual(store, {"existing": "updated", "untouched": "keep", "new": "added"})
        self.assertEqual(records, original_records)

    def test_empty_batch_leaves_store_unchanged(self):
        store = {"existing": "keep"}
        records = []

        result = import_records(store, records)

        self.assertIsNone(result)
        self.assertEqual(store, {"existing": "keep"})
        self.assertEqual(records, [])

    def test_last_value_wins_for_repeated_ids(self):
        store = {"item": "old", "untouched": "keep"}
        records = [
            {"id": "item", "value": "first"},
            {"id": "other", "value": "added"},
            {"id": "item", "value": "last"},
        ]
        original_records = deepcopy(records)

        result = import_records(store, records)

        self.assertIsNone(result)
        self.assertEqual(store, {"item": "last", "untouched": "keep", "other": "added"})
        self.assertEqual(records, original_records)


if __name__ == "__main__":
    unittest.main()
''',
    "README.md": b'''# Record importer

A small Python module for applying batches of records to an in-memory dictionary.
Use Python 3.11 or newer; only the standard library is needed.

```python
from importer import import_records

store = {"saved": "old"}
import_records(store, [
    {"id": "item", "value": "first"},
    {"id": "item", "value": "last"},
])
print(store)  # {'saved': 'old', 'item': 'last'}
```

Repeated IDs currently use the last value in the batch, as in this example.
The [importer contract](docs/importer.md) owns the API details and
enduring requirements; this example follows that contract.

Run the project's tests from this directory:

```sh
python -B -m unittest -v
```
''',
    "docs/importer.md": b'''# Importer contract

This file is the canonical owner of the current API and enduring requirements.
README.md provides usage examples and test instructions based on this contract.

## Supported interface

`import_records(store, records)` operates on a caller-owned dictionary mapping
string IDs to string values. `records` is a finite list of dictionaries, each
containing an `id` string and a `value` string. IDs use exact, case-sensitive
string equality; matching a store key is an update, not an invalid input.

Malformed records, generators, concurrency, crash recovery, and persistent
storage are outside the supported interface. The contract concerns observable
contents when the call exits, not intermediate operations.

## Enduring requirements

These requirements govern supported calls, not the completion of a development
task. Last-value-wins is the current accepted duplicate policy.

| ID | Requirement |
| --- | --- |
| IMP-1 | When importing a batch, the importer shall insert or update each ID in the supplied store with the last value for that ID in the batch. |
| IMP-2 | When importing a batch, the importer shall preserve store entries whose IDs do not occur in the batch. |
| IMP-3 | The importer shall compare record IDs using case-sensitive string equality. |
| IMP-4 | When importing a batch, the importer shall leave the input list and its record dictionaries unchanged. |
| IMP-5 | When importing a batch, the importer shall return None. |

For an empty batch, IMP-2 preserves the entire store and IMP-5 still requires
None. Repeating an ID with the same value is also accepted under IMP-1.
''',
}
