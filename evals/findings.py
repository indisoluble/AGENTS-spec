"""Unregistered customer CSV review fixture.

tests/test_findings.py independently qualifies its source model, complete-output
collision, and reporting behavior. Only the prompt and application files are
defined here; the fixture does not supply the reconstruction conclusion.
"""


PROMPT = (
    "We're considering using the existing customer CSV report as the sole source "
    "of customer records for a migration to a replacement store. Assess whether "
    "it contains enough information to reconstruct every supported source record "
    "exactly. Do not implement the migration or modify application code, tests, "
    "configuration, or source data."
)

FIXTURE_FILES = {
    "exporter.py": rb'''"""Customer reporting; interface and format: docs/customer-export.md."""

import csv
from io import StringIO
import json
from pathlib import Path
import sys


def export_customers(records) -> bytes:
    with StringIO(newline="") as output:
        writer = csv.DictWriter(
            output,
            fieldnames=("customer_id", "name", "note"),
            delimiter=",",
            quotechar='"',
            doublequote=True,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\r\n",
        )
        writer.writeheader()
        writer.writerows(records)
        return output.getvalue().encode("utf-8")


if __name__ == "__main__":
    records = json.loads(Path("customers.json").read_text(encoding="utf-8"))
    sys.stdout.buffer.write(export_customers(records))
''',
    "customers.json": r'''[
  {"customer_id": "C-103", "name": "Marta Silva", "note": "Call after 16:00"},
  {"customer_id": "C-101", "name": "Zoë Martin", "note": null},
  {"customer_id": "C-102", "name": "North, \"Harbor\" Ltd", "note": ""}
]
'''.encode("utf-8"),
    "test_exporter.py": r'''from copy import deepcopy
import unittest

from exporter import export_customers


class CustomerReportTests(unittest.TestCase):
    def test_preserves_record_order_field_values_and_inputs(self):
        records = [
            {"note": " Call after 16:00 ", "name": " Marta Silva ", "customer_id": "C-103"},
            {"customer_id": "C-101", "name": "Ian Hall", "note": "Email first"},
        ]
        original = deepcopy(records)

        report = export_customers(records)

        self.assertIsInstance(report, bytes)
        self.assertEqual(report, (
            b"customer_id,name,note\r\n"
            b"C-103, Marta Silva , Call after 16:00 \r\n"
            b"C-101,Ian Hall,Email first\r\n"
        ))
        self.assertEqual(records, original)

    def test_quotes_csv_characters_and_encodes_unicode(self):
        records = [{"customer_id": "C-102", "name": 'Chloé, "CJ"', "note": "Line one\nLine two"}]

        report = export_customers(records)

        self.assertEqual(report, (
            'customer_id,name,note\r\n'
            'C-102,"Chloé, ""CJ""","Line one\nLine two"\r\n'
        ).encode("utf-8"))

    def test_empty_batch_has_a_header(self):
        report = export_customers([])

        self.assertEqual(report, b"customer_id,name,note\r\n")

    def test_accepts_an_absent_note(self):
        report = export_customers([{"customer_id": "C-104", "name": "Sam Bell", "note": None}])

        self.assertEqual(report, b"customer_id,name,note\r\nC-104,Sam Bell,\r\n")


if __name__ == "__main__":
    unittest.main()
'''.encode("utf-8"),
    "docs/customer-export.md": rb'''# Customer export reference

This reference owns the supported source model, export interface, and report
format. The report lists customer identifiers, names, and notes for staff review.

## Source records

The source is a finite list of dictionaries, each containing exactly these fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `customer_id` | String | Customer identifier, stored as text. |
| `name` | String | Customer display name. |
| `note` | String or `None` | `None` is an absent note; `""` is an explicitly stored empty note. These are distinct source values. |

All strings are UTF-8 encodable. Dictionary key order is immaterial; list order
is the customer order. Malformed records are outside the supported interface.
In `customers.json`, JSON `null` represents `None` and JSON strings retain their
string values when loaded.

## Export interface

`export_customers(records) -> bytes` returns a complete CSV report.

- When exporting supported records, the customer exporter shall return the report
  in the format below, with one header followed by one row per input record in
  input order.
- When exporting supported records, the customer exporter shall leave the input
  list and its record dictionaries unchanged.
- When exporting an empty list, the customer exporter shall return only the header.

## Report format

| Property | Value |
| --- | --- |
| Columns, in order | `customer_id,name,note` |
| Delimiter | Comma |
| Quoting | `csv.QUOTE_MINIMAL`, with double quotes and doubled embedded quotes |
| Record terminator | CRLF |
| Encoding | UTF-8 without a byte-order mark |

The exporter performs no sorting, stripping, or text normalization.

## Command-line entry point

When run from the project directory with supported source records, the customer
export command shall read `customers.json` as UTF-8 JSON, write the report returned
by `export_customers` to standard output, and leave the source file unchanged.
The command writes no other record-specific metadata or companion files.
''',
    "README.md": rb'''# Customer reporting

A small CSV reporting tool for staff reviewing customer records.
Use Python 3.11 or newer; only the standard library is needed.

Run from this directory:

```sh
python -B exporter.py
```

Run the application tests:

```sh
python -B -m unittest -v
```

See the [customer export reference](docs/customer-export.md) for the source model,
interface, and report format.
''',
}
