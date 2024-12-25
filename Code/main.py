import re
import sys
from PySide6 import QtWidgets, QtCore, QtGui
from AoCFetcher import fetch_problem, extract_last_sentence


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
            "background-color: #f0f0f0; color: black; font-size: 14px; border: 1px solid #ccc;")

        row1_layout.addWidget(self.hint_box, 0, 0)

        dropdown_layout = QtWidgets.QHBoxLayout()
        dropdown_layout.addStretch(1)
        dropdown_layout.addWidget(QtWidgets.QLabel("Year:"))

        self.year_dropdown = QtWidgets.QComboBox()
        self.year_dropdown.addItems([str(y) for y in range(2015, 2025)])
        self.year_dropdown.setCurrentText(
            str(QtCore.QDate.currentDate().year()))
        dropdown_layout.addWidget(self.year_dropdown)

        dropdown_layout.addWidget(QtWidgets.QLabel("Day:"))
        self.day_dropdown = QtWidgets.QComboBox()
        self.day_dropdown.addItems([str(d) for d in range(1, 26)])
        self.day_dropdown.setCurrentText(str(QtCore.QDate.currentDate().day()))
        dropdown_layout.addWidget(self.day_dropdown)

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setFixedSize(50, 50)
        self.run_button.setStyleSheet(
            "border-radius: 25px; background-color: lightgray;")
        self.run_button.setIcon(self.create_triangle_icon())
        self.run_button.setIconSize(QtCore.QSize(40, 40))
        dropdown_layout.addWidget(self.run_button)

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

        self.problem_tabs.addTab(self.part1_panel, "Part 1")
        self.problem_tabs.addTab(self.part2_panel, "Part 2")

        left_layout.addWidget(self.problem_tabs)
        main_splitter.addWidget(left_widget)

        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        self.code_editor = QtWidgets.QTextEdit()
        self.code_editor.setPlaceholderText("Write your code here...")
        right_splitter.addWidget(self.code_editor)

        self.terminal = QtWidgets.QTextEdit()
        self.terminal.setPlaceholderText("Output will appear here...")
        right_splitter.addWidget(self.terminal)

        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([400, 800])
        right_splitter.setSizes([800, 200])

        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

        # If you change the year or day, update the problem description
        self.year_dropdown.currentIndexChanged.connect(
            self.update_problem_description)
        self.day_dropdown.currentIndexChanged.connect(
            self.update_problem_description)

        # Initial fetch
        self.update_problem_description()

        # Update hint if part changes
        self.problem_tabs.currentChanged.connect(self.update_hint)

    def update_problem_description(self):
        """Fetch and update the problem description when year or day changes."""
        year = self.year_dropdown.currentText()
        day = self.day_dropdown.currentText()

        # Fetch problem descriptions
        part1_text, part2_text = fetch_problem(year, day, self.session_cookie)

        self.part1_panel.setPlainText(part1_text)
        self.part2_panel.setPlainText(part2_text)

        last_sentence = extract_last_sentence(part1_text)
        self.hint_box.setPlainText(last_sentence)

        # Show part 1 by default
        self.problem_tabs.setCurrentIndex(0)

    def update_hint(self, index):
        """Update the hint box based on the selected part."""
        if index == 0:
            last_sentence = extract_last_sentence(
                self.part1_panel.toPlainText())
        else:
            last_sentence = extract_last_sentence(
                self.part2_panel.toPlainText())

        self.hint_box.setPlainText(last_sentence)

    def prompt_for_session(self):
        """Prompt the user to input their AoC session token at launch (non-modal)."""
        self.dialog = QtWidgets.QDialog(self)
        self.dialog.setWindowTitle("Session Token Required")
        self.dialog.setModal(False)

        layout = QtWidgets.QVBoxLayout(self.dialog)
        label = QtWidgets.QLabel("Enter AoC Session Cookie:")
        self.session_input = QtWidgets.QLineEdit()
        self.session_input.setEchoMode(QtWidgets.QLineEdit.Password)
        submit_button = QtWidgets.QPushButton("Submit")

        layout.addWidget(label)
        layout.addWidget(self.session_input)
        layout.addWidget(submit_button)

        def handle_submit():
            self.session_cookie = self.session_input.text().strip()
            regex = re.compile(r'[^a-zA-Z0-9-_]')

            if regex.search(self.session_cookie) or len(self.session_cookie) != 128:
                QtWidgets.QMessageBox.warning(
                    self, "Invalid Session",
                    "Invalid session token. Please enter a valid session token without special characters."
                )
                self.dialog.reject()
                return

            self.dialog.accept()
        submit_button.clicked.connect(handle_submit)
        self.dialog.show()
        return None

    def create_triangle_icon(self):
        pixmap = QtGui.QPixmap(50, 50)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("black")))
        painter.setPen(QtCore.Qt.NoPen)
        points = [QtCore.QPoint(10, 10), QtCore.QPoint(
            40, 25), QtCore.QPoint(10, 40)]
        painter.drawPolygon(QtGui.QPolygon(points))
        painter.end()
        return QtGui.QIcon(pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AoCEditor()
    window.show()
    sys.exit(app.exec())
