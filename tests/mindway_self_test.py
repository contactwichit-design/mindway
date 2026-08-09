#!/usr/bin/env python3
"""Deterministic Mindway architecture/regression self-test.

This suite validates repository contracts and behavioral state-machine invariants.
It does not claim to test external AI providers or live network transports.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def decide_entry(routes, refs_ok=True, remembered=False):
    """routes: ordered iterable of (available, result) where result is verified|failed|unverified."""
    for available, result in routes:
        if not available:
            continue
        if result == "verified":
            return "MINDWAY_LOADED" if refs_ok else "MINDWAY_BLOCKED"
    return "MINDWAY_BLOCKED"


def can_do_substantial(entry_state):
    return entry_state == "MINDWAY_LOADED"


def main():
    failures = []

    required_files = [
        "BOOTSTRAP.md", "my.md", "README.md", "PUBLIC_STANDARD.md",
        "ARCHITECTURE.md", "INVARIANTS.md",
        "skills/entry-access-gate/SKILL.md",
        "skills/capability-negotiation/SKILL.md",
        "tests/REGRESSION_CASES.md",
    ]
    for rel in required_files:
        if not (ROOT / rel).exists():
            failures.append(f"missing:{rel}")

    if failures:
        print("FAIL", *failures, sep="\n")
        return 1

    bootstrap = read("BOOTSTRAP.md")
    my = read("my.md")
    arch = read("ARCHITECTURE.md")
    inv = read("INVARIANTS.md")
    gate = read("skills/entry-access-gate/SKILL.md")

    required_strings = {
        "BOOTSTRAP.md": ["MW-BOOT/1", "NO VERIFIED /my = NO SUBSTANTIAL EXECUTION"],
        "my.md": ["BOOTSTRAP.md", "README.md", "PUBLIC_STANDARD.md", "Entry Access Gate"],
        "ARCHITECTURE.md": ["MW-BOOT/1", "/my", "/loop", "INVARIANTS.md"],
        "INVARIANTS.md": ["INV-001", "INV-002", "INV-003", "INV-004", "INV-005"],
        "entry gate": ["NO VERIFIED /my = NO SUBSTANTIAL EXECUTION", "MINDWAY_BLOCKED"],
    }
    docs = {"BOOTSTRAP.md": bootstrap, "my.md": my, "ARCHITECTURE.md": arch, "INVARIANTS.md": inv, "entry gate": gate}
    for name, needles in required_strings.items():
        for needle in needles:
            if needle not in docs[name]:
                failures.append(f"contract:{name}:{needle}")

    # Deterministic behavioral regression cases.
    cases = [
        ([(True, "verified")], True, "MINDWAY_LOADED"),
        ([(True, "failed"), (True, "verified")], True, "MINDWAY_LOADED"),
        ([(False, "failed"), (True, "verified")], True, "MINDWAY_LOADED"),
        ([(True, "unverified"), (True, "verified")], True, "MINDWAY_LOADED"),
        ([(True, "failed"), (True, "failed")], True, "MINDWAY_BLOCKED"),
        ([(True, "verified")], False, "MINDWAY_BLOCKED"),
    ]
    for i, (routes, refs_ok, expected) in enumerate(cases, 1):
        got = decide_entry(routes, refs_ok=refs_ok)
        if got != expected:
            failures.append(f"behavior:{i}:{got}!={expected}")

    if can_do_substantial("MINDWAY_BLOCKED"):
        failures.append("anti-bypass:block-state-allows-work")
    if not can_do_substantial("MINDWAY_LOADED"):
        failures.append("anti-bypass:loaded-state-denies-work")

    if failures:
        print("MINDWAY_SELF_TEST=FAIL")
        for item in failures:
            print(item)
        return 1

    print("MINDWAY_SELF_TEST=PASS")
    print(f"files_checked={len(required_files)}")
    print(f"behavior_cases={len(cases)}")
    print("scope=deterministic repository contracts; not live-provider testing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
