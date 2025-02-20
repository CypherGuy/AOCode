import unittest
from unittest.mock import MagicMock
from Code.Highlighter import PythonHighlighter


class TestHighlightKeywordsAndClassNames(unittest.TestCase):
    def setUp(self):
        self.highlighter = PythonHighlighter()
        self.highlighter.setFormat = MagicMock()
        # assuming these are the keywords
        self.highlighter.keywords = ["class", "def", "if"]

    def test_keyword_highlighting(self):
        text = "def foo():"
        start_pos = 0
        end_pos = len(text)
        self.highlighter.highlight_keywords_and_class_names(
            text, start_pos, end_pos)
        self.highlighter.setFormat.assert_called_once_with(
            0, 3, self.highlighter.keyword_format)

    def test_class_name_highlighting(self):
        text = "class Foo:"
        start_pos = 0
        end_pos = len(text)
        self.highlighter.highlight_keywords_and_class_names(
            text, start_pos, end_pos)
        self.highlighter.setFormat.assert_called_once_with(
            0, 5, self.highlighter.class_format)

    def test_waiting_for_class_name_flag(self):
        text = "class Foo:"
        start_pos = 0
        end_pos = len(text)
        self.highlighter.highlight_keywords_and_class_names(
            text, start_pos, end_pos)
        self.assertTrue(self.highlighter.waiting_for_class_name)

    def test_non_keyword_and_non_class_name_words(self):
        text = "hello world"
        start_pos = 0
        end_pos = len(text)
        self.highlighter.highlight_keywords_and_class_names(
            text, start_pos, end_pos)
        self.highlighter.setFormat.assert_not_called()

    def test_edge_cases(self):
        text = ""
        start_pos = 0
        end_pos = 0
        self.highlighter.highlight_keywords_and_class_names(
            text, start_pos, end_pos)
        self.highlighter.setFormat.assert_not_called()

        text = "def foo()"
        start_pos = 1
        end_pos = len(text)
        self.highlighter.highlight_keywords_and_class_names(
            text, start_pos, end_pos)
        self.highlighter.setFormat.assert_called_once_with(
            1, 3, self.highlighter.keyword_format)


if __name__ == "__main__":
    unittest.main()
