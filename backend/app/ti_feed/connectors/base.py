from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any, List
from app.ti_feed.models import FeedRegistry

class FeedConnector(ABC):
    """
    Abstract base class for all Feed Connectors.
    A connector is responsible for connecting to a source, fetching data,
    and yielding normalized standard dictionaries containing indicators.
    """

    def __init__(self, feed_config: FeedRegistry):
        self.feed_config = feed_config
        self.auth_config = feed_config.auth_config or {}
        self.connector_config = feed_config.connector_config or {}

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection or verify credentials.
        Returns True if successful, raises Exception otherwise.
        """
        pass

    @abstractmethod
    def fetch(self, since: str = None) -> Iterator[Dict[str, Any]]:
        """
        Fetches data from the source and yields individual records or chunks.
        `since` can be used for incremental updates.
        The yielded dictionaries should contain raw indicators that can be mapped.
        """
        pass

    @abstractmethod
    def get_health(self) -> Dict[str, Any]:
        """
        Returns health status of the connector.
        """
        pass
