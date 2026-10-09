"""TOY_ONLY finite symbolic slots; NOT physical video or learned perception; no I/O."""
from itertools import product
from collections import Counter

TRUE, FALSE, UNKNOWN = "TRUE", "FALSE", "UNKNOWN"


class ToyError(ValueError):
    pass


def check_view(view):
    if not isinstance(view, (tuple, list)) or not 2 <= len(view) <= 4:
        raise ToyError("TWO_TO_FOUR_SLOTS_REQUIRED")
    if any(v is not None and (type(v) is not int or v not in (0, 1)) for v in view):
        raise ToyError("INVALID_OBSERVATION")


def consistent_worlds(view):
    """Known bits are assumed perfectly sound and complete for their finite slot."""
    check_view(view)
    return tuple(w for w in product((0, 1), repeat=len(view))
                 if all(v is None or v == w[i] for i, v in enumerate(view)))


def never(world):
    return not any(world)


def certify_never(view):
    values = {never(w) for w in consistent_worlds(view)}
    return TRUE if values == {True} else FALSE if values == {False} else UNKNOWN


def naive_never(view):
    """Deliberately UNSOUND baseline: substitutes zero for unknown slots."""
    check_view(view)
    return not any(v if v is not None else 0 for v in view)


def audit_small_worlds():
    counts = Counter()
    for n in range(2, 5):
        for view in product((None, 0, 1), repeat=n):
            result = certify_never(view)
            counts["views"] += 1
            counts[result] += 1
            for world in consistent_worlds(view):
                counts["world_view_pairs"] += 1
                counts["monitor_false_true"] += int(result == TRUE and not never(world))
                counts["monitor_false_false"] += int(result == FALSE and never(world))
                counts["naive_false_true"] += int(naive_never(view) and not never(world))
    counts["always_unknown_determinate"] = 0
    return dict(counts)


def retract(dependencies, invalid):
    """Classical AND-dependency cone; does not learn dependencies or contradictions."""
    affected = set(invalid)
    changed = True
    while changed:
        changed = False
        for claim, requirements in dependencies.items():
            if claim not in affected and set(requirements) & affected:
                affected.add(claim)
                changed = True
    return frozenset(affected & set(dependencies))


def cache_baseline(dependencies, invalid):
    """Independent reachability expression of ordinary dependency invalidation."""
    def reaches(node, path):
        if node in invalid:
            return True
        if node in path:
            raise ToyError("CYCLIC_CACHE_GRAPH")
        return any(reaches(d, path | {node}) for d in dependencies.get(node, ()))
    return frozenset(c for c in dependencies if reaches(c, set()))


def observe(worlds, index, value):
    if not worlds or any(len(w) != len(worlds[0]) for w in worlds):
        raise ToyError("WORLD_SET_INVALID")
    if type(index) is not int or not 0 <= index < len(worlds[0]):
        raise ToyError("OBSERVATION_INDEX_INVALID")
    if value is None:
        return tuple(worlds)
    if type(value) is not int or value not in (0, 1):
        raise ToyError("OBSERVATION_VALUE_INVALID")
    return tuple(w for w in worlds if w[index] == value)


def answer_set(worlds):
    if not worlds:
        raise ToyError("NO_CONSISTENT_WORLD")
    return frozenset("NEVER" if never(w) else "SOME" for w in worlds)


def separates_answers(worlds, index):
    """Every possible perfect bit outcome must leave only one target answer."""
    if len(answer_set(worlds)) <= 1:
        return False
    partitions = [observe(worlds, index, v) for v in (0, 1)]
    return all(len(answer_set(p)) == 1 for p in partitions if p)
