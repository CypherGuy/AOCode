import pytest
from Code.core.aoc_fetcher import get_last_paragraph


@pytest.mark.parametrize("text,expected", [
    ("", ""),
    ("This is a single paragraph.", "This is a single paragraph."),
    ("This is the first paragraph.\n\nThis is the second paragraph.",
     "This is the second paragraph."),
    ("   This is a paragraph with leading whitespace.   \n\nThis is another paragraph.",
     "This is another paragraph."),
    ("This is a paragraph.\n\n\nThis is another paragraph.",
     "This is another paragraph."),
])
def test_get_last_paragraph(text, expected):
    """Test get_last_paragraph with various inputs."""
    assert get_last_paragraph(text) == expected


def test_get_last_paragraph_with_trailing_whitespace():
    """Test that trailing whitespace is handled correctly."""
    text = "First paragraph.\n\nLast paragraph.   \n\n"
    assert get_last_paragraph(text) == "Last paragraph.   "


def test_get_last_paragraph_with_only_whitespace():
    """Test that only whitespace returns empty string."""
    text = "   \n\n   \n   "
    assert get_last_paragraph(text) == ""
