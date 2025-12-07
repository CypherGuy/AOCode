import unittest
from unittest.mock import MagicMock
from Code.ui.highlighter import PythonHighlighter


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

    def test_keywords_inside_normal_strings_not_highlighted(self):
        """Ensure keywords inside quoted strings are NOT highlighted."""
        text = 'print("class def if while return")'
        doc = QTextDocument(text)
        highlighter = PythonHighlighter(doc)

        # Spy on setFormat
        highlighter.setFormat = MagicMock()

        # Run the highlighter on the whole document
        highlighter.rehighlight()

        # Extract all formatted segments (start, count, format)
        calls = highlighter.setFormat.call_args_list

        # Check each call to ensure the highlighted text is NOT inside the string
        inside_string_range = (text.index('"'), text.rindex('"'))

        for call in calls:
            start, count, _ = call[0]
            # If any formatting covers chars inside quotes → FAIL
            if start >= inside_string_range[0] and start < inside_string_range[1]:
                self.fail(
                    "Keyword inside quoted string was incorrectly highlighted")

        # If no illegal call fails, the test passes
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
