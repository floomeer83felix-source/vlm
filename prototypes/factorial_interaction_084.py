"""One four-logit interaction diagnostic, with synthetic scorers only.

R reindexes stored units; it is not raw-video reversal. tau swaps the current
structured question. No text encoder/parser, learned model, data I/O or training
is implemented. Synthetic event labels and badges are oracle fixture fields.
"""
from dataclasses import dataclass
import math

# Predeclared fixture error bound for moderate scores, not an inference threshold.
FIXTURE_ABS_TOL = 1e-10


@dataclass(frozen=True)
class Unit:
    event: str
    badge: float


@dataclass(frozen=True)
class Question:
    first: str
    second: str

    def __post_init__(self):
        if not self.first or not self.second or self.first == self.second:
            raise ValueError("two distinct event names are required")


def reverse_units(video):
    """Reverse a tuple of existing units without recomputing their contents."""
    return tuple(reversed(video))


def swap_roles(question):
    return Question(question.second, question.first)


def four_logits(scorer, video, question):
    """Four fresh scalar evaluations; callers must supply pre-threshold logits.

    Float type/finite checks cannot establish a caller's logit provenance. A
    float-cast binary prediction is still forbidden by the diagnostic contract.
    No sharing with another example's predictions or labels occurs here.
    """
    rv, tq = reverse_units(video), swap_roles(question)
    values = tuple(scorer(v, q) for v, q in
                   ((video, question), (video, tq), (rv, question), (rv, tq)))
    if any(type(x) is not float for x in values):
        raise TypeError("scorer must return floating scalar logits, not decisions")
    if not all(math.isfinite(x) for x in values):
        raise ValueError("nonfinite scalar logit")
    return values


def interaction(scorer, video, question):
    a, b, c, d = four_logits(scorer, video, question)
    result = math.fsum((a, -b, -c, d))
    if not math.isfinite(result):
        raise ValueError("nonfinite interaction")
    return result


def role_code(question):
    """Lexical fixture code, deliberately not a semantic event representation."""
    return 1.0 if question.first < question.second else -1.0


def order_code(video):
    """Synthetic two-event oracle code; never offered as a real feature reader."""
    names = [unit.event for unit in video]
    if len(names) != 2 or sorted(names) != ["A", "B"]:
        raise ValueError("fixture requires exactly one A and one B")
    return 1.0 if names == ["A", "B"] else -1.0


def additive_scorer(video, question):
    # a(V) need not itself be reversal-invariant; it still cancels in I.
    return 1.25 * order_code(video) + 2.5 * role_code(question) + 3.0


def multiplicative_scorer(video, question):
    return order_code(video) * role_code(question)


def shortcut_scorer(video, question):
    """Reads ordered static badges and lexical roles; ignores event identities."""
    return (video[0].badge - video[-1].badge) * role_code(question)


def fixture_truth(video, question):
    """Fixture oracle for testing a counterexample, not a deployed input."""
    names = [unit.event for unit in video]
    if names.count(question.first) != 1 or names.count(question.second) != 1:
        raise ValueError("fixture events must occur exactly once")
    return names.index(question.first) < names.index(question.second)


def fixtures():
    # The same badge layout occurs with opposite event meanings. No random data
    # generation, labels from a research cache, optimizer or fit is involved.
    return ((Unit("A", 1.0), Unit("B", -1.0)),
            (Unit("B", 1.0), Unit("A", -1.0))), Question("A", "B")
