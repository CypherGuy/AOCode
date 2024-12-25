import sys
from PySide6 import QtWidgets, QtCore, QtGui


class AoCEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1200, 1000)
        self.setWindowTitle("Advent of Code IDE")

        main_layout = QtWidgets.QVBoxLayout(self)

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

        self.problem_tabs.setStyleSheet("""
            QTabBar::tab {
                background: #dcdcdc;
                padding: 5px;
                font-size: 14px;

            }
            QTabBar::tab:selected {
                background: #b0b0b0;
            }
            QTabBar::tab:hover {
                background: #c4c4c4;
            }
        """)

        left_layout.addWidget(self.problem_tabs)

        main_splitter.addWidget(left_widget)

        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        # Top Section (Code Editor + Run Button)
        top_right_widget = QtWidgets.QWidget()
        top_right_layout = QtWidgets.QVBoxLayout(top_right_widget)
        top_right_layout.setContentsMargins(0, 0, 0, 0)

        top_bar = QtWidgets.QHBoxLayout()
        top_bar.addStretch(1)

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setFixedSize(50, 50)
        self.run_button.setStyleSheet(
            "border-radius: 25px; background-color: lightgray;")
        self.run_button.setIcon(self.create_triangle_icon())
        self.run_button.setIconSize(QtCore.QSize(40, 40))
        self.run_button.clicked.connect(self.on_run_clicked)
        top_bar.addWidget(self.run_button)

        self.code_editor = QtWidgets.QTextEdit()
        self.code_editor.setPlaceholderText("Write your code here...")
        top_right_layout.addLayout(top_bar)
        top_right_layout.addWidget(self.code_editor)

        # Add Top Section to Splitter
        right_splitter.addWidget(top_right_widget)

        self.terminal = QtWidgets.QTextEdit()
        self.terminal.setPlaceholderText("Output will appear here...")
        right_splitter.addWidget(self.terminal)

        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([400, 800])
        right_splitter.setSizes([800, 200])

        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

        self.part_descriptions = {
            "Part 1": "Part 1",
            "Part 2": "Part 2"
        }
        self.update_description(0)  # Load Part 1 description initially
        self.problem_tabs.currentChanged.connect(self.update_description)

    def create_triangle_icon(self):
        """Create a triangle-shaped 'Run' icon for the button."""
        pixmap = QtGui.QPixmap(50, 50)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("black")))
        painter.setPen(QtCore.Qt.NoPen)

        points = [
            QtCore.QPoint(10, 10),
            QtCore.QPoint(40, 25),
            QtCore.QPoint(10, 40),
        ]
        painter.drawPolygon(QtGui.QPolygon(points))
        painter.end()

        return QtGui.QIcon(pixmap)

    def update_description(self, index):
        """Update the problem description based on the selected tab."""
        tab_name = self.problem_tabs.tabText(index)
        description = self.part_descriptions.get(tab_name, "")

        if index == 0:
            self.part1_panel.setPlainText(description)
            self.part1_panel.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOn)

        else:
            self.part2_panel.setPlainText(description)
            self.part2_panel.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOn)

    def on_run_clicked(self):
        """Action when the Run button is clicked."""
        print("Run button clicked!")
        self.terminal.append("Running your solution...\n")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AoCEditor()
    window.show()
    sys.exit(app.exec())
