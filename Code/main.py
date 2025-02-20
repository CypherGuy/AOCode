import sys
from PySide6 import QtWidgets, QtCore, QtGui
from AoCFetcher import fetch_input, fetch_problem, get_last_paragraph
from Highlighter import PythonHighlighter
from PySide6.QtGui import QFont, QTextCursor, QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize
from exec import execute_code, submit_answer
from utils import Utils
import config
import Preferences


class AoCEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1200, 1000)
        self.setWindowTitle("AoCode")

        self.session_cookie = self.get_session_token()
        config.TOKEN = self.session_cookie

        if not self.session_cookie:
            QtWidgets.QMessageBox.critical(
                self, "No Session Token", "A valid session token is required to continue."
            )
            QtWidgets.QApplication.instance().quit()

        main_layout = QtWidgets.QVBoxLayout(self)

        # Row 1: Hint, Settings, Dropdowns, Run Button
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

        self.settings_button = QtWidgets.QPushButton(self)
        self.settings_button.clicked.connect(self.toggle_preferences)
        self.settings_button.setIcon(QIcon("Code/images/cog.png"))
        self.settings_button.setIconSize(QSize(24, 24))
        self.settings_button.setFixedSize(32, 32)
        dropdown_layout.addWidget(self.settings_button)

        dropdown_layout.addWidget(QtWidgets.QLabel("Year:"))

        self.year_dropdown = QtWidgets.QComboBox()
        self.year_dropdown.setFixedWidth(77)
        current_year = str(QtCore.QDate.currentDate().year())
        self.year_dropdown.addItems([str(y)
                                    for y in range(2015, int(current_year) + 1)])
        self.year_dropdown.setCurrentText(
            str(int(current_year) + 1))
        dropdown_layout.addWidget(self.year_dropdown)

        dropdown_layout.addWidget(QtWidgets.QLabel("Day:"))
        self.day_dropdown = QtWidgets.QComboBox()
        self.day_dropdown.setFixedWidth(58)
        current_day = str(QtCore.QDate.currentDate().day())
        self.day_dropdown.addItems([str(d) for d in range(1, 26)])
        self.day_dropdown.setCurrentText(
            str(current_day) if int(current_day) <= 25 else "1")
        dropdown_layout.addWidget(self.day_dropdown)

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setFixedSize(50, 50)
        self.run_button.setStyleSheet(
            "border-radius: 25px; background-color: lightgray;"
        )
        self.run_button.setIcon(self.create_triangle_icon())
        self.run_button.setIconSize(QtCore.QSize(40, 40))
        dropdown_layout.addWidget(self.run_button)

        self.run_button.clicked.connect(self.run_code)

        row1_layout.addLayout(dropdown_layout, 0, 1)
        main_layout.addLayout(row1_layout)

        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.setFixedSize(80, 50)
        self.submit_button.setText("Submit")
        self.submit_button.clicked.connect(self.handle_submit_button)
        dropdown_layout.addWidget(self.submit_button)

        # Row 2: Problem Description and Code/Terminal Section
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.problem_tabs = QtWidgets.QTabWidget()
        self.part1_panel = QtWidgets.QTextEdit()
        self.part2_panel = QtWidgets.QTextEdit()
        self.utils_panel = QtWidgets.QTextEdit()

        self.utilsEditor = Utils(self.utils_panel)

        for panel in [self.part1_panel, self.part2_panel, self.utils_panel]:
            panel.setStyleSheet("background-color: #f0f0f0; color: black;")

        self.utils_panel.setPlaceholderText(
            self.utilsEditor.default_template)

        self.part1_panel.setReadOnly(True)
        self.part2_panel.setReadOnly(True)

        self.input_panel = QtWidgets.QTextEdit()
        self.input_panel.setStyleSheet(
            "background-color: #ffffff; color: black;"
        )

        self.problem_tabs.addTab(self.part1_panel, "Part 1")
        self.problem_tabs.addTab(self.part2_panel, "Part 2")
        self.problem_tabs.addTab(self.input_panel, "Your input")
        self.problem_tabs.addTab(self.utils_panel, "Utils File")

        left_layout.addWidget(self.problem_tabs)
        main_splitter.addWidget(left_widget)

        self.year, self.day, self.part = self.get_info()
        config.CURRENT_DAY = self.day
        config.CURRENT_YEAR = self.year
        config.CURRENT_PART = self.part

        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        self.code_editor = QtWidgets.QTextEdit()
        self.code_editor.setPlaceholderText("Write your code here...")
        self.preferences_panel = Preferences.Preferences(
            editor=self.code_editor, console=self, token=config.TOKEN)

        # Set tab width to exactly 4 spaces
        metrics = QtGui.QFontMetrics(QFont("Arial", 12))
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
        self.preferences_panel.editor = self.code_editor

        self.year_dropdown.currentIndexChanged.connect(
            self.update_problem_description
        )
        self.day_dropdown.currentIndexChanged.connect(
            self.update_problem_description
        )

        self.update_problem_description()
        self.problem_tabs.currentChanged.connect(self.update_hint)

    def toggle_preferences(self):
        if self.preferences_panel.isVisible():
            self.close_preferences()
        else:
            self.open_preferences()

    def open_preferences(self):
        self.preferences_panel.show()

    def close_preferences(self):
        self.preferences_panel.close()

    def handle_submit_button(self):
        # Handles the submit button action
        year, day, part = config.CURRENT_YEAR, config.CURRENT_DAY, config.CURRENT_PART
        submit_answer(year, day, part, self.session_cookie,
                      self.terminal.toPlainText(), self.terminal, self)

    def get_info(self):
        # Get the currently selected tab index
        current_tab = self.problem_tabs.currentIndex()

        # Determine the part based on the index
        if current_tab == 0:
            part = "1"
        elif current_tab == 1:
            part = "2"
        else:
            QtWidgets.QMessageBox.warning(
                self, "Invalid Tab", "You must be on either Part 1 or Part 2 to submit. Look on the tabs to the left."
            )
            return

        # Retrieve year and day
        year = self.year_dropdown.currentText()
        day = self.day_dropdown.currentText()
        return year, day, part

    def run_code(self):
        code = self.code_editor.toPlainText().strip()

        if not code:
            self.terminal.setPlainText("Error: No code to execute!")
            return

        output = execute_code(code)
        self.terminal.setPlainText(output)

    def eventFilter(self, obj, event):
        if obj == self.code_editor and event.type() == QtCore.QEvent.KeyPress:
            match event.key():
                case QtCore.Qt.Key_V if event.modifiers() == QtCore.Qt.ControlModifier:
                    text = QApplication.clipboard().text()
                    highlighter = PythonHighlighter(obj.document())
                    highlighter.highlightBlock(text)
                    font = QFont("Menlo", 14)
                    obj.setFont(font)
                    obj.insertPlainText(text)
                    return True

                case QtCore.Qt.Key_Tab:
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

                case QtCore.Qt.Key_Backtab:
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

                case QtCore.Qt.Key_Return | QtCore.Qt.Key_Enter:
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

        config.CURRENT_YEAR = year
        config.CURRENT_DAY = day

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
            config.CURRENT_PART = 1
            last_sentence = get_last_paragraph(
                self.part1_panel.toPlainText()
            )
            self.hint_box.setPlainText(last_sentence)
        elif index == 1:
            config.CURRENT_PART = 2
            last_sentence = get_last_paragraph(
                self.part2_panel.toPlainText()
            )
            self.hint_box.setPlainText(last_sentence)

    def get_session_token(parent=None):
        while True:
            dialog = QtWidgets.QDialog(parent)
            dialog.setWindowTitle("Session Token Required")
            dialog.setWindowFlags(
                QtCore.Qt.Dialog |
                QtCore.Qt.WindowStaysOnTopHint |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint
            )
            dialog.setModal(True)

            layout = QtWidgets.QVBoxLayout(dialog)

            label = QtWidgets.QLabel(
                "Please enter your Advent of Code session token (128 characters):"
            )

            layout.addWidget(label)

            session_input = QtWidgets.QLineEdit()
            session_input.setEchoMode(QtWidgets.QLineEdit.Password)
            session_input.setPlaceholderText("Session Token (128 characters)")
            layout.addWidget(session_input)

            submit_button = QtWidgets.QPushButton("Submit")
            layout.addWidget(submit_button)

            valid_token = [None]

            def handle_submit():
                token = session_input.text().strip()
                if len(token) == 128 and token.isalnum():
                    valid_token[0] = token
                    dialog.accept()
                else:
                    QtWidgets.QMessageBox.warning(
                        dialog, "Invalid Session",
                        "Invalid session token. Please ensure it is exactly 128 alphanumeric characters and try again."
                    )

            submit_button.clicked.connect(handle_submit)
            dialog.exec()

            if valid_token[0]:
                return valid_token[0]

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
