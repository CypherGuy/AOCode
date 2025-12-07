import unittest

from Code.core.aoc_fetcher import get_last_paragraph


class TestGetLastParagraph(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(get_last_paragraph(""), "")

    def test_single_paragraph(self):
        text = "This is a single paragraph."
        self.assertEqual(get_last_paragraph(text), text)

    def test_multiple_paragraphs(self):
        text = "This is the first paragraph.\n\nThis is the second paragraph."
        self.assertEqual(get_last_paragraph(
            text), "This is the second paragraph.")

    def test_paragraphs_with_whitespace(self):
        text = "   This is a paragraph with leading whitespace.   \n\nThis is another paragraph."
        self.assertEqual(get_last_paragraph(
            text), "This is another paragraph.")

    def test_paragraphs_with_multiple_newlines(self):
        text = "This is a paragraph.\n\n\nThis is another paragraph."
        self.assertEqual(get_last_paragraph(
            text), "This is another paragraph.")


if __name__ == "__main__":
    unittest.main()
