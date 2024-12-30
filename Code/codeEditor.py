#!/usr/bin/env python3
# python_highlighter.py

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QSyntaxHighlighter, QTextCharFormat, QColor, QFont
)
from PySide6.QtWidgets import QApplication, QTextEdit

# For our State controller
STATE_NONE = 0
STATE_MULTILINE_SINGLE = 1
STATE_MULTILINE_DOUBLE = 2
STATE_SINGLE_UNCLOSED = 3
STATE_DOUBLE_UNCLOSED = 4

PYTHON_KEYWORDS = [
    "False", "None", "True",
    "and", "as", "assert",
    "async", "await",
    "break",
    "class", "continue",
    "def", "del",
    "elif", "else", "except",
    "finally", "for", "from",
    "global",
    "if", "import", "in", "is",
    "lambda",
    "nonlocal", "not",
    "or",
    "pass",
    "raise", "return",
    "try",
    "while", "with",
    "yield",
    "print"
]


class PythonHighlighter(QSyntaxHighlighter):
    """
    A PySide6-based Python syntax highlighter that:
      - Highlights the next identifier after 'class' as a class name (blue)
      - Handles multiline triple-quoted strings
      - Handles unclosed single/double quotes (continuing across lines)
      - Highlights # comments in gray
      - Keywords in orange
      - Default text in black
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Keywords => Orange + Bold
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#FF8C00"))  # orange
        self.keyword_format.setFontWeight(QFont.Bold)

        # Classes => Softer Blue + Bold
        self.class_format = QTextCharFormat()
        self.class_format.setForeground(QColor("#6699CC"))
        self.class_format.setFontWeight(QFont.Bold)

        # Strings => Green
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#00C800"))

        # Comments => Gray + Italic
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#888888"))
        self.comment_format.setFontItalic(True)

        # Normal => White
        self.normal_format = QTextCharFormat()
        self.normal_format.setForeground(QColor("#ffffff"))

        # Store the Python keywords
        self.keywords = PYTHON_KEYWORDS
        self.waiting_for_class_name = False

    def highlightBlock(self, text: str):
        """
        A single-pass state machine that tracks multiline/unclosed strings across lines.
        """
        prev_state = self.previousBlockState()
        if prev_state == -1:
            prev_state = STATE_NONE

        state = prev_state
        self.setCurrentBlockState(state)

        i = 0
        length = len(text)

        while i < length:
            if state == STATE_MULTILINE_SINGLE:
                # Currently inside ''' ... '''
                end_index = text.find("'''", i)
                if end_index == -1:
                    # Can't be closed
                    self.setFormat(i, length - i, self.string_format)
                    self.setCurrentBlockState(STATE_MULTILINE_SINGLE)
                    break
                else:
                    self.setFormat(i, end_index + 3 - i, self.string_format)
                    i = end_index + 3
                    state = STATE_NONE
                    self.setCurrentBlockState(STATE_NONE)

            elif state == STATE_MULTILINE_DOUBLE:
                # Currently inside """ ... """
                end_index = text.find('"""', i)
                if end_index == -1:
                    self.setFormat(i, length - i, self.string_format)
                    self.setCurrentBlockState(STATE_MULTILINE_DOUBLE)
                    break
                else:
                    self.setFormat(i, end_index + 3 - i, self.string_format)
                    i = end_index + 3
                    state = STATE_NONE
                    self.setCurrentBlockState(STATE_NONE)

            elif state == STATE_SINGLE_UNCLOSED:
                close_index = self.find_unescaped_quote(text, "'", i)
                if close_index == -1:
                    self.setFormat(i, length - i, self.string_format)
                    self.setCurrentBlockState(STATE_SINGLE_UNCLOSED)
                    break
                else:
                    self.setFormat(i, close_index + 1 - i, self.string_format)
                    i = close_index + 1
                    state = STATE_NONE
                    self.setCurrentBlockState(STATE_NONE)

            elif state == STATE_DOUBLE_UNCLOSED:
                close_index = self.find_unescaped_quote(text, '"', i)
                if close_index == -1:
                    self.setFormat(i, length - i, self.string_format)
                    self.setCurrentBlockState(STATE_DOUBLE_UNCLOSED)
                    break
                else:
                    self.setFormat(i, close_index + 1 - i, self.string_format)
                    i = close_index + 1
                    state = STATE_NONE
                    self.setCurrentBlockState(STATE_NONE)

            else:
                triple_single_index = text.find("'''", i)
                triple_double_index = text.find('"""', i)
                single_quote_index = text.find("'", i)
                double_quote_index = text.find('"', i)
                hash_index = text.find('#', i)

                matches = []
                if triple_single_index != -1:
                    matches.append((triple_single_index, "multisingle"))
                if triple_double_index != -1:
                    matches.append((triple_double_index, "multidouble"))
                if single_quote_index != -1:
                    matches.append((single_quote_index, "single"))
                if double_quote_index != -1:
                    matches.append((double_quote_index, "double"))
                if hash_index != -1:
                    matches.append((hash_index, "comment"))

                if not matches:
                    # No special tokens -> highlight leftover code
                    self.highlight_keywords_and_class_names(text, i, length)
                    break

                matches.sort(key=lambda x: x[0])
                found_pos, token_type = matches[0]

                if found_pos > i:
                    self.highlight_keywords_and_class_names(
                        text, i, found_pos)

                if token_type == "comment":
                    self.setFormat(found_pos, length -
                                   found_pos, self.comment_format)
                    break

                elif token_type == "multisingle":
                    self.setFormat(found_pos, 3, self.string_format)
                    i = found_pos + 3
                    state = STATE_MULTILINE_SINGLE
                    self.setCurrentBlockState(STATE_MULTILINE_SINGLE)

                elif token_type == "multidouble":
                    self.setFormat(found_pos, 3, self.string_format)
                    i = found_pos + 3
                    state = STATE_MULTILINE_DOUBLE
                    self.setCurrentBlockState(STATE_MULTILINE_DOUBLE)

                elif token_type == "single":
                    self.setFormat(found_pos, 1, self.string_format)
                    i = found_pos + 1
                    close_index = self.find_unescaped_quote(text, "'", i)
                    if close_index == -1:
                        self.setFormat(i, length - i, self.string_format)
                        self.setCurrentBlockState(STATE_SINGLE_UNCLOSED)
                        break
                    else:
                        self.setFormat(i, close_index - i +
                                       1, self.string_format)
                        i = close_index + 1
                        # Keep going

                elif token_type == "double":
                    # Highlight opening double quote and enter double-quoted string
                    self.setFormat(found_pos, 1, self.string_format)
                    i = found_pos + 1
                    close_index = self.find_unescaped_quote(text, '"', i)
                    if close_index == -1:
                        # Unclosed double quote => highlight rest of line
                        self.setFormat(i, length - i, self.string_format)
                        self.setCurrentBlockState(STATE_DOUBLE_UNCLOSED)
                        break
                    else:
                        self.setFormat(i, close_index - i +
                                       1, self.string_format)
                        i = close_index + 1

            if state == STATE_NONE:
                self.waiting_for_class_name = False

    def highlight_keywords_and_class_names(self, text, start_pos, end_pos):
        """
        Parses the text chunk [start_pos:end_pos], 
        highlighting keywords and the next valid identifier if we just saw 'class'.
        We do NOT reset self.waiting_for_class_name on punctuation, so even if
        there's whitespace or parentheses after 'class', the next identifier 
        is still the class name.
        """
        i = start_pos

        while i < end_pos:
            ch = text[i]

            if not (ch.isalpha() or ch == '_'):
                i += 1
                continue

            # Start of a word
            start_word = i
            while i < end_pos and (text[i].isalnum() or text[i] == '_'):
                i += 1
            word = text[start_word:i]

            # Is it a class?
            if self.waiting_for_class_name:
                self.setFormat(start_word, len(word), self.class_format)
                self.waiting_for_class_name = False
            else:
                # Else, check if keyword
                if word in self.keywords:
                    self.setFormat(start_word, len(word), self.keyword_format)
                    if word == "class":
                        self.waiting_for_class_name = True

    def find_unescaped_quote(self, text, quote_char, start):
        """
        Finds the next unescaped quote character.
        Returns the index or -1 if not found.
        """
        i = start
        while i < len(text):
            if text[i] == '\\':
                i += 2  # Skip escaped character
                continue
            if i < len(text) and text[i] == quote_char:
                return i
            i += 1
        return -1

    def highlight_brackets(self, text):
        """
        Highlights brackets ()[]{ } in black.
        """
        brackets = "()[]{}"
        for idx, ch in enumerate(text):
            if ch in brackets:
                self.setFormat(idx, 1, self.normal_format)
