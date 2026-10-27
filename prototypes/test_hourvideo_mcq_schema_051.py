"""Owned fixtures only; no HourVideo records, labels, paths or model imports."""
import unittest
from hourvideo_mcq_schema_051 import bind_original_nongold, parse_mcq_test, SchemaError


class TestOfficialDisplayBinding(unittest.TestCase):
    options = ["owned red", "owned blue", "owned green", "owned gray", "owned gold"]

    def display(self, values=None, sep="\n", marker="dot"):
        values = self.options if values is None else values
        def prefix(c):
            return f"({c})" if marker == "paren" else f"{c})" if marker == "close" else f"{c}:" if marker == "colon" else f"{c}."
        return sep.join(f"{prefix(c)} {v}" for c, v in zip("ABCDE", values))

    def bind(self, display=None, **extra):
        row = {"question": "Owned question?", "mcq_test": self.display() if display is None else display, **extra}
        return bind_original_nongold(row, "Owned question?", self.options)

    def test_official_lines(self):
        self.assertEqual(self.bind()["options"], self.options)

    def test_inline_labels(self):
        self.assertEqual(self.bind(self.display(sep=" "))["parse_mode"], "inline_labels")

    def test_marker_forms(self):
        for marker in ("dot", "paren", "close", "colon"):
            with self.subTest(marker=marker):
                self.assertEqual(self.bind(self.display(marker=marker))["options"], self.options)
                compact = self.display(marker=marker).replace(". ", ".").replace(") ", ")").replace(": ", ":")
                self.assertEqual(self.bind(compact)["options"], self.options)

    def test_structural_header(self):
        self.assertEqual(self.bind("Answers:\n" + self.display())["schema"], "official_mcq_test")

    def test_crlf(self):
        self.assertEqual(self.bind(self.display(sep="\r\n"))["options"], self.options)

    def test_boundary_whitespace(self):
        values = ["  " + x + "  " for x in self.options]
        self.assertEqual(self.bind(self.display(values))["options"], self.options)
        row = {"question": "Owned question?", "mcq_test": self.display()}
        bound = bind_original_nongold(row, "Owned question?", values)
        self.assertEqual(bound["options"], values)
        self.assertEqual(bound["frozen_option_boundary_normalization_count"], 5)

    def test_interior_whitespace_not_changed(self):
        values = self.options.copy(); values[0] = "owned  red"
        with self.assertRaises(SchemaError):
            self.bind(self.display(values))

    def test_case_not_changed(self):
        values = self.options.copy(); values[0] = values[0].upper()
        with self.assertRaises(SchemaError):
            self.bind(self.display(values))

    def test_label_swap_refused(self):
        values = self.options.copy(); values[0], values[1] = values[1], values[0]
        with self.assertRaises(SchemaError):
            self.bind(self.display(values))

    def test_missing_or_repeated_label_refused(self):
        for value in (self.display().replace("E. ", "D. "), self.display().split("\nE. ")[0]):
            with self.subTest(value=value), self.assertRaises(SchemaError):
                self.bind(value)

    def test_question_must_join(self):
        with self.assertRaises(SchemaError):
            bind_original_nongold({"question": "different", "mcq_test": self.display()},
                                  "Owned question?", self.options)

    def test_no_old_options_fallback(self):
        row = {"question": "Owned question?", "options": self.options,
               **{f"answer_{i+1}": v for i, v in enumerate(self.options)}}
        with self.assertRaises(SchemaError):
            bind_original_nongold(row, "Owned question?", self.options)

    def test_answer_fields_do_not_override_display(self):
        row = {"question": "Owned question?", "mcq_test": self.display(),
               **{f"answer_{i+1}": v for i, v in enumerate(reversed(self.options))}}
        self.assertEqual(bind_original_nongold(row, "Owned question?", self.options)["options"], self.options)

    def test_multiline_body_and_incidental_label(self):
        values = self.options.copy(); values[0] = "owned Plan B. detail\ncontinued"
        parsed, mode = parse_mcq_test(self.display(values))
        self.assertEqual(parsed, values); self.assertEqual(mode, "line_labels")

    def test_gold_value_never_accessed(self):
        class Forbidden:
            def __str__(self): raise AssertionError("gold string access")
            def __repr__(self): raise AssertionError("gold repr access")
        result = self.bind(correct_answer_label=Forbidden())
        self.assertEqual(result["gold_values_accessed"], 0)

    def test_unrecognized_prefix_and_oversize_refused(self):
        for value in ("arbitrary prefix\n" + self.display(), "x" * 65537):
            with self.subTest(size=len(value)), self.assertRaises(SchemaError):
                self.bind(value)


if __name__ == "__main__":
    unittest.main()
