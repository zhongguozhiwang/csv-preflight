# csv-preflight

A small, read-only CSV checker for sample sheets, metadata tables and other
tabular inputs. Python standard library only; no installation, API key or network
access required. Maintained by [zhongguozhiwang](https://github.com/zhongguozhiwang).

## Quick start

Requires Python 3.9 or later. Save this synthetic example as `samples.csv`:

```csv
sample_id,group
S01,control
S02,treated
```

From the repository directory, run:

```sh
python csv_preflight.py samples.csv --require group --unique sample_id
```

Expected output: `PASS: samples.csv` (exit status 0).
On Windows, `py` may be used in place of `python`.

## Checks and behavior

- Reject empty files and empty or duplicate column names.
- Reject rows with too few or too many fields, including blank rows.
- `--require COLUMN` requires that column and nonblank values; repeat the flag
  for additional columns.
- `--unique COLUMN` also requires the column and nonblank, unique values.
- Accept UTF-8 with or without a BOM, CRLF, quoted commas and quoted newlines.
- Trim surrounding whitespace when comparing column names and checked values.
  Comparisons remain case-sensitive; the input file is never changed.
- Report parsing errors from Python's standard comma-delimited CSV reader.

Exit statuses: **0** checks passed, **1** validation failed, **2** input/encoding
or command-line error. Diagnostics go to stderr. Line numbers refer to the
physical end line of a CSV record, which may span several lines.

A header-only table passes. This tool checks structure and explicitly requested
constraints, not scientific validity, data types, spreadsheet formulas or all
possible CSV dialects. It keeps diagnostics and unique identifiers in memory;
it is intended for small to medium metadata files rather than massive datasets.

## Tests and contributions

```sh
python -m unittest -v
```

The tests cover valid and malformed input, Unicode, BOM/CRLF, quoted multiline
fields, schema checks, identifiers, CLI exit statuses and preservation of input
bytes. GitHub Actions runs the same command on Ubuntu and Windows with Python
3.9 and 3.13.

This is an initial, early-stage release. External adoption and download metrics
have not been established. Bug reports and focused pull requests are welcome:
include the command, expected result and a **synthetic, minimal CSV example**.
Do not upload private sample information, credentials or other sensitive data.
Keep changes dependency-free and add a regression case for changed behavior.

Initial implementation and documentation were developed with Codex assistance.
License: [MIT](LICENSE).

## 中文说明

一个零依赖、只读的 CSV 检查工具，适合样本清单和元数据表。可检查空表、
重复或空列名、行列数不一致、必填值缺失和标识符重复。支持 UTF-8 BOM、
中文和带引号的多行字段，不会修改或上传输入数据。

示例：`python csv_preflight.py samples.csv --require group --unique sample_id`。
返回码 0 表示通过，1 表示数据校验失败，2 表示文件、编码或命令行错误。
项目刚起步，尚无已证实的外部采用或下载指标。欢迎使用合成数据报告问题。
