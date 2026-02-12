import unittest
from unittest.mock import patch, MagicMock
from src.data_collection import GitHubFetcher

class TestGitHubFetcher(unittest.TestCase):
    @patch('src.data_collection.requests.get')
    def test_fetch_user_profile_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"login": "testuser", "public_repos": 10}
        mock_get.return_value = mock_response

        fetcher = GitHubFetcher(username="testuser", token="fake_token")
        profile = fetcher.fetch_user_profile()

        self.assertEqual(profile["login"], "testuser")
        self.assertEqual(profile["public_repos"], 10)

    @patch('src.data_collection.requests.get')
    def test_fetch_repositories_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [[{"name": "repo1"}, {"name": "repo2"}], []] # First page has repos, second empty
        mock_get.return_value = mock_response

        fetcher = GitHubFetcher(username="testuser", token="fake_token")
        repos = fetcher.fetch_repositories()

        self.assertEqual(len(repos), 2)
        self.assertEqual(repos[0]["name"], "repo1")

if __name__ == '__main__':
    unittest.main()
