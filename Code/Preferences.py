import os
import json
import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QComboBox, QPushButton, QTextEdit, QMessageBox, QColorDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
import config


class Preferences(QWidget):
    def __init__(self, editor: QTextEdit, console: QTextEdit, token: str) -> None:
        super().__init__()

        self.editor: QTextEdit = editor
        self.token: str = token
        self.console: QTextEdit = console
        self.user_id: str = self.generate_user_id(token)
        self.preferences_dir: str = os.path.join("user_files", self.user_id)
        self.preferences_path: str = os.path.join(
            self.preferences_dir, "preferences.json")

        self.default_template: dict = self.get_template()

        self.add_user()
        self.setWindowTitle("Preferences")
        self.setGeometry(300, 300, 400, 200)

        splitter = QSplitter(Qt.Horizontal)

        main_layout = QVBoxLayout()
        main_layout.addWidget(
            QLabel("Here you can preview and save your preferences"))
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

    def create_editor_preferences_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)

        layout.addWidget(QLabel("Code Editor"))

        layout.addWidget(QLabel("Theme"))
        self.editor_theme = QComboBox()
        self.editor_theme.addItems(
            ["Default", "Light", "Dark", "Solarized", "Monokai", "Custom", "Change Custom"])

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

    def create_console_preferences_panel(self) -> QWidget:
        panel: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout(panel)

        layout.addWidget(QLabel("Console"))

        layout.addWidget(QLabel("Theme"))
        self.console_theme: QComboBox = QComboBox()
        self.console_theme.addItems(
            ["Default", "Light", "Dark", "Solarized", "Monokai", "Custom", "Change Custom"])
        self.console_theme.currentTextChanged.connect(
            self.apply_console_preferences)
        layout.addWidget(self.console_theme)

        return panel

    def generate_user_id(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def add_user(self) -> None:
        os.makedirs(self.preferences_dir, exist_ok=True)
        if not os.path.exists(self.preferences_path):
            with open(self.preferences_path, "w") as f:
                f.write(self.default_template)

    def load_file(self) -> None:
        try:
            with open(self.preferences_path, "r") as f:
                preferences = json.load(f)

            self.editor_font.setCurrentText(
                preferences["code_editor_preferences"]["Font"])

            editor_theme = preferences["code_editor_preferences"]["Theme"]
            # If the theme starts with #, it's a custom color
            if editor_theme.startswith('#'):
                self.editor_theme.setCurrentText("Custom")
            else:
                self.editor_theme.setCurrentText(editor_theme)

            console_theme = preferences["console_preferences"]["Theme"]
            if console_theme.startswith('#'):
                self.console_theme.setCurrentText("Custom")
            else:
                self.console_theme.setCurrentText(console_theme)

        except FileNotFoundError as e:
            QMessageBox.warning(
                self, "Could not load Preferences", f"Failed to load preferences. Error: {e}"
            )
            self.editor_font.setCurrentText("Menlo")
            self.editor_theme.setCurrentText("Default")
            self.console_theme.setCurrentText("Default")

    def get_content(self) -> str | QMessageBox:
        try:
            with open(self.preferences_path, "r") as f:
                return f.read()
        except Exception as e:
            QMessageBox.critical(
                None, "Error", f"Failed to load Preferences.py in get_content: {e}"
            )

    def save_file(self) -> QMessageBox:
        try:
            with open(self.preferences_path, "r") as f:
                preferences = json.load(f)

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

            QMessageBox.information(
                self, "Success", "Preferences saved successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(
                None, "Error", f"Failed to save Preferences.py: {e}"
            )

    def get_template(self) -> str:
        return json.dumps({
            "code_editor_preferences": {
                "Theme": "Default",
                "Font": "Menlo"
            },
            "console_preferences": {
                "Theme": "Default",
            }
        }, indent=4)

    def apply_editor_preferences(self) -> None:
        """Apply preferences to the editor (GUI)."""
        theme = self.editor_theme.currentText()
        with open(self.preferences_path, "r") as f:
            preferences = json.load(f)

        if theme != "Custom" and theme != "Change Custom":
            self.editor.setStyleSheet(config.THEMES[theme])
        else:
            try:
                if theme == "Change Custom":
                    color = QColorDialog.getColor()
                    if not color.isValid():
                        return

                    preferences["code_editor_preferences"]["Theme"] = color.name()
                    with open(self.preferences_path, "w") as f:
                        json.dump(preferences, f, indent=4)

                    self.editor.setStyleSheet(
                        f"background-color: {color.name()}; color: #000000;")
                else:  # theme == "Custom"

                    current_theme = preferences["code_editor_preferences"]["Theme"]
                    # If this is a fresh "Custom" selection or not a hex color
                    if not current_theme.startswith('#'):
                        color = QColorDialog.getColor()
                        if not color.isValid():
                            return

                        # Save the hex color directly
                        preferences["code_editor_preferences"]["Theme"] = color.name()
                        with open(self.preferences_path, "w") as f:
                            json.dump(preferences, f, indent=4)
                    else:
                        # Use the existing hex color
                        color = QColor(current_theme)

                    self.editor.setStyleSheet(
                        f"background-color: {color.name()}; color: #000000;")

            except Exception as e:
                print(f"Error applying editor preferences: {e}")
                self.editor.setStyleSheet(config.THEMES["Default"])

        font = QFont(preferences["code_editor_preferences"]["Font"], 15)
        font.setFixedPitch(True)
        self.editor.setFont(font)

    def apply_console_preferences(self) -> None:
        """Apply preferences to the console (GUI)."""
        theme = self.console_theme.currentText()

        with open(self.preferences_path, "r") as f:
            preferences = json.load(f)

        font = QFont("Menlo", 15)
        font.setFixedPitch(True)
        self.editor.setFont(font)

        if theme != "Custom" and theme != "Change Custom":
            self.console.setStyleSheet(config.THEMES[theme])
        else:
            # If theme is Custom, use the stored hex color
            if theme == "Custom":
                try:
                    theme = preferences["console_preferences"]["Theme"]

                    if theme.startswith('#'):
                        color = QColor(theme)
                        self.console.setStyleSheet(
                            f"background-color: {color.name()}; color: #000000;")
                except Exception as e:
                    self.console.setStyleSheet(config.THEMES["Default"])

            else:  # theme == "Change Custom"
                color = QColorDialog.getColor()
                if not color.isValid():
                    return

                preferences["console_preferences"]["Theme"] = color.name()
                with open(self.preferences_path, "w") as f:
                    json.dump(preferences, f, indent=4)

                self.console.setStyleSheet(
                    f"background-color: {color.name()}; color: #000000;")
