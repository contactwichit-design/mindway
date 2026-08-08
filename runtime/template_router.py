#!/usr/bin/env python3
"""Mindway Universal Template Router.

Provider-agnostic deterministic helper. It accepts behavior tags rather than trying to
replace model judgment with brittle natural-language classification.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TAG_TO_FAMILY = {
    "define":"T01", "task":"T01", "scope":"T01",
    "research":"T02", "discover":"T02", "compare_sources":"T02",
    "plan":"T03", "sequence":"T03", "decompose":"T03",
    "decide":"T04", "recommend":"T04", "approve":"T04",
    "status":"T05", "routine":"T05", "progress":"T05",
    "handoff":"T06", "checkpoint":"T06", "resume":"T06",
    "qa":"T07", "review":"T07", "test":"T07", "regression":"T07",
    "data":"T08", "analyze":"T08", "kpi":"T08",
    "communicate":"T09", "email":"T09", "line":"T09", "announcement":"T09",
    "document":"T10", "sop":"T10", "report":"T10", "proposal":"T10",
    "visual":"T11", "graphic":"T11", "diagram":"T11", "poster":"T11",
    "presentation":"T12", "slides":"T12", "deck":"T12",
    "web":"T13", "ui":"T13", "dashboard":"T13", "app":"T13",
    "learning":"T14", "lms":"T14", "lesson":"T14", "quiz":"T14",
    "media":"T15", "video":"T15", "audio":"T15", "subtitle":"T15", "motion":"T15",
    "automation":"T16", "agent":"T16", "trigger":"T16", "recurring":"T16",
    "blocked":"T17", "recover":"T17", "fallback":"T17",
    "evolve":"T18", "skill":"T18", "maintenance":"T18", "benchmark":"T18",
}

RECIPES = {
    "approval_memo":["T01","T09","T10","T07"],
    "research_report":["T01","T02","T10","T07"],
    "project_plan":["T01","T03","T17","T07"],
    "decision_support":["T01","T02","T04","T07"],
    "routine_status":["T01","T05","T17","T07"],
    "handoff":["T01","T06","T07"],
    "data_dashboard":["T01","T08","T04","T13","T07"],
    "graphic":["T01","T11","T07"],
    "presentation":["T01","T12","T11","T07"],
    "web_product":["T01","T13","T07","T06"],
    "lms_lesson":["T01","T14","T15","T11","T07","T06"],
    "video":["T01","T15","T11","T07"],
    "automation":["T01","T16","T05","T17","T07"],
    "skill_evolution":["T01","T18","T07","T06"],
}

ORDER = [f"T{i:02d}" for i in range(1, 19)]


def route(tags=None, recipe=None):
    if recipe:
        if recipe not in RECIPES:
            raise ValueError(f"Unknown recipe: {recipe}")
        families = RECIPES[recipe]
    else:
        tags = tags or []
        unknown = [t for t in tags if t not in TAG_TO_FAMILY]
        if unknown:
            raise ValueError("Unknown behavior tags: " + ", ".join(unknown))
        families = [TAG_TO_FAMILY[t] for t in tags]
    unique = []
    for fam in families:
        if fam not in unique:
            unique.append(fam)
    return sorted(unique, key=ORDER.index)


def self_test():
    cases = {
        "approval_memo":["T01","T07","T09","T10"],
        "lms_lesson":["T01","T06","T07","T11","T14","T15"],
        "automation":["T01","T05","T07","T16","T17"],
    }
    for recipe, expected in cases.items():
        got = route(recipe=recipe)
        assert got == expected, (recipe, got, expected)
    assert route(tags=["data","recommend","dashboard","qa"]) == ["T04","T07","T08","T13"]
    assert route(tags=["blocked","research"]) == ["T02","T17"]
    return {"status":"PASS","tests":5}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--recipe", choices=sorted(RECIPES))
    p.add_argument("--tags", nargs="*", default=[])
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    result = self_test() if args.self_test else {"families": route(args.tags, args.recipe)}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
