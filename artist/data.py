"""Data Retriever to use to get MRF information."""
from abc import ABC, abstractmethod

import epics


class AbstractDataRetriever(ABC):
    """Abstract base class for retrieving data.

    Attributes:
        data_source: The data source from which to retrieve data.

    Methods:
        get(): Retrieve and return the data from the specified source.

    """

    @abstractmethod
    def get(self) -> type:
        """Retrieve data from the source and return it.

        Returns:
            type: The retrieved data in its native form (can be any type).

        """
class ChannelAccessRetriever(AbstractDataRetriever):
    """Class for retrieving data using Channel Access protocol."""

    def get(self, channel_name: str, as_string: bool = False) -> type:
        """Retrieve the latest value from the Channel Access channel."""
        return epics.caget(channel_name,as_string,timeout=2)
