"""TOY ONLY, NOT FOR REAL DATA OR MODEL USE. Standard library; no I/O."""
from dataclasses import dataclass
from fractions import Fraction
from collections import Counter


class ContractError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def require(condition, code):
    if not condition:
        raise ContractError(code)


def rational(value):
    require(not isinstance(value, (float, bool)) and value is not None,
            "RATIONAL_TIME_REQUIRED")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError):
        raise ContractError("RATIONAL_TIME_REQUIRED") from None


@dataclass(frozen=True)
class Frame:
    index: int
    pts: int
    time_base: Fraction
    version: str = "toy-media-v1"
    rgb: str = "toy-rgb"
    size: tuple = (16, 16)
    preprocessing: str = "toy-fixed"

    @property
    def key(self):
        return self.version, self.index


def timeline(frames, origin, parent_offset, scale):
    origin, parent_offset, scale = map(rational, (origin, parent_offset, scale))
    require(scale > 0, "NONPOSITIVE_SCALE")
    result, seen = [], set()
    for frame in frames:
        require(isinstance(frame.version, str) and frame.version.startswith("toy-"),
                "MEDIA_VERSION_UNKNOWN")
        require(type(frame.index) is int and frame.index >= 0, "INVALID_FRAME_INDEX")
        require(frame.key not in seen, "DUPLICATE_SOURCE_FRAME")
        require(type(frame.pts) is int, "FRAME_PTS_REQUIRED")
        base = rational(frame.time_base)
        require(base > 0, "NONPOSITIVE_TIME_BASE")
        time = parent_offset + scale * (frame.pts * base - origin)
        require(not result or time > result[-1], "NONMONOTONIC_PTS")
        result.append(time)
        seen.add(frame.key)
    return result


def inside(time, interval):
    require(isinstance(interval, (tuple, list)) and len(interval) == 3, "INVALID_INTERVAL")
    lo, hi, semantics = interval
    lo, hi = rational(lo), rational(hi)
    require(lo < hi and semantics in ("closed", "half-open"), "INVALID_INTERVAL")
    return lo <= time <= hi if semantics == "closed" else lo <= time < hi


def validate_reference_intervals(intervals):
    require(isinstance(intervals, (tuple, list)) and len(intervals) >= 3,
            "AT_LEAST_THREE_REFERENCE_INTERVALS")
    result = []
    for item in intervals:
        require(isinstance(item, (tuple, list)) and len(item) == 3,
                "INVALID_REFERENCE_INTERVAL")
        try:
            lo, hi = rational(item[0]), rational(item[1])
        except ContractError:
            raise ContractError("INVALID_REFERENCE_ENDPOINT") from None
        require(lo < hi and item[2] in ("closed", "half-open"),
                "INVALID_REFERENCE_INTERVAL")
        if result:
            previous_lo, previous_hi, previous_kind = result[-1]
            require(lo >= previous_lo, "REFERENCE_INTERVALS_UNORDERED")
            require(lo > previous_hi or (lo == previous_hi and previous_kind == "half-open"),
                    "REFERENCE_INTERVALS_OVERLAP")
        result.append((lo, hi, item[2]))
    return tuple(result)


@dataclass(frozen=True)
class Source:
    name: str
    typed_id: tuple = None
    content_alias: str = None
    verified_parent: str = None
    protected: bool = False
    coverage_known: bool = True


def source_groups(sources, potential_edges=()):
    nodes = {s.name: s for s in sources}
    require(len(nodes) == len(sources), "DUPLICATE_SOURCE_NODE")
    require(all(n.startswith("toy-") for n in nodes), "TOY_NAMESPACE_REQUIRED")
    parent = {n: n for n in nodes}
    def find(n):
        while parent[n] != n:
            n = parent[n]
        return n
    def union(a, b):
        require(a in nodes and b in nodes, "SOURCE_EDGE_UNKNOWN")
        a, b = find(a), find(b)
        parent[max(a, b)] = min(a, b)
    aliases, typed = {}, {}
    for s in sources:
        if s.typed_id is not None:
            require(isinstance(s.typed_id, tuple) and len(s.typed_id) == 3 and
                    all(isinstance(v, str) and v for v in s.typed_id), "INVALID_TYPED_ID")
            union(s.name, typed.setdefault(s.typed_id, s.name))
        if s.content_alias:
            union(s.name, aliases.setdefault(s.content_alias, s.name))
        if s.verified_parent:
            union(s.name, s.verified_parent)
    for a, b in potential_edges:
        union(a, b)
    groups = {}
    for n in sorted(nodes):
        groups.setdefault(find(n), []).append(n)
    result = []
    for members in groups.values():
        status = ("BLOCKED" if any(nodes[n].protected for n in members) else
                  "UNKNOWN" if any(nodes[n].typed_id is None or
                                   not nodes[n].coverage_known for n in members) else
                  "ELIGIBLE_TOY_ONLY")
        result.append({"members": members, "status": status,
                       "real_event_independence": "UNKNOWN"})
    return result


def pair_contract(d1, d2, anchors, intervals, origin, parent_offset, scale,
                  guard, time_bins=None, toy_token_counts=None):
    require(len(d1) == len(d2) == 12, "TWELVE_FRAMES_REQUIRED")
    intervals = validate_reference_intervals(intervals)
    t1 = timeline(d1, origin, parent_offset, scale)
    t2 = timeline(d2, origin, parent_offset, scale)
    require(len({f.version for f in d1 + d2}) == 1, "MEDIA_VERSION_MISMATCH")
    maps = [{f.key: (f, t) for f, t in zip(fs, ts)} for fs, ts in ((d1, t1), (d2, t2))]
    anchor_set = set(anchors)
    require(0 < len(anchor_set) == len(anchors) < 12, "ANCHOR_SET_INVALID")
    require(all(k in m for m in maps for k in anchors), "ANCHOR_MISSING")
    require(all(maps[0][k] == maps[1][k] for k in anchors), "ANCHOR_IDENTITY_MISMATCH")
    require(intervals and all(any(inside(maps[0][k][1], i) for k in anchors)
                              for i in intervals), "REFERENCE_UNCOVERED")
    require(all(any(inside(maps[0][k][1], i) for i in intervals) for k in anchors),
            "ANCHOR_OUTSIDE_REFERENCE")
    guard = rational(guard)
    require(guard >= 0, "NEGATIVE_GUARD")
    for mapping in maps:
        for key, (_, time) in mapping.items():
            if key not in anchor_set:
                require(all(not (rational(lo)-guard <= time <= rational(hi)+guard)
                            for lo, hi, _ in intervals), "BACKGROUND_IN_GUARD")
    require(all(isinstance(f.rgb, str) and f.rgb and isinstance(f.size, tuple) and
                len(f.size) == 2 and all(type(v) is int and v > 0 for v in f.size) and
                isinstance(f.preprocessing, str) and f.preprocessing
                for f in d1 + d2), "FRAME_GEOMETRY_UNKNOWN")
    require(len({(f.size, f.preprocessing) for f in d1 + d2}) == 1,
            "PREPROCESS_MISMATCH")
    warnings = ["TOKEN_BUDGET_UNKNOWN"]  # Toy integers never certify real processor tokens.
    if toy_token_counts is not None:
        require(len(toy_token_counts) == 2 and all(type(v) is int and v > 0
                                                 for v in toy_token_counts), "TOKEN_COUNTS_INVALID")
        require(toy_token_counts[0] == toy_token_counts[1], "TOKEN_BUDGET_MISMATCH")
    if time_bins is None:
        warnings.append("TEMPORAL_MATCH_UNVERIFIED")
    else:
        edges = list(map(rational, time_bins))
        require(len(edges) >= 2 and all(a < b for a, b in zip(edges, edges[1:])),
                "TIME_BINS_INVALID")
        def histogram(times):
            counts = Counter()
            for t in times:
                hit = [j for j, (a, b) in enumerate(zip(edges, edges[1:])) if a <= t < b]
                require(len(hit) == 1, "TIME_OUTSIDE_BINS")
                counts[hit[0]] += 1
            return counts
        require(histogram(t1) == histogram(t2), "TEMPORAL_MATCH_MISMATCH")
        if t1 != t2:
            warnings.append("TEMPORAL_FINE_MATCH_UNVERIFIED")
    return {"structural": "PASS_TOY_ONLY", "fairness": "UNKNOWN",
            "warnings": warnings, "real_G1": "HOLD", "semantic_sufficiency": "UNKNOWN"}
