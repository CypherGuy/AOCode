import os
import json
import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PySide6 import QtCore


class Preferences(QWidget):
    def __init__(self, editor, token):
        super().__init__()

        self.editor = editor
        self.token = token
        self.user_id = self.generate_user_id(token)
        self.preferences_dir = os.path.join("user_files", self.user_id)
        self.preferences_path = os.path.join(
            self.preferences_dir, "preferences.json")

        self.default_template = self.get_template()

        self.add_user()
        self.load_file()

        self.setWindowTitle("Preferences")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Font"))
        self.fontType = QComboBox()
        self.fontType.addItems(["Arial", "Menlo", "Consolas"])
        self.fontType.currentTextChanged.connect(self.apply_preferences)
        layout.addWidget(self.fontType)

        layout.addWidget(QLabel("Theme"))
        self.theme = QComboBox()
        self.theme.addItems(["Default", "Light", "Dark", "Solarized"])
        self.theme.currentTextChanged.connect(self.apply_preferences)
        layout.addWidget(self.theme)

        save = QPushButton("Save")
        save.clicked.connect(self.save_file)
        layout.addWidget(save)

        self.setLayout(layout)

    def generate_user_id(self, token):
        return hashlib.sha256(token.encode()).hexdigest()

    def add_user(self):
        os.makedirs(self.preferences_dir, exist_ok=True)
        if not os.path.exists(self.preferences_path):
            with open(self.preferences_path, "w") as f:
                f.write(self.default_template)

    def load_file(self):
        try:
            with open(self.preferences_path, "r") as f:
                content = json.load(f)
                fontType, theme = content["Font"], content["Theme"]

            # Apply Preferences here because Python won't let me call apply_preferences
            self.editor.setFont(fontType)
            if theme == "Dark":
                self.editor.setStyleSheet(
                    "background-color: #1E1E1E; color: #FFFFFF;")
            elif theme == "Light":
                self.editor.setStyleSheet(
                    "background-color: #FFFFFF; color: #000000;")
            elif theme == "Solarized":
                self.editor.setStyleSheet(
                    "background-color: #002b36; color: #839496;")
            else:
                self.editor.setStyleSheet("")

        except Exception as e:
            QMessageBox.critical(
                None, "Error", f"Failed to load Preferences.py in load_file: {
                    e}"
            )

    def get_content(self):
        try:
            with open(self.preferences_path, "r") as f:
                return f.read()
        except Exception as e:
            QMessageBox.critical(
                None, "Error", f"Failed to load Preferences.py in get_content: {
                    e}"
            )

    def save_file(self):
        try:
            preferences = {
                "Theme": self.theme.currentText(),
                "Font": self.fontType.currentText()
            }
            with open(self.preferences_path, "w") as f:
                json.dump(preferences, f, indent=4)
            self.apply_preferences()
            self.close()

        except Exception as e:
            QMessageBox.critical(
                None, "Error", f"Failed to save Preferences.py: {e}"
            )

        except Exception as e:
            QMessageBox.critical(
                None, "Error", f"Failed to save Preferences.py: {e}"
            )

    def get_template(self):
        return '''{
    "Theme": "Default",
    "Font": "Menlo"
}'''

    def apply_preferences(self):
        """Apply preferences to the editor."""
        theme = self.theme.currentText()
        font = self.fontType.currentText()

        self.editor.setFont(font)

        if theme == "Dark":
            self.editor.setStyleSheet(
                "background-color: #1E1E1E; color: #FFFFFF;")
        elif theme == "Light":
            self.editor.setStyleSheet(
                "background-color: #FFFFFF; color: #000000;")
        elif theme == "Solarized":
            self.editor.setStyleSheet(
                "background-color: #002b36; color: #839496;")
        else:
            self.editor.setStyleSheet("")
