# csv-preflight

Check a CSV before passing it to an analysis script. Finds mismatched row lengths,
missing values in required columns, and duplicate IDs. Uses the Python standard
library and leaves the input file alone.

## Usage

Requires Python 3.9 or later. For a file named `samples.csv`:

```csv
sample_id,group
S01,control
S02,treated
```

```sh
python csv_preflight.py samples.csv --require group --unique sample_id
```

This prints `PASS: samples.csv`. If both rows use `S01`, it reports:

```text
FAIL: line 3: duplicate value in 'sample_id'
```

Run without flags to check headers and row lengths only. Empty files, blank or
duplicate headers, and blank rows fail. A header-only file passes.

`--require COLUMN` checks that a column exists and has no blank values; repeat it
for more columns. `--unique COLUMN` also rejects duplicates. These checks trim
surrounding whitespace and are case-sensitive.

Input must be comma-delimited UTF-8; a BOM and Windows line endings are accepted.
Quoted commas and newlines follow Python's `csv` parser. Reported line numbers
refer to the end of a record. The checker does not validate data types or infer
a schema. Diagnostics and unique IDs are kept in memory.

Exit codes: `0` passed, `1` invalid CSV, `2` file, encoding or argument error.
Errors go to stderr. On Windows, use `py` if `python` is not on your PATH.

## Development

```sh
python -m unittest -v
```

CI runs these tests on Ubuntu and Windows with Python 3.9 and 3.13. For bugs,
open an issue with the command and a small CSV that reproduces the problem.
Use made-up data if the original contains private information.

[MIT license](LICENSE).

## 中文说明

在运行分析脚本前，检查 CSV 是否缺列、缺值、行列数不一致或 ID 重复。
直接运行上面的命令即可，不需要安装第三方包，也不会修改原文件。
`--require` 指定必填列，`--unique` 指定不能重复的 ID 列。
