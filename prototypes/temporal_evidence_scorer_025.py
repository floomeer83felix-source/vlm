"""025 separate, one-shot final CPU scoring interface; no import-time work.

This is a logical contract only. The future trusted supervisor must enforce
real child exits, gold-denied generation and durable no-retry bookkeeping.
A caller-created receipt or a new scorer instance cannot establish OS safety.
025 injects invented in-memory streams, never real annotations or predictions.
"""

from dataclasses import dataclass, field
from itertools import combinations

from temporal_evidence_adapter_025 import (
    ARMS, Call, ContractError, FrozenPlan, PlanQuestion, QuestionKey,
    ProjectionError, SourceRecord, decompose,
    _Projector, _calls, _check_batch, _question_path,
    STRICT_025, container_binding,
)


@dataclass(frozen=True)
class TerminalAttempt:
    call: Call
    state: str
    prediction: object = field(default=None, repr=False)


@dataclass(frozen=True)
class FrozenLedger:
    attempts: tuple
    frozen: bool


@dataclass(frozen=True)
class ChildExitReceipt:
    launched: tuple = field(repr=False)
    exited: tuple = field(repr=False)
    queue_closed: bool


@dataclass(frozen=True)
class ArmScore:
    arm: str
    correct_known: int
    invalid: int
    failed: int
    not_run: int
    accuracy: object


@dataclass(frozen=True)
class PairScore:
    left: str
    right: str
    both_correct: int
    left_only: int
    right_only: int
    both_wrong: int


@dataclass(frozen=True)
class ScoreReport:
    status: str
    reason: str
    n_planned: int
    n_valid_gold: int
    n_bad_gold: int
    arms: tuple
    paired: object
    by_source: tuple = ()


@dataclass(frozen=True)
class SourceScore:
    source: str = field(repr=False)
    report: ScoreReport


def _prediction(value):
    if type(value) is str and value.strip() in ARMS + ("E",):
        return value.strip()
    return None


def _canonical_gold(value):
    if type(value) is str and value.strip().upper() in ARMS + ("E",):
        return value.strip().upper()
    return None


def _gate(plan, ledger, receipt):
    if (type(plan) is not FrozenPlan or type(plan.questions) is not tuple
            or type(plan.calls) is not tuple or not plan.questions
            or any(type(q) is not PlanQuestion for q in plan.questions)
            or type(plan.sources) is not tuple
            or any(type(s) is not SourceRecord or type(s.metadata) is not tuple
                   for s in plan.sources)):
        raise ContractError("INVALID_FROZEN_PLAN")
    _check_batch(tuple(q.key for q in plan.questions))
    if (plan.calls != _calls(plan.questions)
            or any(q.decomposition != decompose(q.task, q.question)
                   or q.decomposition.status != "OK" for q in plan.questions)
            or len({s.source for s in plan.sources}) != len(plan.sources)
            or any(q.key.source not in {s.source for s in plan.sources}
                   for q in plan.questions)):
        raise ContractError("INVALID_FROZEN_PLAN")
    if (type(ledger) is not FrozenLedger or ledger.frozen is not True
            or type(ledger.attempts) is not tuple
            or len(ledger.attempts) != len(plan.calls)):
        raise ContractError("FROZEN_COMPLETE_LEDGER_REQUIRED")
    terminal = ("RETURNED", "INVALID", "FAILED", "NOT_RUN")
    for item in ledger.attempts:
        if (type(item) is not TerminalAttempt or item.state not in terminal
                or type(item.call) is not Call
                or type(item.call.key) is not QuestionKey
                or type(item.call.key.source) is not str
                or type(item.call.key.index) is not int
                or item.call.arm not in ARMS):
            raise ContractError("ALL_CALLS_MUST_BE_TERMINAL")
        if item.state == "NOT_RUN" and item.prediction is not None:
            raise ContractError("NOT_RUN_CANNOT_HAVE_PREDICTION")
    if (len({item.call for item in ledger.attempts}) != len(plan.calls)
            or {item.call for item in ledger.attempts} != set(plan.calls)):
        raise ContractError("EXACT_PLANNED_CALLS_REQUIRED")
    if (type(receipt) is not ChildExitReceipt or receipt.queue_closed is not True
            or type(receipt.launched) is not tuple or type(receipt.exited) is not tuple
            or not receipt.launched
            or any(type(x) is not str or not x for x in receipt.launched + receipt.exited)
            or len(set(receipt.launched)) != len(receipt.launched)
            or len(set(receipt.exited)) != len(receipt.exited)
            or set(receipt.launched) != set(receipt.exited)):
        raise ContractError("CLOSED_QUEUE_AND_ALL_CHILD_EXITS_REQUIRED")


def _report(plan, ledger, labels, reason, include_sources=True):
    keys = tuple(q.key for q in plan.questions)
    n = len(keys)
    gold = {key: _canonical_gold(labels.get(key)) for key in keys}
    valid = sum(value is not None for value in gold.values())
    good = {}
    arms = []
    for arm in ARMS:
        rows = tuple(item for item in ledger.attempts if item.call.arm == arm)
        invalid = failed = not_run = 0
        for item in rows:
            label = _prediction(item.prediction) if item.state == "RETURNED" else None
            invalid += item.state == "INVALID" or (item.state == "RETURNED" and label is None)
            failed += item.state == "FAILED"
            not_run += item.state == "NOT_RUN"
            good[(item.call.key, arm)] = (gold[item.call.key] is not None
                                          and label is not None
                                          and label == gold[item.call.key])
        correct = sum(good[(key, arm)] for key in keys)
        arms.append(ArmScore(arm, correct, invalid, failed, not_run,
                             correct / n if valid == n else None))
    pairs = None
    if valid == n:
        tables = []
        for left, right in combinations(ARMS, 2):
            cells = [0, 0, 0, 0]
            for key in keys:
                lgood, rgood = good[(key, left)], good[(key, right)]
                cells[0 if lgood and rgood else 1 if lgood else 2 if rgood else 3] += 1
            tables.append(PairScore(left, right, *cells))
        pairs = tuple(tables)
    sources = []
    if include_sources:
        for source in plan.sources:
            questions = tuple(q for q in plan.questions if q.key.source == source.source)
            if not questions:
                continue
            subplan = FrozenPlan((source,), questions, (), _calls(questions))
            subledger = FrozenLedger(tuple(row for row in ledger.attempts
                                          if row.call.key.source == source.source), True)
            sources.append(SourceScore(source.source,
                                       _report(subplan, subledger, labels, reason, False)))
    return ScoreReport("PASS" if valid == n else "GOLD_SCHEMA_HOLD",
                       reason if reason else "VALID_BATCH" if valid == n else "BAD_OR_MISSING_GOLD",
                       n, valid, n - valid, tuple(arms), pairs, tuple(sources))


class OneShotScorer:
    """Consumes once per instance, before opening; no persistence/OS claims."""

    def __init__(self):
        self._consumed = False

    def score(self, opener, plan, ledger, receipt, *, profile=STRICT_025,
              expected_binding=None, diagnostic=None):
        if self._consumed:
            raise ContractError("SCORER_ALREADY_CONSUMED")
        _gate(plan, ledger, receipt)
        self._consumed = True
        binding = container_binding(profile)
        if (expected_binding is not None and tuple(expected_binding) != binding
                or profile != STRICT_025 and expected_binding is None):
            raise ContractError("SCORING_CONTAINER_BINDING_HOLD")
        batch = set(q.key for q in plan.questions)

        def allow(path):
            return (_question_path(path) and QuestionKey(path[0], path[2]) in batch
                    and path[3] == "correct_answer_label")

        stream, data, failure = None, {}, ""
        try:
            stream = opener()
            data = _Projector(stream, allow, profile=profile, diagnostic=diagnostic).read()
        except ProjectionError:
            # No partial gold is scored after a parser failure. All N are then
            # unusable/unverified, not claimed to have individually bad labels.
            failure = "PARSER_HOLD"
        except Exception:
            failure = "STREAM_OPEN_OR_READ_FAILED"
        finally:
            if stream is not None:
                try:
                    stream.close()
                except Exception:
                    failure = "STREAM_CLOSE_FAILED"
        if failure:
            return _report(plan, ledger, {}, failure)
        labels = {}
        for key in batch:
            node = data.get(key.source, {}).get("benchmark_dataset", {}).get(key.index, {})
            if "correct_answer_label" in node:
                labels[key] = node["correct_answer_label"]
        return _report(plan, ledger, labels, "")
