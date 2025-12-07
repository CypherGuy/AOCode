import os
import json
import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QComboBox, QPushButton, QTextEdit, QMessageBox, QColorDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
import config.config as config


class Preferences(QWidget):
    def __init__(self, editor: QTextEdit, console: QTextEdit, token: str) -> None:
        super().__init__()

        self.editor = editor
        self.console = console
        self.token = token
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
        main_layout.addWidget(QLabel("Live preview • Saves automatically"))
        main_layout.addWidget(splitter)

        splitter.addWidget(self.create_editor_preferences_panel())
        splitter.addWidget(self.create_console_preferences_panel())

        save = QPushButton("Save")
        save.clicked.connect(self.save_file)
        main_layout.addWidget(save)
        self.setLayout(main_layout)

        self.load_file()  # sync dropdowns with saved prefs
        self.apply_editor_preferences()
        self.apply_console_preferences()

    def create_editor_preferences_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)

        layout.addWidget(QLabel("Code Editor"))

        layout.addWidget(QLabel("Theme"))
        self.editor_theme = QComboBox()
        self.editor_theme.addItems(
            ["Default", "Light", "Dark", "Solarized",
                "Monokai", "Custom", "Change Custom"]
        )
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
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("Console"))

        layout.addWidget(QLabel("Theme"))
        self.console_theme = QComboBox()
        self.console_theme.addItems(
            ["Default", "Light", "Dark", "Solarized",
                "Monokai", "Custom", "Change Custom"]
        )
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

            code_theme = preferences["code_editor_preferences"]["Theme"]
            self.editor_theme.setCurrentText(
                "Custom" if code_theme == "Custom" else code_theme)

            console_theme = preferences["console_preferences"]["Theme"]
            self.console_theme.setCurrentText(
                "Custom" if console_theme == "Custom" else console_theme)

        except Exception as e:
            QMessageBox.warning(
                self, "Error loading your preferences:", str(e))

    def save_file(self) -> None:
        try:
            with open(self.preferences_path, "r") as f:
                preferences = json.load(f)

            eTheme = self.editor_theme.currentText()
            eFont = self.editor_font.currentText()
            cTheme = self.console_theme.currentText()

            if eTheme == "Change Custom":
                eTheme = "Custom"
            if cTheme == "Change Custom":
                cTheme = "Custom"

            preferences["code_editor_preferences"]["Theme"] = eTheme
            preferences["code_editor_preferences"]["Font"] = eFont
            preferences["code_editor_preferences"].setdefault(
                "CustomTheme", "#c2cbc8")

            preferences["console_preferences"]["Theme"] = cTheme
            preferences["console_preferences"].setdefault(
                "CustomTheme", "#000000")

            with open(self.preferences_path, "w") as f:
                json.dump(preferences, f, indent=4)

            QMessageBox.information(
                self, "Success", "Preferences saved successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to save your preferences: {str(e)}")

    def apply_editor_preferences(self) -> None:
        with open(self.preferences_path, "r") as f:
            prefs = json.load(f)

        selected_theme = self.editor_theme.currentText()
        custom_hex = prefs["code_editor_preferences"].get(
            "CustomTheme", "#c2cbc8")
        prefs["code_editor_preferences"]["Theme"] = selected_theme
        prefs["code_editor_preferences"]["Font"] = self.editor_font.currentText()

        if selected_theme == "Change Custom":
            color = QColorDialog.getColor()
            if not color.isValid():
                return
            custom_hex = color.name()
            prefs["code_editor_preferences"]["CustomTheme"] = custom_hex
            selected_theme = "Custom"
            self.editor_theme.setCurrentText("Custom")

        if selected_theme == "Custom":
            self.editor.setStyleSheet(
                f"background-color: {custom_hex}; color: #000000;")
        else:
            self.editor.setStyleSheet(config.THEMES.get(
                selected_theme, config.THEMES["Default"]))

        font = QFont(self.editor_font.currentText(), 15)
        font.setFixedPitch(True)
        self.editor.setFont(font)

        with open(self.preferences_path, "w") as f:
            json.dump(prefs, f, indent=4)

    def apply_console_preferences(self) -> None:
        with open(self.preferences_path, "r") as f:
            prefs = json.load(f)

        selected_theme = self.console_theme.currentText()
        custom_hex = prefs["console_preferences"].get("CustomTheme", "#000000")

        prefs["console_preferences"]["Theme"] = selected_theme

        if selected_theme == "Change Custom":
            color = QColorDialog.getColor()
            if not color.isValid():
                return
            custom_hex = color.name()
            prefs["console_preferences"]["CustomTheme"] = custom_hex
            selected_theme = "Custom"
            self.console_theme.setCurrentText("Custom")

        if selected_theme == "Custom":
            self.console.setStyleSheet(
                f"background-color: {custom_hex}; color: #ffffff;")
        else:
            self.console.setStyleSheet(config.THEMES.get(
                selected_theme, config.THEMES["Default"]))

        with open(self.preferences_path, "w") as f:
            json.dump(prefs, f, indent=4)

    def get_template(self) -> str:
        return json.dumps({
            "code_editor_preferences": {
                "Theme": "Default",
                "Font": "Menlo",
                "CustomTheme": "#c2cbc8"
            },
            "console_preferences": {
                "Theme": "Default",
                "CustomTheme": "#000000"
            }
        }, indent=4)
