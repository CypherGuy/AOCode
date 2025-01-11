import re
import sys
from PySide6 import QtWidgets, QtCore, QtGui
from AoCFetcher import fetch_input, fetch_problem, get_last_paragraph
from codeEditor import PythonHighlighter
from PySide6.QtGui import QFont, QTextCursor
from exec import execute_code


class AoCEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1200, 1000)
        self.setWindowTitle("Advent of Code IDE")

        self.session_cookie = self.prompt_for_session()

        main_layout = QtWidgets.QVBoxLayout(self)

        # Row 1: Hint, Dropdowns, Run Button
        row1_layout = QtWidgets.QGridLayout()
        row1_layout.setContentsMargins(0, 0, 0, 0)

        self.hint_box = QtWidgets.QTextEdit()
        self.hint_box.setReadOnly(True)
        self.hint_box.setFixedHeight(50)
        self.hint_box.setFixedWidth(500)
        self.hint_box.setStyleSheet(
            "background-color: #f0f0f0; color: black; font-size: 14px; border: 1px solid #ccc;"
        )

        row1_layout.addWidget(self.hint_box, 0, 0)

        dropdown_layout = QtWidgets.QHBoxLayout()
        dropdown_layout.addStretch(1)
        dropdown_layout.addWidget(QtWidgets.QLabel("Year:"))

        self.year_dropdown = QtWidgets.QComboBox()
        self.year_dropdown.addItems([str(y) for y in range(2015, 2025)])
        current_year = str(QtCore.QDate.currentDate().year())
        if current_year in [str(y) for y in range(2015, 2025)]:
            self.year_dropdown.setCurrentText(current_year)
        dropdown_layout.addWidget(self.year_dropdown)

        dropdown_layout.addWidget(QtWidgets.QLabel("Day:"))
        self.day_dropdown = QtWidgets.QComboBox()
        self.day_dropdown.addItems([str(d) for d in range(1, 26)])
        current_day = str(QtCore.QDate.currentDate().day())
        if current_day in [str(d) for d in range(1, 26)]:
            self.day_dropdown.setCurrentText(current_day)
        dropdown_layout.addWidget(self.day_dropdown)

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setFixedSize(50, 50)
        self.run_button.setStyleSheet(
            "border-radius: 25px; background-color: lightgray;"
        )
        self.run_button.setIcon(self.create_triangle_icon())
        self.run_button.setIconSize(QtCore.QSize(40, 40))
        dropdown_layout.addWidget(self.run_button)

        # Execute code and put output in terminal after pressing run button
        self.run_button.clicked.connect(self.run_code)

        row1_layout.addLayout(dropdown_layout, 0, 1)
        main_layout.addLayout(row1_layout)

        # Row 2: Problem Description and Code/Terminal Section
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.problem_tabs = QtWidgets.QTabWidget()
        self.part1_panel = QtWidgets.QTextEdit()
        self.part2_panel = QtWidgets.QTextEdit()

        for panel in [self.part1_panel, self.part2_panel]:
            panel.setReadOnly(True)
            panel.setStyleSheet("background-color: #f0f0f0; color: black;")

        self.input_panel = QtWidgets.QTextEdit()
        self.input_panel.setPlaceholderText("Enter your custom input here...")
        self.input_panel.setStyleSheet(
            "background-color: #ffffff; color: black;"
        )

        self.problem_tabs.addTab(self.part1_panel, "Part 1")
        self.problem_tabs.addTab(self.part2_panel, "Part 2")
        self.problem_tabs.addTab(self.input_panel, "Your input")

        left_layout.addWidget(self.problem_tabs)
        main_splitter.addWidget(left_widget)

        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        self.code_editor = QtWidgets.QTextEdit()
        self.code_editor.setPlaceholderText("Write your code here...")
        self.code_editor.setStyleSheet(
            "background-color: #1E1E1E; color: #FFFFFF;")

        font = QFont("Menlo", 14)
        font.setFixedPitch(True)
        self.code_editor.setFont(font)

        # Set tab width to exactly 4 spaces
        metrics = QtGui.QFontMetrics(font)
        self.code_editor.setTabStopDistance(metrics.horizontalAdvance(' ') * 4)

        right_splitter.addWidget(self.code_editor)
        self.highlighter = PythonHighlighter(self.code_editor.document())

        self.terminal = QtWidgets.QTextEdit()
        self.terminal.setPlaceholderText("Output will appear here...")
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet(
            "background-color: #f0f0f0; color: black;"
        )
        right_splitter.addWidget(self.terminal)

        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([400, 800])
        right_splitter.setSizes([800, 200])

        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

        self.code_editor.installEventFilter(self)

        self.year_dropdown.currentIndexChanged.connect(
            self.update_problem_description
        )
        self.day_dropdown.currentIndexChanged.connect(
            self.update_problem_description
        )

        self.update_problem_description()
        self.problem_tabs.currentChanged.connect(self.update_hint)

    def run_code(self):
        code = self.code_editor.toPlainText().strip()

        if not code:
            self.terminal.setPlainText("Error: No code to execute!")
            return

        output = execute_code(code)
        self.terminal.setPlainText(output)

    def eventFilter(self, obj, event):
        if obj == self.code_editor and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab:
                cursor = self.code_editor.textCursor()
                if cursor.hasSelection():
                    # Handle block indentation
                    start = cursor.selectionStart()
                    end = cursor.selectionEnd()
                    cursor.setPosition(start)
                    cursor.movePosition(QTextCursor.StartOfBlock)
                    while cursor.position() <= end:
                        cursor.insertText('    ')
                        end += 4
                        if not cursor.movePosition(QTextCursor.NextBlock):
                            break
                else:
                    cursor.insertText('    ')
                return True

            elif event.key() == QtCore.Qt.Key_Backtab:
                cursor = self.code_editor.textCursor()
                if cursor.hasSelection():
                    # Handle block dedentation
                    start = cursor.selectionStart()
                    end = cursor.selectionEnd()
                    cursor.setPosition(start)
                    cursor.movePosition(QTextCursor.StartOfBlock)
                    while cursor.position() <= end:
                        line_text = cursor.block().text()
                        if line_text.startswith('    '):
                            cursor.movePosition(
                                QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 4)
                            cursor.removeSelectedText()
                            end -= 4
                        if not cursor.movePosition(QTextCursor.NextBlock):
                            break
                else:
                    cursor = self.code_editor.textCursor()
                    block_text = cursor.block().text()
                    if block_text.startswith('    '):
                        cursor.movePosition(QTextCursor.StartOfBlock)
                        cursor.movePosition(
                            QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 4)
                        cursor.removeSelectedText()
                return True

            elif event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                cursor = self.code_editor.textCursor()
                current_block = cursor.block().text()
                stripped_line = current_block.rstrip()

                indentation = self.get_current_indentation(stripped_line)
                n = indentation.count('    ')

                if stripped_line.endswith(':'):
                    new_indentation = ' ' * 4 * (n + 1)
                else:
                    new_indentation = indentation

                cursor.insertText('\n' + new_indentation)
                return True

        return super().eventFilter(obj, event)

    def get_current_indentation(self, line: str) -> str:
        indentation = ""
        for char in line:
            if char == ' ':
                indentation += char
            elif char == '\t':
                indentation += '    '
            else:
                break
        return indentation

    def update_problem_description(self):
        year = self.year_dropdown.currentText()
        day = self.day_dropdown.currentText()

        part1_text, part2_text = fetch_problem(year, day, self.session_cookie)

        self.part1_panel.setPlainText(part1_text)
        self.part2_panel.setPlainText(part2_text)

        user_input = fetch_input(year, day, self.session_cookie)
        self.input_panel.setPlainText(user_input)

        last_sentence = get_last_paragraph(part1_text)
        self.hint_box.setPlainText(last_sentence)

        self.problem_tabs.setCurrentIndex(0)

    def update_hint(self, index):
        if index == 0:
            last_sentence = get_last_paragraph(
                self.part1_panel.toPlainText()
            )
        else:
            last_sentence = get_last_paragraph(
                self.part2_panel.toPlainText()
            )

        self.hint_box.setPlainText(last_sentence)

    def prompt_for_session(self):
        self.dialog = QtWidgets.QDialog(self)
        self.dialog.setWindowTitle("Session Token Required")

        self.dialog.setWindowFlags(
            QtCore.Qt.Dialog |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint
        )
        self.dialog.setModal(True)

        layout = QtWidgets.QVBoxLayout(self.dialog)

        label = QtWidgets.QLabel(
            "Please enter your Advent of Code session token:"
        )
        layout.addWidget(label)

        self.session_input = QtWidgets.QLineEdit()
        self.session_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.session_input.setPlaceholderText("Session Token (128 characters)")
        layout.addWidget(self.session_input)

        submit_button = QtWidgets.QPushButton("Submit")
        layout.addWidget(submit_button)

        def handle_submit():
            self.session_cookie = self.session_input.text().strip()
            regex = re.compile(r'[^a-zA-Z0-9-_]')

            if regex.search(self.session_cookie) or len(self.session_cookie) != 128:
                QtWidgets.QMessageBox.warning(
                    self, "Invalid Session",
                    "Invalid session token. Please enter a valid 128-character token."
                )
                return

            self.dialog.accept()

        submit_button.clicked.connect(handle_submit)
        self.dialog.exec()
        return self.session_cookie

    def create_triangle_icon(self):
        pixmap = QtGui.QPixmap(50, 50)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("black")))
        painter.setPen(QtCore.Qt.NoPen)
        points = [
            QtCore.QPoint(10, 10),
            QtCore.QPoint(40, 25),
            QtCore.QPoint(10, 40)
        ]
        painter.drawPolygon(QtGui.QPolygon(points))
        painter.end()
        return QtGui.QIcon(pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AoCEditor()
    window.show()
    sys.exit(app.exec())
