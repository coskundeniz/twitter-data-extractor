from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from twitter_api_service import TwitterAPIService


class BaseExtractor(ABC):
    """Base class for extractors"""

    @abstractmethod
    def extract_data(self, api_service: TwitterAPIService) -> Optional[Union[Any, list[Any]]]:
        """Extract data for users, friends, followers, or tweets"""
