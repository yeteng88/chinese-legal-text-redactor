"""Command-line interface for Chinese Legal Text Redactor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .redactor import available_types, redact_with_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cn-legal-redactor",
        description="离线脱敏中文法律文本中的常见个人信息。",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="输入文本文件；省略或使用 - 时从标准输入读取。",
    )
    parser.add_argument("-o", "--output", help="输出文件；省略时写入标准输出。")
    parser.add_argument(
        "--types",
        help="逗号分隔的处理类型：" + ",".join(available_types()),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="不在标准错误中输出替换统计。",
    )
    return parser


def _read_input(value: str) -> str:
    if value == "-":
        return sys.stdin.read()
    return Path(value).read_text(encoding="utf-8")


def _write_output(value: str, output: str | None) -> None:
    if output:
        Path(output).write_text(value, encoding="utf-8")
    else:
        sys.stdout.write(value)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    selected = None
    if args.types:
        selected = [item.strip() for item in args.types.split(",") if item.strip()]

    try:
        result = redact_with_report(_read_input(args.input), selected)
        _write_output(result.text, args.output)
    except (OSError, UnicodeError, TypeError, ValueError) as exc:
        parser.error(str(exc))

    if not args.quiet:
        summary = ", ".join(f"{name}={count}" for name, count in result.counts.items())
        print(f"redacted: total={result.total}; {summary}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
