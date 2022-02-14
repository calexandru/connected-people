import pytest

from app.connect import ClientException
from app.connect import GitHubClient
from app.connect import TwitterClient
from app.connect import UserConnectionException
from app.connect import UsersConnection


class TestConnect:
    def test_not_connected(self, monkeypatch):
        # GIVEN
        def mock_orgs(instance, handler):
            return {
                "foo_user": {"org_1", "org_2"},
                "baz_user": {"org_9", "org_8"},
            }.get(handler, set())

        def mock_follow(instance, handler_1, handler_2):
            return {
                ("foo_user", "baz_user"): True,
                ("baz_user", "foo_user"): False,
            }.get((handler_1, handler_2), False)

        monkeypatch.setattr(GitHubClient, "get_user_public_organizations", mock_orgs)
        monkeypatch.setattr(TwitterClient, "check_user_follows", mock_follow)
        # WHEN
        connection = UsersConnection("foo_user", "baz_user")
        result = connection.check()
        # THEN
        assert not result.connected
        assert result.to_dict() == {"connected": False}

    def test_connected(self, monkeypatch):
        # GIVEN
        def mock_orgs(instance, handler):
            return {
                "foo_user": {"org_1", "org_2"},
                "bar_user": {"org_9", "org_2", "org_8"},
            }.get(handler, set())

        def mock_follow(instance, handler_1, handler_2):
            return {
                ("foo_user", "bar_user"): True,
                ("bar_user", "foo_user"): True,
            }.get((handler_1, handler_2), False)

        monkeypatch.setattr(GitHubClient, "get_user_public_organizations", mock_orgs)
        monkeypatch.setattr(TwitterClient, "check_user_follows", mock_follow)
        # WHEN
        connection = UsersConnection("foo_user", "bar_user")
        result = connection.check()
        # THEN
        assert result.connected
        assert result.to_dict() == {"connected": True, "organisations": ["org_2"]}

    def test_error(self, monkeypatch):
        # GIVEN
        def mock_orgs(instance, handler):
            raise ClientException(f"{handler} is not a valid user in github")

        def mock_follow(instance, handler_1, handler_2):
            return True

        monkeypatch.setattr(GitHubClient, "get_user_public_organizations", mock_orgs)
        monkeypatch.setattr(TwitterClient, "check_user_follows", mock_follow)
        # WHEN
        connection = UsersConnection("foo_user", "bar_user")
        # THEN
        with pytest.raises(UserConnectionException) as ex:
            connection.check()

        assert set(ex.value.errors_list) == {
            "foo_user is not a valid user in github",
            "bar_user is not a valid user in github",
        }
