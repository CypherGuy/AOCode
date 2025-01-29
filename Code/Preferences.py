import os
import json
import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QSplitter
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class Preferences(QWidget):
    def __init__(self, editor, console, token):
        super().__init__()

        self.editor = editor
        self.token = token
        self.console = console
        self.user_id = self.generate_user_id(token)
        self.preferences_dir = os.path.join("user_files", self.user_id)
        self.preferences_path = os.path.join(
            self.preferences_dir, "preferences.json")

        self.default_template = self.get_template()

        self.add_user()
        self.setWindowTitle("Preferences")
        self.setGeometry(300, 300, 400, 200)

        splitter = QSplitter(Qt.Horizontal)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)

        splitter.addWidget(self.create_editor_preferences_panel())
        splitter.addWidget(self.create_console_preferences_panel())

        save = QPushButton("Save")
        save.clicked.connect(self.save_file)
        main_layout.addWidget(save)

        self.setLayout(main_layout)

        self.load_file()

        self.apply_console_preferences()
        self.apply_editor_preferences()

    def create_editor_preferences_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        layout.addWidget(QLabel("Code Editor"))

        layout.addWidget(QLabel("Theme"))
        self.editor_theme = QComboBox()
        self.editor_theme.addItems(["Default", "Light", "Dark", "Solarized"])
        self.editor_theme.currentTextChanged.connect(
            self.apply_editor_preferences)
        layout.addWidget(self.editor_theme)

        layout.addWidget(QLabel("Font"))
        self.editor_font = QComboBox()
        self.editor_font.addItems(["Arial", "Menlo", "Consolas"])
        self.editor_font.currentTextChanged.connect(
            self.apply_editor_preferences)
        layout.addWidget(self.editor_font)

        return panel

    def create_console_preferences_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        layout.addWidget(QLabel("Console"))

        layout.addWidget(QLabel("Theme"))
        self.console_theme = QComboBox()
        self.console_theme.addItems(["Default", "Light", "Dark", "Solarized"])
        self.console_theme.currentTextChanged.connect(
            self.apply_console_preferences)
        layout.addWidget(self.console_theme)

        return panel

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
                preferences = json.load(f)

            self.editor_font.setCurrentText(
                preferences["code_editor_preferences"]["Font"])
            self.editor_theme.setCurrentText(
                preferences["code_editor_preferences"]["Theme"])
            self.console_theme.setCurrentText(
                preferences["console_preferences"]["Theme"])

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
            eTheme = self.editor_theme.currentText()
            eFont = self.editor_font.currentText()
            cTheme = self.console_theme.currentText()
            preferences = {
                "code_editor_preferences": {
                    "Theme": eTheme,
                    "Font": eFont
                },
                "console_preferences": {
                    "Theme": cTheme,
                }
            }
            with open(self.preferences_path, "w") as f:
                json.dump(preferences, f, indent=4)
            self.apply_editor_preferences()
            self.apply_console_preferences()
            self.close()

        except Exception as e:
            QMessageBox.critical(
                None, "Error", f"Failed to save Preferences.py: {e}"
            )

    def get_template(self):
        return json.dumps({
            "code_editor_preferences": {
                "Theme": "Default",
                "Font": "Menlo"
            },
            "console_preferences": {
                "Theme": "Default",
            }
        }, indent=4)

    def apply_editor_preferences(self):
        """Apply preferences to the editor."""

        theme = self.editor_theme.currentText()
        fontType = self.editor_font.currentText()

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
            self.editor.setStyleSheet(
                "background-color: #ffffff; color: black;")

    def apply_console_preferences(self):
        """Apply preferences to the console (GUI)."""

        theme = self.console_theme.currentText()

        # Just to be sure
        font = QFont("Arial", 12)
        font.setFixedPitch(True)
        self.console.setFont(font)

        if theme == "Dark":
            self.console.setStyleSheet(
                "background-color: #1E1E1E; color: #FFFFFF;")
        elif theme == "Light":
            self.console.setStyleSheet(
                "background-color: #FFFFFF; color: #000000;")
        elif theme == "Solarized":
            self.console.setStyleSheet(
                "background-color: #002b36; color: #839496;")
        else:
            self.console.setStyleSheet(
                "background-color: #303030; color: white;")
