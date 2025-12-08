import sys
import unittest
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout
from Code.ui.infobox import Infobox


class TestInfobox(unittest.TestCase):
    """Test suite for the Infobox widget."""

    @classmethod
    def setUpClass(cls):
        """Create a QApplication instance for all tests."""
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    def test_infobox_opens(self):
        """Test that the Infobox opens successfully."""
        infobox = Infobox()

        # Check that the widget is visible
        self.assertTrue(infobox.isVisible(),
                        "Infobox should be visible after initialization")

        # Check window title
        self.assertEqual(infobox.windowTitle(), "Information",
                         "Window title should be 'Information'")

        # Clean up
        infobox.close()

    def test_infobox_geometry(self):
        """Test that the Infobox has the correct dimensions."""
        infobox = Infobox()

        # Get the geometry set in setGeometry (not the actual window geometry)
        # Using frameGeometry() or geometry() may include window decorations
        # So we'll just check that dimensions are reasonable
        geometry = infobox.geometry()

        # Check that width is 500 and height is at least 400
        # (actual height may be larger due to window decorations/title bar)
        self.assertEqual(geometry.width(), 500, "Infobox width should be 500")
        self.assertGreaterEqual(geometry.height(), 400,
                                "Infobox height should be at least 400")

        # Clean up
        infobox.close()

    def test_infobox_closes(self):
        """Test that the Infobox closes properly."""
        infobox = Infobox()

        # Verify it's initially visible
        self.assertTrue(infobox.isVisible(),
                        "Infobox should be visible initially")

        # Close the infobox
        infobox.close()

        # Verify it's closed
        self.assertFalse(infobox.isVisible(),
                         "Infobox should not be visible after closing")

    def test_infobox_has_labels(self):
        """Test that the Infobox contains the expected labels."""
        infobox = Infobox()

        # Get all child widgets - use QLabel instead of object
        from PySide6.QtCore import QObject
        labels = infobox.findChildren(QLabel)

        # We expect at least 4 labels: 2 titles + 2 content labels
        self.assertGreaterEqual(len(labels), 4,
                                f"Expected at least 4 labels, found {len(labels)}")

        # Check for specific label text
        label_texts = [label.text() for label in labels]

        self.assertTrue(any("Tips and hints" in text for text in label_texts),
                        "Should have 'Tips and hints' label")
        self.assertTrue(any("Features" in text for text in label_texts),
                        "Should have 'Features' label")

        # Clean up
        infobox.close()

    def test_infobox_layout(self):
        """Test that the Infobox has a proper layout."""
        infobox = Infobox()

        # Check that layout exists
        self.assertIsNotNone(infobox.layout(), "Infobox should have a layout")

        # Check layout type
        self.assertIsInstance(infobox.layout(), QVBoxLayout,
                              "Layout should be QVBoxLayout")

        # Clean up
        infobox.close()

    def test_infobox_multiple_instances(self):
        """Test that multiple Infobox instances can be created and closed."""
        infobox1 = Infobox()
        infobox2 = Infobox()

        # Both should be visible
        self.assertTrue(infobox1.isVisible(),
                        "First infobox should be visible")
        self.assertTrue(infobox2.isVisible(),
                        "Second infobox should be visible")

        # Close first one
        infobox1.close()
        self.assertFalse(infobox1.isVisible(),
                         "First infobox should be closed")
        self.assertTrue(infobox2.isVisible(),
                        "Second infobox should still be visible")

        # Close second one
        infobox2.close()
        self.assertFalse(infobox2.isVisible(),
                         "Second infobox should be closed")


if __name__ == "__main__":
    unittest.main()
