"""Public, stdlib-only 025 interfaces; no files, models or live execution.

Streams are injected by a caller. This task uses invented StringIO fixtures
only. Source identifiers and text are deliberately omitted from dataclass reprs.
Neither grouping fields nor similarity ranks authenticate physical provenance
or event presence. Logical plans are not OS isolation or GPU supervision.
"""

from dataclasses import dataclass, field
import json
import math
import re


TASK = "perception/information_retrieval/temporal_distance"
MAX_BYTES = 64 * 1024 * 1024
MAX_DEPTH = 64
MAX_STRING_BYTES = 64 * 1024
ARMS = ("A", "B", "C", "D")
OPTIONS = tuple("answer_" + str(i) for i in range(1, 6))
META_FIELDS = (
    "video_source", "origin_video_id", "fb_participant_id", "release_1",
    "canonical_is_validated", "duration_in_seconds",
)
_SKIP = object()
_AUX = re.compile(r"\b(?:did|does|do|was|were|is|are)\b", re.I)
_MARKER = re.compile(r"\b(?:before|after|then|earlier|later)\b", re.I)


class ContractError(ValueError):
    """Only constant reason codes, never input values, belong in this error."""


class ProjectionError(ContractError):
    pass


class _Projector:
    """Incremental JSON validator/projector. Only admitted scalar values decode.

    Keys must decode to detect escaped duplicate keys, including in discarded
    objects. Skipped strings/numbers are validated character by character and
    never accumulated into scalar tokens or passed to the value decoder.
    Output arrays are sparse index dictionaries, preserving original indices.
    """

    def __init__(self, stream, allow, key_guard=None, *, max_bytes=MAX_BYTES,
                 max_depth=MAX_DEPTH, max_string_bytes=MAX_STRING_BYTES):
        for value, ceiling in ((max_bytes, MAX_BYTES), (max_depth, MAX_DEPTH),
                               (max_string_bytes, MAX_STRING_BYTES)):
            if type(value) is not int or not 1 <= value <= ceiling:
                raise ProjectionError("INVALID_PARSER_LIMIT")
        self.stream, self.allow, self.key_guard = stream, allow, key_guard
        self.max_bytes, self.max_depth = max_bytes, max_depth
        self.max_string_bytes = max_string_bytes
        self.buffer, self.position, self.byte_count = "", 0, 0

    def _peek(self):
        if self.position == len(self.buffer):
            request = min(4096, self.max_bytes - self.byte_count + 1)
            try:
                chunk = self.stream.read(request)
                if type(chunk) is not str or len(chunk) > request:
                    raise ValueError()
                size = len(chunk.encode("utf-8"))
            except Exception:
                raise ProjectionError("INVALID_TEXT_STREAM") from None
            self.byte_count += size
            if self.byte_count > self.max_bytes:
                raise ProjectionError("INPUT_SIZE_LIMIT")
            self.buffer, self.position = chunk, 0
        return self.buffer[self.position:self.position + 1]

    def _take(self):
        char = self._peek()
        if not char:
            raise ProjectionError("TRUNCATED_JSON")
        self.position += 1
        return char

    def _space(self):
        while self._peek() in (" ", "\t", "\r", "\n"):
            self._take()

    def _expect(self, text):
        for char in text:
            if self._take() != char:
                raise ProjectionError("INVALID_JSON")

    def _decode_value(self, token, path):
        # Separate from key decoding so tests can instrument the value boundary.
        try:
            return json.loads(token)
        except Exception:
            raise ProjectionError("INVALID_SCALAR") from None

    def _string(self, keep, path, key=False):
        self._expect('"')
        pieces = ['"'] if keep else None

        def append(char):
            if keep:
                pieces.append(char)
                if len(pieces) > 6 * self.max_string_bytes + 2:
                    raise ProjectionError("STRING_SIZE_LIMIT")

        while True:
            char = self._take()
            append(char)
            if char == '"':
                break
            if ord(char) < 32:
                raise ProjectionError("INVALID_STRING")
            if char == "\\":
                escape = self._take()
                append(escape)
                if escape == "u":
                    for _ in range(4):
                        digit = self._take()
                        append(digit)
                        if digit not in "0123456789abcdefABCDEF":
                            raise ProjectionError("INVALID_ESCAPE")
                elif escape not in '"\\/bfnrt':
                    raise ProjectionError("INVALID_ESCAPE")
        if not keep:
            return _SKIP
        token = "".join(pieces)
        try:
            value = json.loads(token) if key else self._decode_value(token, path)
            length = len(value.encode("utf-8", errors="surrogatepass"))
        except Exception:
            raise ProjectionError("INVALID_STRING") from None
        if length > self.max_string_bytes:
            raise ProjectionError("STRING_SIZE_LIMIT")
        return value

    def _number(self, keep, path):
        pieces = [] if keep else None

        def take():
            char = self._take()
            if keep:
                pieces.append(char)
                if len(pieces) > self.max_string_bytes:
                    raise ProjectionError("SCALAR_SIZE_LIMIT")

        if self._peek() == "-":
            take()
        if self._peek() == "0":
            take()
        elif self._peek() and self._peek() in "123456789":
            while self._peek() and self._peek() in "0123456789":
                take()
        else:
            raise ProjectionError("INVALID_NUMBER")
        if self._peek() == ".":
            take()
            if not self._peek() or self._peek() not in "0123456789":
                raise ProjectionError("INVALID_NUMBER")
            while self._peek() and self._peek() in "0123456789":
                take()
        if self._peek() in ("e", "E"):
            take()
            if self._peek() in ("+", "-"):
                take()
            if not self._peek() or self._peek() not in "0123456789":
                raise ProjectionError("INVALID_NUMBER")
            while self._peek() and self._peek() in "0123456789":
                take()
        if self._peek() and self._peek() not in " \t\r\n,]}":
            raise ProjectionError("INVALID_NUMBER")
        return self._decode_value("".join(pieces), path) if keep else _SKIP

    def _value(self, path, depth):
        self._space()
        char = self._peek()
        keep = self.allow(path)
        if char in ("{", "["):
            if depth >= self.max_depth:
                raise ProjectionError("DEPTH_LIMIT")
            return self._container(path, depth + 1, char == "{")
        if char == '"':
            return self._string(keep, path)
        if char and char in "-0123456789":
            return self._number(keep, path)
        for literal in ("true", "false", "null"):
            if char == literal[0]:
                self._expect(literal)
                return self._decode_value(literal, path) if keep else _SKIP
        raise ProjectionError("INVALID_JSON")

    def _container(self, path, depth, object_kind):
        self._take()
        end = "}" if object_kind else "]"
        seen, result, index = set(), {}, 0
        self._space()
        if self._peek() == end:
            self._take()
            return _SKIP
        while True:
            self._space()
            if object_kind:
                if self._peek() != '"':
                    raise ProjectionError("OBJECT_KEY_REQUIRED")
                key = self._string(True, path, key=True)
                if key in seen:
                    raise ProjectionError("DUPLICATE_JSON_KEY")
                seen.add(key)
                if self.key_guard:
                    self.key_guard(path, key)
                self._space()
                self._expect(":")
            else:
                key = index
            value = self._value(path + (key,), depth)
            if value is not _SKIP:
                result[key] = value
            self._space()
            separator = self._take()
            if separator == end:
                return result if result else _SKIP
            if separator != ",":
                raise ProjectionError("INVALID_SEPARATOR")
            index += 1

    def read(self):
        self._space()
        if self._peek() != "{":
            raise ProjectionError("ROOT_OBJECT_REQUIRED")
        value = self._value((), 0)
        self._space()
        if self._peek():
            raise ProjectionError("TRAILING_JSON")
        return {} if value is _SKIP else value


@dataclass(frozen=True)
class QuestionKey:
    source: str = field(repr=False)
    index: int


def _check_batch(batch):
    if type(batch) is not tuple or not batch or len(batch) > 10000:
        raise ContractError("EXACT_NONEMPTY_BATCH_REQUIRED")
    for key in batch:
        if (type(key) is not QuestionKey or type(key.source) is not str
                or not key.source or type(key.index) is not int or key.index < 0):
            raise ContractError("INVALID_BATCH_KEY")
    if len(set(batch)) != len(batch):
        raise ContractError("DUPLICATE_BATCH_KEY")


def _question_path(path):
    return (len(path) == 4 and type(path[0]) is str
            and path[1] == "benchmark_dataset" and type(path[2]) is int)


@dataclass(frozen=True)
class SourceRecord:
    source: str = field(repr=False)
    metadata: tuple = field(repr=False)


@dataclass(frozen=True)
class QuestionRecord:
    key: QuestionKey
    task: str = field(repr=False)
    question: str = field(repr=False)
    options: tuple = field(default=(), repr=False)


@dataclass(frozen=True)
class Projection:
    view: str
    sources: tuple
    questions: tuple


def _finite(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def project_nongold(stream, batch, view="screen", **limits):
    """No gold validator is called. Inference options never enter decomposition."""
    _check_batch(batch)
    if view not in ("screen", "inference"):
        raise ContractError("INVALID_VIEW")
    wanted = set(batch)
    source_order = tuple(dict.fromkeys(key.source for key in batch))
    source_set = set(source_order)

    def allow(path):
        if (len(path) == 3 and path[0] in source_set
                and path[1] == "video_metadata" and path[2] in META_FIELDS):
            return True
        return (_question_path(path)
                and QuestionKey(path[0], path[2]) in wanted
                and path[3] in (("video_uid", "task", "question")
                               + (OPTIONS if view == "inference" else ())))

    def guard(path, key):
        if (view == "inference" and len(path) == 3
                and path[1] == "benchmark_dataset" and type(path[2]) is int
                and QuestionKey(path[0], path[2]) in wanted
                and re.fullmatch(r"answer_\d+", key) and key not in OPTIONS):
            raise ProjectionError("EXTRA_OPTION_FIELD")

    data = _Projector(stream, allow, guard, **limits).read()
    sources, questions = [], []
    for source in source_order:
        node = data.get(source, {})
        metadata = node.get("video_metadata", {})
        for name, value in metadata.items():
            valid = (type(value) is bool if name in ("release_1", "canonical_is_validated")
                     else _finite(value) and value > 0 if name == "duration_in_seconds"
                     else type(value) is str and bool(value.strip()))
            if not valid:
                raise ProjectionError("INVALID_METADATA_TYPE")
        sources.append(SourceRecord(source, tuple((k, metadata[k]) for k in META_FIELDS
                                                  if k in metadata)))
        for key in sorted((k for k in batch if k.source == source), key=lambda k: k.index):
            row = node.get("benchmark_dataset", {}).get(key.index, {})
            if row.get("video_uid") != source:
                raise ProjectionError("QUESTION_UID_MISMATCH_OR_MISSING")
            if any(type(row.get(k)) is not str or not row[k].strip()
                   for k in ("task", "question")):
                raise ProjectionError("QUESTION_FIELDS_REQUIRED")
            if view == "inference" and any(
                    type(row.get(k)) is not str or not row[k].strip() for k in OPTIONS):
                raise ProjectionError("FIVE_NONEMPTY_OPTIONS_REQUIRED")
            questions.append(QuestionRecord(key, row["task"], row["question"],
                                           tuple(row[k] for k in OPTIONS)
                                           if view == "inference" else ()))
    return Projection(view, tuple(sources), tuple(questions))


@dataclass(frozen=True)
class Decomposition:
    status: str
    reason: str
    event_a: str = field(default="", repr=False)
    event_b: str = field(default="", repr=False)


def decompose(task, question):
    if task != TASK:
        return Decomposition("UNSUPPORTED", "TASK_NOT_ADMITTED")
    if type(question) is not str or len(question) > 4096:
        return Decomposition("UNSUPPORTED", "QUESTION_TYPE_OR_LENGTH")
    text = " ".join(question.split())
    match = re.fullmatch(r"How long after (.+)\?", text, flags=re.I)
    if not match:
        return Decomposition("UNSUPPORTED", "NOT_TIME_GAP_FORM")
    body = match.group(1)
    candidates = []
    for boundary in _AUX.finditer(body):
        left, right = body[:boundary.start()].strip(), body[boundary.end():].strip()
        if left.endswith(","):
            left = left[:-1].rstrip()
        if left and right:
            candidates.append((left, right))
    if len(candidates) != 1:
        return Decomposition("UNSUPPORTED", "AMBIGUOUS_OR_MISSING_BOUNDARY")
    left, right = candidates[0]
    if _MARKER.search(left) or _MARKER.search(right):
        return Decomposition("UNSUPPORTED", "NESTED_TEMPORAL_MARKER")
    return Decomposition("OK", "QUESTION_GIVEN_A_BEFORE_B", left, right)


@dataclass(frozen=True)
class Selection:
    arm: str
    indices: tuple
    anchors: tuple = ()
    event_pair: tuple = ()
    evidence_status: str = "NOT_ASSESSED"


def select_four(pts, q, a, b):
    vectors = (pts, q, a, b)
    if any(type(v) not in (tuple, list) or len(v) != 48 for v in vectors):
        raise ContractError("FOUR_LENGTH_48_VECTORS_REQUIRED")
    if any(not _finite(x) for v in vectors for x in v):
        raise ContractError("FINITE_NUMBERS_REQUIRED")
    if any(pts[i] >= pts[i + 1] for i in range(47)):
        raise ContractError("STRICT_PTS_REQUIRED")
    if any(not -1 <= x <= 1 for v in (q, a, b) for x in v):
        raise ContractError("RAW_COSINE_RANGE_REQUIRED")
    ranked = tuple(sorted(range(48), key=lambda i: (-q[i], pts[i], i)))
    result = [Selection("A", tuple(round(47 * k / 11) for k in range(12))),
              Selection("B", tuple(sorted(ranked[:12])))]
    for arm in ("C", "D"):
        pair = min(((i, j) for i in range(48) for j in range(48)
                    if (i != j if arm == "C" else i < j)),
                   key=lambda ij: (-(a[ij[0]] + b[ij[1]]), ij[0], ij[1]))
        anchors = tuple(sorted(pair))
        chosen = anchors + tuple(i for i in ranked if i not in anchors)[:10]
        result.append(Selection(arm, tuple(sorted(chosen)), anchors, pair,
                                "EVIDENCE_PRESENCE_UNVERIFIED"))
    return tuple(result)


@dataclass(frozen=True)
class PlanQuestion:
    key: QuestionKey
    task: str = field(repr=False)
    question: str = field(repr=False)
    decomposition: Decomposition


@dataclass(frozen=True)
class Call:
    key: QuestionKey
    arm: str


@dataclass(frozen=True)
class FrozenPlan:
    sources: tuple
    questions: tuple
    exclusions: tuple
    calls: tuple

    @property
    def n_planned(self):
        return len(self.questions)


def _calls(questions):
    calls = []
    for index, question in enumerate(questions):
        shift = index % 4
        calls.extend(Call(question.key, arm) for arm in ARMS[shift:] + ARMS[:shift])
    return tuple(calls)


def build_plan(projection):
    if (type(projection) is not Projection or projection.view not in ("screen", "inference")
            or type(projection.sources) is not tuple or type(projection.questions) is not tuple
            or any(type(s) is not SourceRecord or type(s.source) is not str
                   or not s.source or type(s.metadata) is not tuple for s in projection.sources)
            or any(type(q) is not QuestionRecord or type(q.key) is not QuestionKey
                   or type(q.task) is not str or type(q.question) is not str
                   or type(q.options) is not tuple or any(type(x) is not str for x in q.options)
                   for q in projection.questions)):
        raise ContractError("PROJECTION_REQUIRED")
    for source in projection.sources:
        if any(type(pair) is not tuple or len(pair) != 2 or pair[0] not in META_FIELDS
               or type(pair[1]) not in (str, int, float, bool) for pair in source.metadata):
            raise ContractError("IMMUTABLE_METADATA_REQUIRED")
    if projection.questions:
        _check_batch(tuple(q.key for q in projection.questions))
    source_order = tuple(s.source for s in projection.sources)
    if len(set(source_order)) != len(source_order):
        raise ContractError("DUPLICATE_SOURCE")
    rank = {source: i for i, source in enumerate(source_order)}
    if any(q.key.source not in rank for q in projection.questions):
        raise ContractError("UNREGISTERED_SOURCE")
    rows = tuple(sorted(projection.questions, key=lambda q: (rank[q.key.source], q.key.index)))
    if len({q.key for q in rows}) != len(rows):
        raise ContractError("DUPLICATE_BATCH_KEY")
    accepted, excluded = [], []
    for row in rows:
        parts = decompose(row.task, row.question)
        if parts.status == "OK":
            accepted.append(PlanQuestion(row.key, row.task, row.question, parts))
        else:
            excluded.append((row.key, parts.reason))
    questions = tuple(accepted)
    return FrozenPlan(tuple(projection.sources), questions, tuple(excluded), _calls(questions))
