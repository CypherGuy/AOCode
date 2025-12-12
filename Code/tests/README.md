# AOCode Tests

This directory contains the test suite for AOCode, using pytest as the testing framework.

## Running Tests

### Install Dependencies

First, install pytest and required testing packages:

```bash
pip install pytest pytest-qt pytest-mock
```

### Run All Tests

```bash
pytest Code/tests/
```

### Run Specific Test Files

```bash
pytest Code/tests/test_submit_answer.py
pytest Code/tests/test_preferences.py
```

### Run Tests with Verbose Output

```bash
pytest Code/tests/ -v
```

### Run Tests with Coverage (Optional)

If you want to check coverage, install pytest-cov:

```bash
pip install pytest-cov
pytest Code/tests/ --cov=Code --cov-report=html
```

This will generate an HTML coverage report in `htmlcov/index.html`.

## Test Structure

- `test_submit_answer.py` - Tests for answer submission functionality
- `test_get_last_paragraph.py` - Tests for paragraph extraction
- `test_highlight_keywords_and_class_names.py` - Tests for syntax highlighting
- `test_infobox.py` - Tests for the info box UI component
- `test_preferences.py` - Tests for preferences loading/saving

## Writing New Tests

### Using Fixtures

```python
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_terminal():
    """Fixture to create a mock terminal."""
    return MagicMock()

def test_example(mock_terminal):
    # Use the fixture
    assert mock_terminal is not None
```

### Using Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

### For UI Tests (QApplication)

```python
import pytest
import sys
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="module")
def qapp():
    """Create a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

def test_ui_component(qapp):
    # This test can use QApplication
    pass
```

## Running Individual Tests

You can run a specific test function:

```bash
pytest Code/tests/test_submit_answer.py::test_successful_submission_correct_answer
```

Or run tests matching a pattern:

```bash
pytest Code/tests/ -k "preferences"
```
