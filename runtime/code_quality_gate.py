#!/usr/bin/env python3
"""Mindway Code Quality Gate reference runtime.

This scanner intentionally implements only high-confidence deterministic hints.
It does not replace project linters, tests, security tools, or human review.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx"}
TYPE_ESCAPE_PATTERNS = (
    (re.compile(r"\bas\s+any\b"), "TypeScript `as any` escape"),
    (re.compile(r"(?<![A-Za-z0-9_])any(?![A-Za-z0-9_])", re.IGNORECASE), "Possible broad `any` type"),
    (re.compile(r"#\s*type:\s*ignore\b"), "Python type-ignore escape"),
)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    family: str
    path: str
    line: int
    message: str
    severity: str
    confidence: float


def iter_source_files(targets: Iterable[str]) -> Iterable[Path]:
    seen: set[Path] = set()
    for raw in targets:
        target = Path(raw)
        candidates = [target] if target.is_file() else target.rglob("*") if target.is_dir() else []
        for path in candidates:
            if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES and path not in seen:
                seen.add(path)
                yield path


def scan_type_escapes(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern, message in TYPE_ESCAPE_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(
                    rule_id="CQG-TYPE-001",
                    family="TYPE_ESCAPES",
                    path=str(path),
                    line=lineno,
                    message=message,
                    severity="MEDIUM",
                    confidence=0.78 if "Possible" in message else 0.92,
                ))
    return findings


def _max_if_depth(node: ast.AST, depth: int = 0) -> tuple[int, int | None]:
    best_depth = depth
    best_line = getattr(node, "lineno", None)
    for child in ast.iter_child_nodes(node):
        next_depth = depth + 1 if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.Match)) else depth
        child_depth, child_line = _max_if_depth(child, next_depth)
        if child_depth > best_depth:
            best_depth, best_line = child_depth, child_line
    return best_depth, best_line


def scan_python(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            broad = node.type is None or (
                isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}
            )
            if broad:
                findings.append(Finding(
                    rule_id="CQG-DEF-001",
                    family="DEFENSIVE_OVERGROWTH",
                    path=str(path),
                    line=node.lineno,
                    message="Broad exception handler requires contextual justification",
                    severity="MEDIUM",
                    confidence=0.94,
                ))
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                findings.append(Finding(
                    rule_id="CQG-DEF-002",
                    family="DEFENSIVE_OVERGROWTH",
                    path=str(path),
                    line=node.lineno,
                    message="Exception is silently swallowed with `pass`",
                    severity="HIGH",
                    confidence=0.99,
                ))

    depth, line = _max_if_depth(tree)
    if depth >= 4 and line is not None:
        findings.append(Finding(
            rule_id="CQG-NEST-001",
            family="NESTING_CONTROL_FLOW",
            path=str(path),
            line=line,
            message=f"Control-flow nesting depth reached {depth}; inspect for early-return or decomposition opportunity",
            severity="MEDIUM",
            confidence=0.75,
        ))

    return findings


def scan_file(path: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return []
    findings = scan_type_escapes(path, text)
    if path.suffix.lower() == ".py":
        findings.extend(scan_python(path, text))
    return findings


def verdict_for(findings: list[Finding]) -> str:
    if any(item.severity in {"HIGH", "BLOCKER"} for item in findings):
        return "REPAIR_REQUIRED"
    if any(item.severity == "MEDIUM" for item in findings):
        return "REPAIR_REQUIRED"
    if findings:
        return "PASS_WITH_DEBT"
    return "PASS"


def build_report(targets: list[str]) -> dict:
    findings: list[Finding] = []
    scanned_files = 0
    for path in iter_source_files(targets):
        scanned_files += 1
        findings.extend(scan_file(path))

    return {
        "version": "0.1.0",
        "scanner": "mindway-reference-deterministic-hints",
        "targets": targets,
        "scanned_files": scanned_files,
        "verdict": verdict_for(findings),
        "findings": [asdict(item) for item in findings],
        "limitations": [
            "A PASS is not REVIEW_READY.",
            "Subjective rules require contextual review.",
            "Security and project invariants override cleanup suggestions.",
            "Run project lint, typecheck, tests, and security checks separately."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Mindway deterministic code-quality hint scanner")
    parser.add_argument("targets", nargs="+", help="Files or directories to scan")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()
    report = build_report(args.targets)
    print(json.dumps(report, indent=2 if args.pretty else None, sort_keys=args.pretty))
    return 1 if report["verdict"] == "REPAIR_REQUIRED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
