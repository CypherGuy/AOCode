import unittest
from unittest.mock import MagicMock, patch
from Code.runner import submit_answer


class TestSubmitAnswer(unittest.TestCase):
    @patch('requests.post')
    def test_successful_submission_correct_answer(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<article><p>That\'s the right answer</p></article>'
        mock_post.return_value = mock_response

        terminal = MagicMock()
        instance = MagicMock()
        instance.get_info.return_value = (None, None, '1')
        instance.problem_tabs = MagicMock()

        submit_answer(2022, 1, '1', 'token', 'answer', terminal, instance)

        terminal.append.assert_called_with(
            '<span style="color: green;">------That\'s the right answer</span>')
        instance.problem_tabs.setCurrentIndex.assert_called_with(1)

    @patch('requests.post')
    def test_successful_submission_incorrect_answer(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<article><p>Incorrect answer</p></article>'
        mock_post.return_value = mock_response

        terminal = MagicMock()
        instance = MagicMock()
        instance.get_info.return_value = (None, None, '1')
        instance.problem_tabs = MagicMock()

        submit_answer(2022, 1, '1', 'token', 'answer', terminal, instance)

        terminal.append.assert_called_with(
            '<span style="color: red;">------Incorrect answer</span>')

    @patch('requests.post')
    def test_failed_submission_invalid_session_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_post.return_value = mock_response

        terminal = MagicMock()
        instance = MagicMock()
        instance.get_info.return_value = (None, None, '1')
        instance.problem_tabs = MagicMock()

        submit_answer(2022, 1, '1', 'invalid_token',
                      'answer', terminal, instance)

        terminal.append.assert_called_with('Error: Received status code 403')

    @patch('requests.post')
    def test_failed_submission_invalid_url(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        terminal = MagicMock()
        instance = MagicMock()
        instance.get_info.return_value = (None, None, '1')
        instance.problem_tabs = MagicMock()

        submit_answer(2022, 1, '1', 'token', 'answer', terminal, instance)

        terminal.append.assert_called_with('Error: Received status code 404')

    @patch('requests.post')
    def test_failed_submission_missing_article_or_p_tag(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_post.return_value = mock_response

        terminal = MagicMock()
        instance = MagicMock()
        instance.get_info.return_value = (None, None, '1')
        instance.problem_tabs = MagicMock()

        submit_answer(2022, 1, '1', 'token', 'answer', terminal, instance)

        terminal.append.assert_called_with(
            'Error: Could not find <article> tag in response.')

    @patch('requests.post')
    def test_successful_submission_part1_correct_answer_auto_switch_to_part2(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<article><p>Answer submitted successfully! That\'s the right answer.</p></article>'
        mock_post.return_value = mock_response

        terminal = MagicMock()
        instance = MagicMock()
        instance.get_info.return_value = (None, None, '1')
        instance.problem_tabs = MagicMock()

        submit_answer(2022, 1, '1', 'token', 'answer', terminal, instance)

        instance.problem_tabs.setCurrentIndex.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()
