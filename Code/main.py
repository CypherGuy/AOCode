import sys
from PySide6 import QtWidgets, QtCore, QtGui


class AoCEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1200, 1000)
        self.setWindowTitle("Advent of Code IDE")

        # Overall layout for the window
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QHBoxLayout(top_widget)
        top_layout.setContentsMargins(10, 10, 10, 10)
        top_layout.setSpacing(10)

        self.part_tabs = QtWidgets.QTabWidget()
        self.part_tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: none;
                background: none;
            }
            QTabBar::tab {
                background-color: #3a3a3a;
                color: #ffffff;
                padding: 8px 16px;
                border: 1px solid #2f2f2f;
            }
            QTabBar::tab:selected {
                background-color: #505050;
                color: #ffffff;
            }
            """
        )

        self.add_part_tab("Part 1", "Description for part 1")
        self.add_part_tab("Part 2", "Description for part 2")

        top_layout.addWidget(self.part_tabs)
        top_layout.addStretch(1)

        self.run_button = QtWidgets.QPushButton()
        self.run_button.setFixedSize(35, 35)
        self.run_button.setStyleSheet(
            "border-radius: 17px; background-color: #888;")
        self.run_button.setIcon(self.create_triangle_icon())
        self.run_button.setIconSize(QtCore.QSize(20, 20))
        self.run_button.clicked.connect(self.on_run_clicked)
        top_layout.addWidget(self.run_button)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QtWidgets.QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(10, 0, 10, 10)
        bottom_layout.setSpacing(0)

        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # part description on the left
        self.part_panel = QtWidgets.QTextEdit()
        self.part_panel.setPlaceholderText(
            "Part description (Read-Only)")
        self.part_panel.setReadOnly(True)
        self.part_panel.setStyleSheet(
            "background-color: white; color: black;")
        main_splitter.addWidget(self.part_panel)

        # Code editor + terminal on the right
        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.code_editor = QtWidgets.QTextEdit()
        self.code_editor.setPlaceholderText("Write your code here...")
        self.code_editor.setStyleSheet(
            "background-color: #1e1e1e; color: #cccccc;")
        right_splitter.addWidget(self.code_editor)
        self.terminal = QtWidgets.QTextEdit()
        self.terminal.setPlaceholderText("Output will appear here...")
        self.terminal.setStyleSheet(
            "background-color: #1e1e1e; color: #cccccc;")
        right_splitter.addWidget(self.terminal)
        main_splitter.addWidget(right_splitter)

        main_splitter.setSizes([300, 900])
        right_splitter.setSizes([800, 200])

        # Add horizontal splitter to the bottom widget layout
        bottom_layout.addWidget(main_splitter)

        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        vertical_splitter.addWidget(top_widget)
        vertical_splitter.addWidget(bottom_widget)
        main_layout.addWidget(vertical_splitter)
        self.setLayout(main_layout)

        # Update part description on tab change
        self.part_tabs.currentChanged.connect(
            self.update_part_description)

    def add_part_tab(self, title, content):
        """Add a tab for the given part, stored in self.part_panel"""
        tab = QtWidgets.QWidget()
        tab.setProperty("description", content)
        self.part_tabs.addTab(tab, title)

    def update_part_description(self):
        """On tab switch, update user text."""
        current_tab = self.part_tabs.currentWidget()
        if current_tab:
            description = current_tab.property("description")
            self.part_panel.setText(description)

    def create_triangle_icon(self):
        """Make triangle"""
        pixmap = QtGui.QPixmap(50, 50)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("white")))
        painter.setPen(QtCore.Qt.NoPen)
        points = [
            QtCore.QPoint(10, 10),
            QtCore.QPoint(40, 25),
            QtCore.QPoint(10, 40),
        ]
        painter.drawPolygon(QtGui.QPolygon(points))
        painter.end()
        return QtGui.QIcon(pixmap)

    def on_run_clicked(self):
        """Handle Run button click."""
        print("Run button clicked!")
        self.terminal.append("Running your solution...\n")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AoCEditor()
    window.show()
    sys.exit(app.exec())
