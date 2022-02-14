import pytest

from app.client import ClientException
from app.client import GitHubClient


class TestGitHubClient:
    def test_one_organization(self, requests_mock):
        # GIVEN
        requests_mock.get(
            f"{GitHubClient.BASE_API_URL}/users/test_user/orgs",
            json=[
                {
                    "login": "audiencetradingplatform",
                    "id": 4127819,
                    "node_id": "MDEyOk9yZ2FuaXphdGlvbjQxMjc4MTk=",
                    "url": "https://api.github.com/orgs/audiencetradingplatform",
                    "description": "",
                }
            ],
        )

        # WHEN
        client = GitHubClient()
        orgs = client.get_user_public_organizations("test_user")

        # THEN
        assert orgs == {"audiencetradingplatform"}

    def test_call_with_no_data(self, requests_mock):
        # GIVEN
        requests_mock.get(
            f"{GitHubClient.BASE_API_URL}/users/test_user/orgs",
            json=[],
        )

        # WHEN
        client = GitHubClient()
        orgs = client.get_user_public_organizations("test_user")

        # THEN
        assert orgs == set()

    def test_multiple_organizations(self, requests_mock):
        # GIVEN
        requests_mock.get(
            f"{GitHubClient.BASE_API_URL}/users/test_user/orgs",
            json=[
                {
                    "login": "audiencetradingplatform",
                    "id": 4127819,
                    "node_id": "MDEyOk9yZ2FuaXphdGlvbjQxMjc4MTk=",
                    "url": "https://api.github.com/orgs/audiencetradingplatform",
                    "description": "",
                },
                {
                    "login": "django",
                    "id": 4127600,
                    "node_id": "DEFyOk9yZ2FuaXphdGlvbjQxMjcDEF=",
                    "url": "https://api.github.com/orgs/django",
                    "description": "",
                },
                {
                    "login": "python",
                    "id": 4127500,
                    "node_id": "ABCyOk9yZ2FuaXphdGlvbjQxMjc4ABC=",
                    "url": "https://api.github.com/orgs/python",
                    "description": "",
                },
            ],
        )

        # WHEN
        client = GitHubClient()
        orgs = client.get_user_public_organizations("test_user")

        # THEN
        assert orgs == {"django", "python", "audiencetradingplatform"}

    def test_missing_user(self, requests_mock):
        # GIVEN
        requests_mock.get(f"{GitHubClient.BASE_API_URL}/users/fake_user/orgs", status_code=404)

        # WHEN
        client = GitHubClient()

        # THEN
        with pytest.raises(ClientException) as ex:
            client.get_user_public_organizations("fake_user")

        assert str(ex.value) == "fake_user is not a valid user in github"
