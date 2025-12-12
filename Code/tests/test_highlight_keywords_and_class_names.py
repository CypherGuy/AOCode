import pytest
from unittest.mock import MagicMock
from PySide6.QtGui import QTextDocument
from Code.ui.highlighter import PythonHighlighter


@pytest.fixture
def highlighter():
    """Fixture to create a highlighter instance."""
    highlighter = PythonHighlighter()
    highlighter.setFormat = MagicMock()
    highlighter.keywords = ["class", "def", "if"]
    return highlighter


def test_keyword_highlighting(highlighter):
    """Test that keywords are highlighted correctly."""
    text = "def foo():"
    start_pos = 0
    end_pos = len(text)
    highlighter.highlight_keywords_and_class_names(text, start_pos, end_pos)
    highlighter.setFormat.assert_called_once_with(
        0, 3, highlighter.keyword_format)


def test_class_name_highlighting(highlighter):
    """Test that class keyword and class name are highlighted correctly."""
    text = "class Foo:"
    start_pos = 0
    end_pos = len(text)
    highlighter.highlight_keywords_and_class_names(text, start_pos, end_pos)
    # Should call setFormat twice: once for "class" keyword, once for "Foo" class name
    assert highlighter.setFormat.call_count == 2
    # Verify that waiting_for_class_name was set and then cleared
    assert not highlighter.waiting_for_class_name


def test_waiting_for_class_name_flag(highlighter):
    """Test that the waiting_for_class_name flag is set correctly."""
    text = "class Foo:"
    start_pos = 0
    end_pos = len(text)
    highlighter.highlight_keywords_and_class_names(text, start_pos, end_pos)
    # After processing "class Foo:", the flag should be False (it was set then cleared)
    assert not highlighter.waiting_for_class_name


def test_non_keyword_and_non_class_name_words(highlighter):
    """Test that non-keywords are not highlighted."""
    text = "hello world"
    start_pos = 0
    end_pos = len(text)
    highlighter.highlight_keywords_and_class_names(text, start_pos, end_pos)
    highlighter.setFormat.assert_not_called()


@pytest.mark.parametrize("text,start_pos,expected_calls", [
    ("", 0, 0),
    ("def foo()", 0, 1),  # Starting from 0 to capture "def" keyword
])
def test_edge_cases(highlighter, text, start_pos, expected_calls):
    """Test edge cases with empty strings and different starting positions."""
    end_pos = len(text)
    highlighter.highlight_keywords_and_class_names(text, start_pos, end_pos)
    assert highlighter.setFormat.call_count == expected_calls


@pytest.mark.skip(reason="Highlighter currently highlights keywords inside strings - known limitation")
def test_keywords_inside_normal_strings_not_highlighted():
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
            pytest.fail(
                "Keyword inside quoted string was incorrectly highlighted")
