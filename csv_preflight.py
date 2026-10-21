"""Read-only CSV checks using only the Python standard library."""

import argparse
from collections import Counter
import csv
import sys


def validate(source, required=(), unique=None):
    """Return diagnostics for a text stream; line numbers are physical end lines."""
    reader = csv.reader(source, strict=True)
    headers = next(reader, None)
    if headers is None:
        return ["empty file: a header row is required"]
    headers = [name.strip() for name in headers]
    errors = []
    if not headers or any(not name for name in headers):
        errors.append("header: column names must not be blank")
    for name, count in Counter(headers).items():
        if count > 1:
            errors.append("header: duplicate column {!r}".format(name))
    needed = set(required)
    if unique is not None:
        needed.add(unique)
    for name in sorted(needed - set(headers)):
        errors.append("header: missing column {!r}".format(name))
    if errors:
        return errors

    checked = [(headers.index(name), name) for name in sorted(needed)]
    unique_index = headers.index(unique) if unique is not None else None
    seen = set()
    for row in reader:
        location = "line {}".format(reader.line_num)
        if len(row) != len(headers):
            errors.append("{}: expected {} fields, found {}".format(
                location, len(headers), len(row)))
            continue
        for index, name in checked:
            if not row[index].strip():
                errors.append("{}: blank value in {!r}".format(location, name))
        if unique_index is not None:
            value = row[unique_index].strip()
            if value and value in seen:
                errors.append("{}: duplicate value in {!r}".format(location, unique))
            seen.add(value)
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="UTF-8 comma-delimited CSV (BOM is accepted)")
    parser.add_argument("--require", action="append", default=[], metavar="COLUMN",
                        help="require a column and nonblank values; repeat as needed")
    parser.add_argument("--unique", metavar="COLUMN",
                        help="require nonblank, unique values in one column")
    args = parser.parse_args(argv)
    try:
        with open(args.file, encoding="utf-8-sig", newline="") as source:
            errors = validate(source, args.require, args.unique)
    except csv.Error as exc:
        print("FAIL: invalid CSV: {}".format(exc), file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print("ERROR: {}".format(exc), file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        return 1
    print("PASS: " + args.file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
