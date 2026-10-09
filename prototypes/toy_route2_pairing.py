"""TOY_ONLY: standard-library paired arithmetic, NOT real data/model use; no I/O."""
from dataclasses import dataclass
from fractions import Fraction
from collections import Counter

ARMS = ("S_q", "S_t")
STATUSES = ("ok", "failed", "invalid", "not_started", "construction_failed")


class PairingError(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise PairingError(code)


@dataclass(frozen=True)
class Outcome:
    group: str
    question: str
    arm: str
    score: int
    status: str = "ok"


def estimate(planned, outcomes):
    """Missing rows are errors; explicit failures stay as zero in frozen denominator."""
    require(planned, "EMPTY_DENOMINATOR")
    plan, question_owner = set(), {}
    for pair in planned:
        require(isinstance(pair, (tuple, list)) and len(pair) == 2, "INVALID_PLAN_PAIR")
        group, question = pair
        require(all(isinstance(x, str) and x.startswith("toy-") for x in pair),
                "TOY_NAMESPACE_REQUIRED")
        require((group, question) not in plan, "DUPLICATE_PLANNED_PAIR")
        require(question not in question_owner or question_owner[question] == group,
                "QUESTION_CROSSES_GROUPS")
        plan.add((group, question))
        question_owner[question] = group
    rows, statuses = {}, Counter()
    for row in outcomes:
        require((row.group, row.question) in plan, "UNPLANNED_PAIR")
        require(row.arm in ARMS, "UNKNOWN_ARM")
        require(type(row.score) is int and row.score in (0, 1), "INVALID_BINARY_SCORE")
        require(row.status in STATUSES, "UNKNOWN_STATUS")
        require(row.status == "ok" or row.score == 0, "FAILURE_MUST_SCORE_ZERO")
        key = (row.group, row.question, row.arm)
        require(key not in rows, "DUPLICATE_GROUP_QUESTION_ARM")
        rows[key] = row.score
        statuses[(row.arm, row.status)] += 1
    expected = {(g, q, a) for g, q in plan for a in ARMS}
    require(set(rows) == expected, "MISSING_ARM")
    grouped, cells = {}, Counter()
    for group, question in sorted(plan):
        q = rows[(group, question, "S_q")]
        t = rows[(group, question, "S_t")]
        gain, harm = int(t == 0 and q == 1), int(t == 1 and q == 0)
        cells[(t, q)] += 1
        grouped.setdefault(group, []).append((q-t, gain, harm))
    stats = {}
    for group, values in grouped.items():
        n = len(values)
        stats[group] = {
            "questions": n, "delta": Fraction(sum(v[0] for v in values), n),
            "gain_rate": Fraction(sum(v[1] for v in values), n),
            "harm_rate": Fraction(sum(v[2] for v in values), n)}
    groups, pairs = len(stats), len(plan)
    delta = sum((s["delta"] for s in stats.values()), Fraction(0)) / groups
    gain = sum((s["gain_rate"] for s in stats.values()), Fraction(0)) / groups
    harm = sum((s["harm_rate"] for s in stats.values()), Fraction(0)) / groups
    require(delta == gain-harm, "INTERNAL_IDENTITY_FAILURE")
    return {"group_n": groups, "pair_n": pairs, "delta": delta,
            "group_gain_rate": gain, "group_harm_rate": harm,
            "gains": cells[(0, 1)], "harms": cells[(1, 0)],
            "stable_wrong": cells[(0, 0)], "stable_correct": cells[(1, 1)],
            "question_delta": Fraction(cells[(0, 1)]-cells[(1, 0)], pairs),
            "group_statistics": stats, "status_counts": dict(statuses),
            "real_source_independence": "UNKNOWN", "NG_data_gate": "HOLD"}
