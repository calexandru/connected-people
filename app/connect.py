from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Set

from app.client import ClientException
from app.client import GitHubClient
from app.client import TwitterClient


class UserConnectionException(Exception):
    def __init__(self, errors_list=None):
        self.errors_list = errors_list or []


@dataclass
class ConnectionResult:
    user_1_follows: bool
    user_2_follows: bool
    common_orgs: Set[str]

    @property
    def connected(self) -> bool:
        return self.user_1_follows and self.user_2_follows and bool(self.common_orgs)

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"connected": self.connected}
        if self.connected:
            result["organisations"] = list(self.common_orgs)
        return result


class UsersConnection:
    def __init__(self, user_1_handler: str, user_2_handler: str):
        self.handler_1 = user_1_handler
        self.handler_2 = user_2_handler
        self.github_client = GitHubClient()
        self.twitter_client = TwitterClient()

    def check(self) -> ConnectionResult:
        """Check if two users are connected.

        Raises:
            UserConnectionException: If there is an error while checking the connection.

        Returns:
            ConnectionResult: The result of the connection check.
        """
        user_1_github_orgs = set()
        user_2_github_orgs = set()
        is_user_1_following_user_2_on_twitter = False
        is_user_2_following_user_1_on_twitter = False
        errors = []

        try:
            user_1_github_orgs = self.github_client.get_user_public_organizations(self.handler_1)
        except ClientException as ex:
            errors.append(str(ex))

        try:
            user_2_github_orgs = self.github_client.get_user_public_organizations(self.handler_2)
        except ClientException as ex:
            errors.append(str(ex))

        try:
            is_user_1_following_user_2_on_twitter = self.twitter_client.check_user_follows(
                self.handler_1, self.handler_2
            )
        except ClientException as ex:
            errors.append(str(ex))

        try:
            is_user_2_following_user_1_on_twitter = self.twitter_client.check_user_follows(
                self.handler_2, self.handler_1
            )
        except ClientException as ex:
            errors.append(str(ex))

        if errors:
            raise UserConnectionException(errors)

        return ConnectionResult(
            is_user_1_following_user_2_on_twitter,
            is_user_2_following_user_1_on_twitter,
            user_1_github_orgs & user_2_github_orgs,
        )
