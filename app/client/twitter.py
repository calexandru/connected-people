import logging

from tweepy import Client
from tweepy import TweepyException

from app import settings
from app.client.exceptions import GenericException
from app.client.exceptions import InvalidUserException

logger = logging.getLogger(__name__)


class TwitterClient:
    def __init__(self, twitter_token: str = settings.TWITTER_ACCESS_TOKEN):
        self.access_token = twitter_token
        self._client = Client(bearer_token=twitter_token, wait_on_rate_limit=True)

    def get_user_id_by_handler(self, user_handler: str) -> int:
        """Find the user id for a Twitter user handler.

        Args:
            user_handler (str): Twitter user handler

        Raises:
            InvalidUserException: Exception raised when the user is not found.
            GenericException: Exception raised when the request fails.

        Returns:
            int: Twitter user id.
        """
        try:
            response = self._client.get_user(username=user_handler)
            if response.data is None:
                raise InvalidUserException(f"{user_handler} is not a valid user in twitter")
            return response.data.id
        except TweepyException as ex:
            logger.error(
                "Failed to fetch details for Twitter user '%s'. Reason: %s", user_handler, ex
            )
            raise GenericException(f"ailed to fetch details for twiter user {user_handler}")

    def check_user_follows(self, user_handler: str, follow_handler: str) -> bool:
        """Find if a user follows another user on Twitter.

        Args:
            user_handler (str): Twitter user handler
            follow_handler (str): Twitter user handler

        Raises:
            GenericException: Exception raised when the request fails.

        Returns:
            bool: True if the user follows the other user, False otherwise.
        """
        pagination_token = None
        try:
            user_id = self.get_user_id_by_handler(user_handler)
            while True:
                response = self._client.get_users_following(
                    user_id, pagination_token=pagination_token, max_results=1000
                )
                if response.data:
                    if any(map(lambda x: x.username == follow_handler, response.data)):
                        return True
                    if pagination_token := response.meta.get("next_token"):
                        continue  # continue to next page
                break  # bail out - nothing else to see here folks
        except TweepyException as ex:
            logger.error(
                "Failed to fetch users following for Twitter user '%s'. Reason: %s",
                user_handler,
                ex,
            )
            raise GenericException(f"failed to fetch users following for twiter user {user_id}")
        return False
