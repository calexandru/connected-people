import logging
from typing import Set

import requests

from app.client.exceptions import GenericException
from app.client.exceptions import InvalidUserException

logger = logging.getLogger(__name__)

NOT_FOUND = 404
SUCCESS = 200


class GitHubClient:
    BASE_API_URL = "https://api.github.com"

    def get_user_public_organizations(self, user_handler: str) -> Set[str]:
        """Find all public organizations of a user.

        Args:
            user_handler (str): github user handler

        Raises:
            InvalidUserException: Exception raised when the user is not found.
            GenericException: Exception raised when the request fails.

        Returns:
            Set[str]: Set of organizations.
        """
        orgs: Set[str] = set()
        try:
            response = requests.get(f"{self.BASE_API_URL}/users/{user_handler}/orgs")
            if response.status_code == SUCCESS:
                orgs = set(filter(None, (x.get("login") for x in response.json())))
            elif response.status_code == NOT_FOUND:
                raise InvalidUserException(f"{user_handler} is not a valid user in github")
        except requests.exceptions.RequestException as ex:
            logger.error("Failed to fetch orgs for GitHUb user '%s'. Reason: %s", user_handler, ex)
            raise GenericException(f"failed to fetch github organizations for user {user_handler}")
        return orgs
