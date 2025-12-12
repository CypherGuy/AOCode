import pytest
import json
import os
import sys
import tempfile
import shutil
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication, QTextEdit
from PySide6.QtGui import QColor
from Code.config.preferences import Preferences
import Code.config.config as config


@pytest.fixture(scope="module")
def qapp():
    """Create a QApplication instance for all tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def temp_user_dir():
    """Create a temporary directory for user files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_editor():
    """Create a mock QTextEdit for the editor."""
    return MagicMock(spec=QTextEdit)


@pytest.fixture
def mock_console():
    """Create a mock QTextEdit for the console."""
    return MagicMock(spec=QTextEdit)


@pytest.fixture
def preferences(qapp, mock_editor, mock_console, temp_user_dir):
    """Create a Preferences instance with mocked dependencies."""
    # Use a test token
    test_token = "a" * 128

    prefs = Preferences(editor=mock_editor,
                        console=mock_console, token=test_token)

    # Override the paths to use temp directory instead of the real user_files
    prefs.preferences_dir = os.path.join(temp_user_dir, prefs.user_id)
    prefs.preferences_path = os.path.join(
        prefs.preferences_dir, "preferences.json")

    # Ensure directory exists
    os.makedirs(prefs.preferences_dir, exist_ok=True)

    # Create initial preferences file
    with open(prefs.preferences_path, "w") as f:
        f.write(prefs.default_template)

    yield prefs
    prefs.close()


def test_preferences_initialization(preferences):
    """Test that preferences are initialized correctly."""
    assert preferences.editor is not None
    assert preferences.console is not None
    assert len(preferences.user_id) == 64  # SHA256 hash length
    assert os.path.exists(preferences.preferences_path)


def test_preferences_file_creation(preferences):
    """Test that preferences file is created with default values."""
    assert os.path.exists(preferences.preferences_path)

    with open(preferences.preferences_path, "r") as f:
        data = json.load(f)

    assert "code_editor_preferences" in data
    assert "console_preferences" in data
    assert data["code_editor_preferences"]["Theme"] == "Default"
    assert data["code_editor_preferences"]["Font"] == "Menlo"
    assert data["console_preferences"]["Theme"] == "Default"


def test_load_preferences(preferences):
    """Test that preferences are loaded correctly from file."""
    # Modify the preferences file
    test_prefs = {
        "code_editor_preferences": {
            "Theme": "Dark",
            "Font": "Arial",
            "CustomTheme": "#c2cbc8"
        },
        "console_preferences": {
            "Theme": "Light",
            "CustomTheme": "#000000"
        }
    }

    with open(preferences.preferences_path, "w") as f:
        json.dump(test_prefs, f)

    # Reload preferences
    preferences.load_file()

    assert preferences.editor_theme.currentText() == "Dark"
    assert preferences.editor_font.currentText() == "Arial"
    assert preferences.console_theme.currentText() == "Light"


def test_save_preferences(preferences):
    """Test that preferences are saved correctly to file."""
    # Change some preferences
    preferences.editor_theme.setCurrentText("Dark")
    preferences.editor_font.setCurrentText("Consolas")
    preferences.console_theme.setCurrentText("Monokai")

    # Save
    preferences.save_file()

    # Read back from file
    with open(preferences.preferences_path, "r") as f:
        data = json.load(f)

    assert data["code_editor_preferences"]["Theme"] == "Dark"
    assert data["code_editor_preferences"]["Font"] == "Consolas"
    assert data["console_preferences"]["Theme"] == "Monokai"


def test_apply_editor_theme(preferences):
    """Test that editor theme is applied correctly."""
    # Set theme to Dark
    preferences.editor_theme.setCurrentText("Dark")
    preferences.apply_editor_preferences()

    # Check that setStyleSheet was called with Dark theme
    preferences.editor.setStyleSheet.assert_called()
    call_args = preferences.editor.setStyleSheet.call_args[0][0]
    assert "1E1E1E" in call_args or config.THEMES["Dark"] == call_args


def test_apply_console_theme(preferences):
    """Test that console theme is applied correctly."""
    # Set theme to Solarized
    preferences.console_theme.setCurrentText("Solarized")
    preferences.apply_console_preferences()

    # Check that setStyleSheet was called
    preferences.console.setStyleSheet.assert_called()
    call_args = preferences.console.setStyleSheet.call_args[0][0]
    assert "002b36" in call_args or config.THEMES["Solarized"] == call_args


@pytest.mark.parametrize("theme_name,expected_in_stylesheet", [
    ("Default", "#707070"),
    ("Dark", "#1E1E1E"),
    ("Light", "#c2cbc8"),
    ("Solarized", "#002b36"),
    ("Monokai", "#272822"),
])
def test_apply_different_themes(preferences, theme_name, expected_in_stylesheet):
    """Test that different themes are applied correctly."""
    preferences.editor_theme.setCurrentText(theme_name)
    preferences.apply_editor_preferences()

    preferences.editor.setStyleSheet.assert_called()
    call_args = preferences.editor.setStyleSheet.call_args[0][0]
    assert expected_in_stylesheet in call_args


def test_custom_theme_color(preferences):
    """Test that custom theme colors can be set."""
    # Mock QColorDialog to return a specific color
    with patch('Code.config.preferences.QColorDialog.getColor') as mock_color_dialog:
        mock_color = QColor("#FF5733")
        mock_color_dialog.return_value = mock_color

        preferences.editor_theme.setCurrentText("Change Custom")
        preferences.apply_editor_preferences()

        # Check that custom color was saved
        with open(preferences.preferences_path, "r") as f:
            data = json.load(f)

        assert data["code_editor_preferences"]["CustomTheme"] == "#ff5733"


def test_generate_user_id(preferences):
    """Test that user ID is generated consistently from token."""
    import hashlib
    test_token = "a" * 128
    expected_id = hashlib.sha256(test_token.encode()).hexdigest()

    generated_id = preferences.generate_user_id(test_token)
    assert generated_id == expected_id


def test_preferences_persistence(preferences, temp_user_dir):
    """Test that preferences persist across instances."""
    # Set some preferences
    preferences.editor_theme.setCurrentText("Monokai")
    preferences.editor_font.setCurrentText("Consolas")
    preferences.save_file()
    preferences.close()

    # Create a new instance with the same token
    test_token = "a" * 128
    new_prefs = Preferences(
        editor=MagicMock(spec=QTextEdit),
        console=MagicMock(spec=QTextEdit),
        token=test_token
    )

    # Override paths to use the same temp directory
    new_prefs.preferences_dir = os.path.join(temp_user_dir, new_prefs.user_id)
    new_prefs.preferences_path = os.path.join(
        new_prefs.preferences_dir, "preferences.json")
    new_prefs.load_file()

    # Check that preferences were loaded
    assert new_prefs.editor_theme.currentText() == "Monokai"
    assert new_prefs.editor_font.currentText() == "Consolas"

    new_prefs.close()


def test_invalid_preferences_file(preferences, caplog):
    """Test handling of corrupted preferences file."""
    # Write invalid JSON to preferences file
    with open(preferences.preferences_path, "w") as f:
        f.write("{ invalid json }")

    # Attempt to load - should not crash
    preferences.load_file()

    # Should show warning (captured in caplog or shown to user)


def test_missing_preferences_keys(preferences):
    """Test that missing keys in preferences are handled gracefully."""
    # Write incomplete preferences
    incomplete_prefs = {
        "code_editor_preferences": {
            "Theme": "Dark"
            # Missing Font
        },
        "console_preferences": {}
    }

    with open(preferences.preferences_path, "w") as f:
        json.dump(incomplete_prefs, f)

    # Should not crash when loading
    try:
        preferences.load_file()
    except KeyError:
        pytest.fail("Should handle missing keys gracefully")


def test_preferences_dropdown_options(preferences):
    """Test that all dropdown options are available."""
    # Editor theme options
    editor_themes = [preferences.editor_theme.itemText(i)
                     for i in range(preferences.editor_theme.count())]
    assert "Default" in editor_themes
    assert "Dark" in editor_themes
    assert "Light" in editor_themes
    assert "Custom" in editor_themes

    # Editor font options
    editor_fonts = [preferences.editor_font.itemText(i)
                    for i in range(preferences.editor_font.count())]
    assert "Arial" in editor_fonts
    assert "Menlo" in editor_fonts
    assert "Consolas" in editor_fonts

    # Console theme options
    console_themes = [preferences.console_theme.itemText(i)
                      for i in range(preferences.console_theme.count())]
    assert "Default" in console_themes
    assert "Dark" in console_themes
