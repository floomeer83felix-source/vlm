"""OEP-12: pure, synthetic-only evidence selection under the 023 protocol.

Callers supply only integer toy IDs, relative PTS and three numeric score
vectors. There is no text, answer, feature, file, model or relation-truth input.
SUPPORTED means a score-qualified candidate pair exists, not that an event
identity, AB/BA proposition or causal claim has been verified.

The unordered ablation is frozen here as the earliest highest-scoring frame
for each event separately, subject to the same threshold, with deduplication
and identical question-score filling. It never imposes a pair order.
"""

from dataclasses import dataclass
import math
from typing import Optional, Tuple


CANDIDATES = 48
BUDGET = 12
TAU = 0.70  # Synthetic normalized scores only; not a real cosine calibration.


@dataclass(frozen=True)
class PairEvidence:
    first: int
    second: int
    score_sum: float


@dataclass(frozen=True)
class Selection:
    status: str
    reason: str
    policy: str
    indices: Tuple[int, ...] = ()
    ids: Tuple[int, ...] = ()
    pts: Tuple[float, ...] = ()
    anchors: Tuple[int, ...] = ()
    ab: Optional[PairEvidence] = None
    ba: Optional[PairEvidence] = None
    ab_status: str = "NOT_EVALUATED"
    ba_status: str = "NOT_EVALUATED"


def _number(value):
    # Exclude bools, strings, arbitrary objects and unbounded numeric coercions.
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _invalid(ids, pts, s_a, s_b, s_q, decomposable):
    if type(decomposable) is not bool:
        return "DECOMPOSABLE_BOOL_REQUIRED"
    for name, values in (("IDS", ids), ("PTS", pts), ("S_A", s_a),
                         ("S_B", s_b), ("S_Q", s_q)):
        # Bound access without consuming an arbitrary iterator or external data.
        if type(values) not in (list, tuple):
            return name + "_LIST_OR_TUPLE_REQUIRED"
        if len(values) != CANDIDATES:
            return name + "_LENGTH_MUST_BE_48"
    if any(type(value) is not int or value < 0 for value in ids):
        return "SYNTHETIC_NONNEGATIVE_INTEGER_IDS_REQUIRED"
    if len(set(ids)) != CANDIDATES:
        return "DUPLICATE_ID"
    if any(not _number(value) for value in pts):
        return "FINITE_PTS_REQUIRED"
    if any(pts[i] >= pts[i + 1] for i in range(CANDIDATES - 1)):
        return "PTS_MUST_BE_STRICTLY_INCREASING"
    for name, values in (("S_A", s_a), ("S_B", s_b), ("S_Q", s_q)):
        if any(not _number(value) or not 0 <= value <= 1 for value in values):
            return name + "_FINITE_UNIT_SCORES_REQUIRED"
    return None


def _hold(reason, policy):
    return Selection("HOLD", reason, policy)


def _top_indices(pts, s_q):
    return sorted(range(CANDIDATES), key=lambda i: (-s_q[i], pts[i], i))


def _finish(ids, pts, s_q, anchors, policy, reason, ab=None, ba=None,
            ab_status="NOT_EVALUATED", ba_status="NOT_EVALUATED"):
    anchor_set = set(anchors)
    chosen = set(anchor_set)
    for index in _top_indices(pts, s_q):
        if len(chosen) == BUDGET:
            break
        chosen.add(index)
    chronological = tuple(sorted(chosen))  # Validated strictly increasing PTS.
    return Selection(
        status="OK", reason=reason, policy=policy, indices=chronological,
        ids=tuple(ids[i] for i in chronological),
        pts=tuple(pts[i] for i in chronological),
        anchors=tuple(sorted(anchor_set)), ab=ab, ba=ba,
        ab_status=ab_status, ba_status=ba_status,
    )


def _best_ordered(first_scores, second_scores):
    # Lexicographic enumeration plus strict improvement freezes all sum ties.
    best = None
    for i in range(CANDIDATES):
        if first_scores[i] < TAU:
            continue
        for j in range(i + 1, CANDIDATES):
            if second_scores[j] < TAU:
                continue
            score = first_scores[i] + second_scores[j]
            if best is None or score > best.score_sum:
                best = PairEvidence(i, j, score)
    return best


def global_top12(ids, pts, s_a, s_b, s_q, decomposable=True):
    """Exact baseline, with the same complete input validation as both variants."""
    reason = _invalid(ids, pts, s_a, s_b, s_q, decomposable)
    if reason:
        return _hold(reason, "GLOBAL_TOP12")
    return _finish(ids, pts, s_q, (), "GLOBAL_TOP12", "BASELINE")


def oep12(ids, pts, s_a, s_b, s_q, decomposable=True):
    """Return bidirectional anchors plus Top12 fill, or an empty explicit HOLD.

    Exactly 48 candidates and budget 12; no configurable threshold/budget.
    No decomposition or no supported direction returns exactly baseline frames.
    Invalid inputs HOLD even when decomposition is unavailable; no silent repair.
    """
    reason = _invalid(ids, pts, s_a, s_b, s_q, decomposable)
    if reason:
        return _hold(reason, "ORDERED")
    if not decomposable:
        return _finish(ids, pts, s_q, (), "GLOBAL_TOP12", "NOT_DECOMPOSABLE")
    ab = _best_ordered(s_a, s_b)
    ba = _best_ordered(s_b, s_a)
    anchors = []
    for pair in (ab, ba):
        if pair is not None:
            anchors.extend((pair.first, pair.second))
    return _finish(
        ids, pts, s_q, anchors,
        "ORDERED" if anchors else "GLOBAL_TOP12",
        "SCORE_QUALIFIED_CANDIDATES_ONLY" if anchors else "NO_SUPPORTED_DIRECTION",
        ab=ab, ba=ba, ab_status="SUPPORTED" if ab else "UNSUPPORTED",
        ba_status="SUPPORTED" if ba else "UNSUPPORTED",
    )


def unordered12(ids, pts, s_a, s_b, s_q, decomposable=True):
    """Ablation: independent event maxima, no i<j relation or truth prediction.

    A frame may maximize both events and then occupies one anchor slot. A lone
    supported event may supply an anchor, but cannot certify a two-event pair.
    """
    reason = _invalid(ids, pts, s_a, s_b, s_q, decomposable)
    if reason:
        return _hold(reason, "UNORDERED")
    if not decomposable:
        return _finish(ids, pts, s_q, (), "GLOBAL_TOP12", "NOT_DECOMPOSABLE")
    anchors = []
    for scores in (s_a, s_b):
        best = min(range(CANDIDATES), key=lambda i: (-scores[i], pts[i], i))
        if scores[best] >= TAU:
            anchors.append(best)
    return _finish(
        ids, pts, s_q, anchors,
        "UNORDERED" if anchors else "GLOBAL_TOP12",
        "INDEPENDENT_EVENT_MAXIMA" if anchors else "NO_EVENT_ANCHOR",
    )
