"""Strict HourVideo display-option binding for task 051.

Only nongold question and mcq_test are accessed. Dataset text is never executed.
Official baseline builds the prompt from question + mcq_test; raw answer_N
fields do not override display labels. No model/runtime imports.
"""
import re

MAX_DISPLAY_CHARS = 65536
_LABEL = r"(?:\(([A-E])\)|([A-E])[.):])"
_LINE = re.compile(r"(?m)^[ \t]*" + _LABEL + r"[ \t]*")
_INLINE = re.compile(r"(?:^|(?<=\s))" + _LABEL + r"[ \t]*")
_HEADERS = {"", "Answers:", "Options:", "Choices:"}


class SchemaError(ValueError):
    pass


def _require(ok, reason):
    if not ok:
        raise SchemaError(reason)


def _extract(text, pattern):
    matches = list(pattern.finditer(text))
    labels = [(m.group(1) or m.group(2)) for m in matches]
    if labels != list("ABCDE"):
        return None
    if text[:matches[0].start()].strip() not in _HEADERS:
        return None
    values = [
        text[m.end():matches[j + 1].start() if j + 1 < len(matches) else len(text)].strip()
        for j, m in enumerate(matches)
    ]
    return values if all(values) else None


def parse_mcq_test(display):
    _require(type(display) is str and 0 < len(display) <= MAX_DISPLAY_CHARS,
             "MCQ_TEST_STRING_REQUIRED")
    text = display.replace("\r\n", "\n").replace("\r", "\n")
    # Structured line labels take precedence over incidental labels in bodies.
    values = _extract(text, _LINE)
    mode = "line_labels"
    if values is None:
        values = _extract(text, _INLINE)
        mode = "inline_labels"
    _require(values is not None, "MCQ_TEST_LABELS_OR_BODY_INVALID")
    return values, mode


def bind_original_nongold(row, frozen_question, frozen_options):
    _require(type(row) is dict, "ORIGINAL_OBJECT_REQUIRED")
    _require("question" in row and type(row["question"]) is str,
             "ORIGINAL_QUESTION_REQUIRED")
    _require("mcq_test" in row, "ORIGINAL_MCQ_TEST_REQUIRED")
    _require(type(frozen_question) is str and row["question"] == frozen_question,
             "QUESTION_JOIN_MISMATCH")
    _require(type(frozen_options) is list and len(frozen_options) == 5
             and all(type(x) is str and x.strip() for x in frozen_options),
             "FROZEN_OPTIONS_INVALID")
    actual, mode = parse_mcq_test(row["mcq_test"])
    expected = [x.replace("\r\n", "\n").replace("\r", "\n").strip()
                for x in frozen_options]
    # Formatting whitespace at boundaries is allowed; no case/punctuation or
    # interior whitespace normalization, reordering, or answer-key access.
    _require(actual == expected, "DISPLAY_OPTIONS_JOIN_MISMATCH")
    return {
        "question": frozen_question,
        "options": list(frozen_options),
        "schema": "official_mcq_test",
        "parse_mode": mode,
        "option_order": "ABCDE",
        "gold_values_accessed": 0,
        "frozen_option_boundary_normalization_count": sum(a != b for a, b in zip(frozen_options, expected)),
        "interior_normalization": False,
    }
