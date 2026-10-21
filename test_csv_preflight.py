import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from csv_preflight import validate


class CsvPreflightTests(unittest.TestCase):
    def test_validation(self):
        cases = [
            ("id,group\na,A\nb,B\n", ["group"], "id", None),
            ('id,note\na,"hello,\nworld"\n', [], "id", None),
            ("id,group\n甲,对照\n", ["group"], "id", None),
            (" id ,group\na,A\n", [], "id", None),
            ("id,group\n", [], "id", None),
            ("", [], None, "empty file"),
            ("\n", [], None, "column names must not be blank"),
            ("id, \na,A\n", [], None, "column names must not be blank"),
            ("id, id\na,b\n", [], None, "duplicate column"),
            ("id\na\n", ["group"], None, "missing column 'group'"),
            ("id\na\n", [], "sample", "missing column 'sample'"),
            ("id,group\na\n", [], None, "expected 2 fields, found 1"),
            ("id\na,b\n", [], None, "expected 1 fields, found 2"),
            ("id\n\n", [], None, "expected 1 fields, found 0"),
            ("id,group\na, \n", ["group"], None, "blank value in 'group'"),
            ("id\n \n", [], "id", "blank value in 'id'"),
            ("id\na\n a \n", [], "id", "line 3: duplicate value"),
        ]
        for text, required, unique, expected in cases:
            with self.subTest(text=text, required=required, unique=unique):
                errors = validate(io.StringIO(text, newline=""), required, unique)
                if expected is None:
                    self.assertEqual(errors, [])
                else:
                    self.assertTrue(any(expected in error for error in errors), errors)

    def test_cli_and_read_only_input(self):
        script = str(Path(__file__).with_name("csv_preflight.py"))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.csv"
            cases = [
                (b"\xef\xbb\xbfid,group\r\na,A\r\n", 0, "PASS:"),
                (b"id,group\na\n", 1, "expected 2 fields"),
                (b'id,group\na,"unterminated', 1, "invalid CSV"),
                (b"id,group\na,\xff\n", 2, "ERROR:"),
            ]
            for content, code, message in cases:
                with self.subTest(content=content):
                    path.write_bytes(content)
                    result = subprocess.run(
                        [sys.executable, script, str(path), "--unique", "id"],
                        capture_output=True, text=True)
                    self.assertEqual(result.returncode, code, result.stderr)
                    self.assertIn(message, result.stdout + result.stderr)
                    self.assertEqual(path.read_bytes(), content)
            result = subprocess.run(
                [sys.executable, script, str(Path(folder) / "missing.csv")],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
