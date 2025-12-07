import re
from PySide6.QtGui import (
    QSyntaxHighlighter, QTextCharFormat, QColor, QFont
)

# For our State controller
STATE_NONE = 0
STATE_MULTILINE_SINGLE = 1
STATE_MULTILINE_DOUBLE = 2
STATE_SINGLE_UNCLOSED = 3
STATE_DOUBLE_UNCLOSED = 4

PYTHON_KEYWORDS = [
    'None', 'and', 'as', 'assert',
    'async', 'await', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if',
    'import', 'in', 'is', 'lambda', 'nonlocal',
    'not', 'or', 'pass', 'raise', 'return',
    'try', 'while', 'with', 'yield', 'print',
    'abs', 'all', 'any', 'bin', 'bool', 'bytearray',
    'bytes', 'chr', 'complex', 'divmod',
    'enumerate', 'float', 'format', 'frozenset',
    'hex', 'input', 'isinstance', 'iter'
]


MAGIC_METHODS = ["__init__", "__str__",
                 "__repr__", "__len__", "__eq__"]

BOOLS = ["True", "False"]


class PythonHighlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Keywords => Orange + Bold
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#FF8C00"))
        self.keyword_format.setFontWeight(QFont.Bold)

        # Functions => Dark Orange + Bold
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor("#DC7800"))
        self.function_format.setFontWeight(QFont.Bold)

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

        # Magic Methods => Maroon
        self.magic_method_format = QTextCharFormat()
        self.magic_method_format.setForeground(QColor("#FF6347"))
        self.magic_method_format.setFontWeight(QFont.Bold)

        # Brackets => White
        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor("#FFFFFF"))

        # Normal => White
        self.normal_format = QTextCharFormat()
        self.normal_format.setForeground(QColor("#FFFFFF"))

        # Integers & Boolean => Purple
        self.integer_boolean_format = QTextCharFormat()
        self.integer_boolean_format.setForeground(QColor("#BB83E6"))

        # "self" => Italic + Purple
        self.self_format = QTextCharFormat()
        self.self_format.setForeground(QColor("#BB83E6"))
        self.self_format.setFontItalic(True)

        self.keywords = PYTHON_KEYWORDS
        self.waiting_for_class_name = False

        self.escaped_methods = [re.escape(method)
                                for method in MAGIC_METHODS]
        self.pattern = r'\b(?:' + '|'.join(self.escaped_methods) + r')\b'
        self.magic_methods_regex = re.compile(self.pattern)

        self.integer_boolean_regex = re.compile(r'\b\d+\b')

        self.function_regex = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\()')
        self.self_regex = re.compile(r'\bself.')

    def highlightBlock(self, text: str) -> None:
        """
        A single-pass state machine that tracks multiline/unclosed strings across lines.
        Strings have top priority: once inside quotes, everything stays string-coloured.
        """
        prev_state = self.previousBlockState()
        if prev_state == -1:
            prev_state = STATE_NONE

        state = prev_state
        self.setCurrentBlockState(state)

        i = 0
        length = len(text)

        while i < length:
            # =========================
            #  CONTINUE MULTILINE STATES
            # =========================
            if state == STATE_MULTILINE_SINGLE:
                end_index = text.find("'''", i)
                if end_index == -1:
                    self.setFormat(i, length - i, self.string_format)
                    self.setCurrentBlockState(STATE_MULTILINE_SINGLE)
                    break
                else:
                    self.setFormat(i, end_index + 3 - i, self.string_format)
                    i = end_index + 3
                    state = STATE_NONE
                    self.setCurrentBlockState(STATE_NONE)
                    continue

            elif state == STATE_MULTILINE_DOUBLE:
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
                    continue

            elif state == STATE_SINGLE_UNCLOSED:
                close_index = self.find_unescaped_quote(text, "'", i)
                if close_index == -1:
                    self.setFormat(i, length - i, self.string_format)
                    self.setCurrentBlockState(STATE_SINGLE_UNCLOSED)
                    break
                else:
                    self.setFormat(i, close_index - i + 1, self.string_format)
                    i = close_index + 1
                    state = STATE_NONE
                    self.setCurrentBlockState(STATE_NONE)
                    continue

            elif state == STATE_DOUBLE_UNCLOSED:
                close_index = self.find_unescaped_quote(text, '"', i)
                if close_index == -1:
                    self.setFormat(i, length - i, self.string_format)
                    self.setCurrentBlockState(STATE_DOUBLE_UNCLOSED)
                    break
                else:
                    self.setFormat(i, close_index - i + 1, self.string_format)
                    i = close_index + 1
                    state = STATE_NONE
                    self.setCurrentBlockState(STATE_NONE)
                    continue

            # =========================
            #  NORMAL STATE: PRIORITISE STRINGS FIRST
            # =========================
            else:
                ch = text[i]

                # Triple-double first: """..."""
                if text.startswith('"""', i):
                    self.setFormat(i, 3, self.string_format)
                    i += 3
                    state = STATE_MULTILINE_DOUBLE
                    self.setCurrentBlockState(state)
                    continue

                # Triple-single: '''...'''
                if text.startswith("'''", i):
                    self.setFormat(i, 3, self.string_format)
                    i += 3
                    state = STATE_MULTILINE_SINGLE
                    self.setCurrentBlockState(state)
                    continue

                # Single-quoted string: '...'
                if ch == "'":
                    start = i
                    i += 1
                    while i < length:
                        if text[i] == "\\":
                            i += 2
                            continue
                        if text[i] == "'":
                            i += 1
                            break
                        i += 1
                    self.setFormat(start, i - start, self.string_format)
                    continue

                # Double-quoted string: "..."
                if ch == '"':
                    start = i
                    i += 1
                    while i < length:
                        if text[i] == "\\":
                            i += 2
                            continue
                        if text[i] == '"':
                            i += 1
                            break
                        i += 1
                    self.setFormat(start, i - start, self.string_format)
                    continue

                # Comments (only reached if not inside string)
                if ch == '#':
                    self.setFormat(i, length - i, self.comment_format)
                    break

                # Integers
                m = self.integer_boolean_regex.match(text, i)
                if m:
                    span = m.end() - m.start()
                    self.setFormat(i, span, self.integer_boolean_format)
                    i = m.end()
                    continue

                # Magic methods
                m = self.magic_methods_regex.match(text, i)
                if m:
                    span = m.end() - m.start()
                    self.setFormat(i, span, self.magic_method_format)
                    i = m.end()
                    continue

                # Functions
                m = self.function_regex.match(text, i)
                if m:
                    span = m.end() - m.start()
                    self.setFormat(i, span, self.function_format)
                    i = m.end()
                    continue

                # self.
                m = self.self_regex.match(text, i)
                if m:
                    span = m.end() - m.start()
                    self.setFormat(i, span, self.self_format)
                    i = m.end()
                    continue

                # Keywords / class names
                if ch.isalpha() or ch == '_':
                    start_word = i
                    while i < length and (text[i].isalnum() or text[i] == '_'):
                        i += 1
                    word = text[start_word:i]

                    if self.waiting_for_class_name:
                        self.setFormat(start_word, len(
                            word), self.class_format)
                        self.waiting_for_class_name = False
                    elif word in self.keywords:
                        self.setFormat(start_word, len(
                            word), self.keyword_format)
                        if word == "class":
                            self.waiting_for_class_name = True
                    continue

                # Nothing special at this char
                i += 1

    def highlight_keywords_and_class_names(self, text: str, start_pos: int, end_pos: int
                                           ) -> None:
        """
        Parses the text chunk [start_pos:end_pos]
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
                    self.setFormat(start_word, len(
                        word), self.keyword_format)
                    if word == "class":
                        self.waiting_for_class_name = True

    def find_unescaped_quote(self, text: str, quote_char: str, start: int) -> int:
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

    def highlight_brackets(self, text: str) -> None:
        brackets = "()[]{}"
        for idx, ch in enumerate(text):
            if ch in brackets:
                self.setFormat(idx, 1, self.bracket_format)
