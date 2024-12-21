import sys
from PySide6 import QtWidgets, QtCore


class DraggableLine(QtWidgets.QFrame):
    def __init__(self, orientation, parent=None):
        super().__init__(parent)
        self.setFrameShape(orientation)
        self.setLineWidth(4)
        self.setStyleSheet("background-color: black;")
        self.dragging = False  # Tracks if the line is being dragged

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            parent = self.parentWidget()
            if self.frameShape() == QtWidgets.QFrame.HLine:
                new_y = self.y() + (event.pos().y() - self.start_pos.y())
                new_y = max(0, min(new_y, parent.height() - self.lineWidth()))
                self.setGeometry(
                    self.x(), new_y, self.width(), self.lineWidth())
            elif self.frameShape() == QtWidgets.QFrame.VLine:
                new_x = self.x() + (event.pos().x() - self.start_pos.x())
                new_x = max(0, min(new_x, parent.width() - self.lineWidth()))
                self.setGeometry(
                    new_x, self.y(), self.lineWidth(), self.height())
                # Update connected lines
                if hasattr(parent, "update_connected_lines"):
                    parent.update_connected_lines()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False  # Stop dragging


class BaseLines(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 1000)
        self.setWindowTitle("AoCode")

        # Horizontal line (85% of the height)
        self.horizontal_line = DraggableLine(QtWidgets.QFrame.HLine, self)
        self.horizontal_line.setGeometry(
            0, int(self.height() * 0.85), self.width(), 3)

        # Second horizontal line (10% of the height)
        self.second_horizontal_line = DraggableLine(
            QtWidgets.QFrame.HLine, self)
        self.second_horizontal_line.setGeometry(
            0, int(self.height() * 0.1), self.width(), 3)

        # Vertical line (25% of the width)
        self.vertical_line = DraggableLine(QtWidgets.QFrame.VLine, self)
        self.vertical_line.setGeometry(
            int(self.width() * 0.333333), 0, 3, self.height())

        self.update_connected_lines()  # Initial alignment

    def update_connected_lines(self):
        """Update the second horizontal line to stay connected to the vertical line."""
        vertical_line_x = self.vertical_line.x()  # Get vertical line's position
        self.horizontal_line.setGeometry(
            vertical_line_x,  # Start at the vertical line
            self.horizontal_line.y(),
            self.width() - vertical_line_x,  # Extend to the right edge
            self.horizontal_line.lineWidth(),
        )

    def resizeEvent(self, event):
        """Ensure all lines resize dynamically when the window is resized."""
        # Update horizontal line
        self.horizontal_line.setGeometry(
            0, int(self.height() * 0.85), self.width(), 3
        )

        # Update vertical line
        self.vertical_line.setGeometry(
            self.vertical_line.x(), 0, self.vertical_line.lineWidth(), self.height()
        )

        self.second_horizontal_line.setGeometry(
            0, int(self.height() * 0.1), self.width(), 3
        )

        # Update connected horizontal line
        self.update_connected_lines()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = BaseLines()
    w.show()
    sys.exit(app.exec())
