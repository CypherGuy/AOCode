import pytest
from unittest.mock import MagicMock, patch
from Code.core.runner import submit_answer


@pytest.fixture
def mock_terminal():
    """Fixture to create a mock terminal."""
    return MagicMock()


@pytest.fixture
def mock_instance():
    """Fixture to create a mock instance with problem_tabs."""
    instance = MagicMock()
    instance.get_info.return_value = (None, None, '1')
    instance.problem_tabs = MagicMock()
    return instance


@patch('Code.core.runner.requests.post')
def test_successful_submission_correct_answer(mock_post, mock_terminal, mock_instance):
    """Test that a correct answer is submitted successfully and shown in green."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<article><p>Answer submitted successfully! That\'s the right answer.</p></article>'
    mock_post.return_value = mock_response

    submit_answer(2022, 1, '1', 'token', 'answer',
                  mock_terminal, mock_instance)

    mock_terminal.append.assert_any_call(
        '<span style="color: green;">------Answer submitted successfully! That\'s the right answer.</span>')
    mock_instance.problem_tabs.setCurrentIndex.assert_called_with(1)


@patch('Code.core.runner.requests.post')
def test_successful_submission_incorrect_answer(mock_post, mock_terminal, mock_instance):
    """Test that an incorrect answer is submitted and shown in red."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<article><p>Incorrect answer</p></article>'
    mock_post.return_value = mock_response

    submit_answer(2022, 1, '1', 'token', 'answer',
                  mock_terminal, mock_instance)

    mock_terminal.append.assert_any_call(
        '<span style="color: red;">------Incorrect answer</span>')


@pytest.mark.parametrize("status_code,expected_message", [
    (403, 'Error: Received status code 403'),
    (404, 'Error: Received status code 404'),
    (500, 'Error: Received status code 500'),
])
@patch('Code.core.runner.requests.post')
def test_failed_submission_http_errors(mock_post, mock_terminal, mock_instance, status_code, expected_message):
    """Test that HTTP errors are handled correctly."""
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_post.return_value = mock_response

    submit_answer(2022, 1, '1', 'token', 'answer',
                  mock_terminal, mock_instance)

    mock_terminal.append.assert_called_with(expected_message)


@patch('Code.core.runner.requests.post')
def test_failed_submission_missing_article_tag(mock_post, mock_terminal, mock_instance):
    """Test that missing article tag in response is handled correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html></html>'
    mock_post.return_value = mock_response

    submit_answer(2022, 1, '1', 'token', 'answer',
                  mock_terminal, mock_instance)

    # Check that an error message about missing article tag was appended
    mock_terminal.append.assert_any_call(
        'Error: Could not find <article> tag in response.')


@patch('Code.core.runner.requests.post')
def test_successful_submission_part1_auto_switch_to_part2(mock_post, mock_terminal, mock_instance):
    """Test that completing part 1 automatically switches to part 2."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<article><p>Answer submitted successfully! That\'s the right answer.</p></article>'
    mock_post.return_value = mock_response

    submit_answer(2022, 1, '1', 'token', 'answer',
                  mock_terminal, mock_instance)

    mock_instance.problem_tabs.setCurrentIndex.assert_called_with(1)
