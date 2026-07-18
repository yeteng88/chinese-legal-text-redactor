"""Redaction rules for common identifiers found in Chinese legal text."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RedactionRule:
    name: str
    placeholder: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class RedactionResult:
    text: str
    counts: dict[str, int]

    @property
    def total(self) -> int:
        return sum(self.counts.values())


# Order matters: specific, structured identifiers run before broader digit rules.
RULES: tuple[RedactionRule, ...] = (
    RedactionRule(
        "email",
        "[EMAIL]",
        re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"),
    ),
    RedactionRule(
        "id_card",
        "[ID_CARD]",
        re.compile(r"(?<![0-9A-Za-z])(?:\d{17}[0-9Xx]|\d{15})(?![0-9A-Za-z])"),
    ),
    RedactionRule(
        "mobile",
        "[MOBILE]",
        re.compile(r"(?<!\d)(?:(?:\+|00)86[- ]?)?1[3-9]\d{9}(?!\d)"),
    ),
    RedactionRule(
        "phone",
        "[PHONE]",
        re.compile(r"(?<!\d)0\d{2,3}[- ]?\d{7,8}(?!\d)"),
    ),
    RedactionRule(
        "bank_card",
        "[BANK_CARD]",
        re.compile(r"(?<!\d)(?:\d[ -]?){15,18}\d(?!\d)"),
    ),
)


def available_types() -> tuple[str, ...]:
    """Return supported redaction type names in processing order."""

    return tuple(rule.name for rule in RULES)


def _selected_rules(types: Iterable[str] | None) -> tuple[RedactionRule, ...]:
    if types is None:
        return RULES

    requested = tuple(dict.fromkeys(types))
    unknown = sorted(set(requested) - set(available_types()))
    if unknown:
        raise ValueError(f"Unsupported redaction type(s): {', '.join(unknown)}")
    return tuple(rule for rule in RULES if rule.name in requested)


def redact_with_report(text: str, types: Iterable[str] | None = None) -> RedactionResult:
    """Redact selected identifier types and return replacement counts."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    cleaned = text
    counts: dict[str, int] = {}
    for rule in _selected_rules(types):
        cleaned, count = rule.pattern.subn(rule.placeholder, cleaned)
        counts[rule.name] = count
    return RedactionResult(cleaned, counts)


def redact_text(text: str, types: Iterable[str] | None = None) -> str:
    """Redact selected identifier types and return only the cleaned text."""

    return redact_with_report(text, types).text
