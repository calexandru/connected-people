import pytest

from app.client import ClientException
from app.client import TwitterClient


class TestTwitterClient:
    def test_get_user_by_handler(self, requests_mock):
        # GIVEN
        requests_mock.get(
            "https://api.twitter.com/2/users/by/username/fake_user",
            json={"data": {"id": "22501696", "name": "Fake User", "username": "fake_user"}},
        )

        # WHEN
        client = TwitterClient()
        twitter_user_id = client.get_user_id_by_handler("fake_user")

        # THEN
        assert twitter_user_id == 22501696

    def test_get_user_by_handler_missing(self, requests_mock):
        # GIVEN
        requests_mock.get(
            "https://api.twitter.com/2/users/by/username/fake_user",
            json={
                "errors": [
                    {
                        "value": "fake_user",
                        "detail": "Could not find user with username: [fake_user].",
                        "title": "Not Found Error",
                        "resource_type": "user",
                        "parameter": "username",
                        "resource_id": "fake_user",
                        "type": "https://api.twitter.com/2/problems/resource-not-found",
                    }
                ]
            },
        )

        # WHEN
        client = TwitterClient()

        # THEN
        with pytest.raises(ClientException) as ex:
            client.get_user_id_by_handler("fake_user")

        assert str(ex.value) == "fake_user is not a valid user in twitter"

    def test_user_follows(self, requests_mock):
        # GIVEN
        requests_mock.get(
            "https://api.twitter.com/2/users/by/username/fake_user",
            json={"data": {"id": "22501696", "name": "Fake User", "username": "fake_user"}},
        )

        requests_mock.get(
            "https://api.twitter.com/2/users/22501696/following?max_results=1000",
            json={
                "data": [
                    {"id": "24500377", "name": "John Doe", "username": "jondoe"},
                    {
                        "id": "187196955",
                        "name": "Another Fake User",
                        "username": "another_fake_user",
                    },
                    {"id": "12497", "name": "John Legend", "username": "jlegend"},
                ]
            },
        )

        # WHEN
        client = TwitterClient()
        follows = client.check_user_follows("fake_user", "another_fake_user")

        # THEN
        assert follows

    def test_user_not_following(self, requests_mock):
        # GIVEN
        requests_mock.get(
            "https://api.twitter.com/2/users/by/username/fake_user",
            json={"data": {"id": "22501696", "name": "Fake User", "username": "fake_user"}},
        )

        requests_mock.get(
            "https://api.twitter.com/2/users/22501696/following?max_results=1000",
            json={
                "data": [
                    {
                        "id": "187196955",
                        "name": "Another Fake User",
                        "username": "another_fake_user",
                    },
                    {"id": "24500377", "name": "John Doe", "username": "jondoe"},
                    {"id": "12497", "name": "John Legend", "username": "jlegend"},
                ]
            },
        )

        # WHEN
        client = TwitterClient()
        follows = client.check_user_follows("fake_user", "rambo")

        # THEN
        assert not follows

    def test_missing_user_follows(self, requests_mock):
        # GIVEN
        requests_mock.get(
            "https://api.twitter.com/2/users/by/username/fake_user",
            json={
                "errors": [
                    {
                        "value": "fake_user",
                        "detail": "Could not find user with username: [fake_user].",
                        "title": "Not Found Error",
                        "resource_type": "user",
                        "parameter": "username",
                        "resource_id": "fake_user",
                        "type": "https://api.twitter.com/2/problems/resource-not-found",
                    }
                ]
            },
        )

        # WHEN
        client = TwitterClient()

        # THEN
        with pytest.raises(ClientException) as ex:
            client.check_user_follows("fake_user", "rambo")

        assert str(ex.value) == "fake_user is not a valid user in twitter"
