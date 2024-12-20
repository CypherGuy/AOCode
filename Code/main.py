import sys
from PySide6 import QtWidgets, QtCore


class BaseLines(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 1000)
        self.setWindowTitle("AoCode")

        # Horizontal line (85% of the height)
        self.horizontal_line = QtWidgets.QFrame(self)
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setLineWidth(3)

        # Second horizontal line (10% of the height)
        self.second_horizontal_line = QtWidgets.QFrame(self)
        self.second_horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.second_horizontal_line.setLineWidth(3)

        # Vertical line 1 (25% of the width)
        self.vertical_line1 = QtWidgets.QFrame(self)
        self.vertical_line1.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line1.setLineWidth(3)

        # Set initial positions for all lines
        self.update_horizontal_line(0.85)
        self.update_second_horizontal_line(0.1)
        self.update_vertical_line(self.vertical_line1, 0.25)

    def update_horizontal_line(self, amountFromTop):
        """Update the position of the horizontal line."""
        window_width = self.width()
        window_height = self.height()
        start_x = int(window_width * 0.25)
        line_y = int(window_height * amountFromTop)
        self.horizontal_line.setGeometry(
            start_x, line_y, window_width - start_x, self.horizontal_line.lineWidth()
        )

    def update_second_horizontal_line(self, amountFromTop):
        """Update the position of the second horizontal line."""
        window_width = self.width()
        line_y = int(self.height() * amountFromTop)
        self.second_horizontal_line.setGeometry(
            0, line_y, window_width, self.second_horizontal_line.lineWidth()
        )

    def update_vertical_line(self, line, amountFromLeft):
        """Update the position of a vertical line."""
        window_width = self.width()
        window_height = self.height()
        line_x = int(window_width * amountFromLeft)  # Line position
        line.setGeometry(line_x, 0, line.lineWidth(), window_height)

    def resizeEvent(self, event):
        """Ensure all lines resize dynamically when the window is resized."""
        self.update_horizontal_line(0.85)
        self.update_second_horizontal_line(
            0.1)
        self.update_vertical_line(self.vertical_line1, 0.25)
        super().resizeEvent(event)  # Call the base class's resizeEvent


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = BaseLines()
    w.show()
    sys.exit(app.exec())
