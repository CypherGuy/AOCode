import pytest
import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout
from Code.ui.infobox import Infobox


@pytest.fixture(scope="module")
def qapp():
    """Create a QApplication instance for all tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def infobox(qapp):
    """Fixture to create an Infobox instance."""
    box = Infobox()
    yield box
    box.close()


def test_infobox_opens(infobox):
    """Test that the Infobox opens successfully."""
    # Qt widgets are hidden by default until .show() is called
    assert not infobox.isVisible(), "Infobox should be hidden on initialization"
    infobox.show()
    assert infobox.isVisible(), "Infobox should be visible after .show()"
    assert infobox.windowTitle() == "Information", "Window title should be 'Information'"


def test_infobox_geometry(infobox):
    """Test that the Infobox has the correct dimensions."""
    geometry = infobox.geometry()
    assert geometry.width() == 500, "Infobox width should be 500"
    assert geometry.height() >= 400, "Infobox height should be at least 400"


def test_infobox_closes(infobox):
    """Test that the Infobox closes properly."""
    # Qt widgets are hidden by default, so show it first
    infobox.show()
    assert infobox.isVisible(), "Infobox should be visible after .show()"

    infobox.close()

    assert not infobox.isVisible(), "Infobox should not be visible after closing"


def test_infobox_has_labels(infobox):
    """Test that the Infobox contains the expected labels."""
    labels = infobox.findChildren(QLabel)

    assert len(labels) >= 3, f"Expected at least 3 labels, found {len(labels)}"

    label_texts = [label.text() for label in labels]

    assert any("Tips" in text for text in label_texts), "Should have 'Tips' label"
    # Features section uses a QPushButton, not a label title


def test_infobox_layout(infobox):
    """Test that the Infobox has a proper layout."""
    assert infobox.layout() is not None, "Infobox should have a layout"
    assert isinstance(infobox.layout(),
                      QVBoxLayout), "Layout should be QVBoxLayout"


def test_infobox_multiple_instances(qapp):
    """Test that multiple Infobox instances can be created and closed."""
    infobox1 = Infobox()
    infobox2 = Infobox()

    # Qt widgets are hidden by default
    assert not infobox1.isVisible(), "First infobox should be hidden on initialization"
    assert not infobox2.isVisible(), "Second infobox should be hidden on initialization"

    infobox1.show()
    infobox2.show()

    assert infobox1.isVisible(), "First infobox should be visible after .show()"
    assert infobox2.isVisible(), "Second infobox should be visible after .show()"

    infobox1.close()
    assert not infobox1.isVisible(), "First infobox should be closed"
    assert infobox2.isVisible(), "Second infobox should still be visible"

    infobox2.close()
    assert not infobox2.isVisible(), "Second infobox should be closed"


def test_infobox_toggle_features(infobox):
    """Test that the features section can be toggled."""
    # Show the parent widget first (required for child visibility in Qt)
    infobox.show()

    # Initially, features should be hidden
    assert not infobox.features_label.isVisible(), "Features should be hidden initially"
    assert infobox.features_button.text(
    ) == "Show Features", "Button should say 'Show Features'"

    # Toggle to show
    infobox.toggle_features()
    assert infobox.features_label.isVisible(), "Features should be visible after toggle"
    assert infobox.features_button.text(
    ) == "Hide Features", "Button should say 'Hide Features'"

    # Toggle to hide
    infobox.toggle_features()
    assert not infobox.features_label.isVisible(
    ), "Features should be hidden after second toggle"
    assert infobox.features_button.text(
    ) == "Show Features", "Button should say 'Show Features' again"
