import abc
from typing import Any, Dict


class BaseConnector(abc.ABC):
    """Base class for all threat intelligence connectors."""
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the connector (e.g., 'virustotal')."""
        pass
        
    @abc.abstractmethod
    async def check_health(self) -> bool:
        """Check if the connector is healthy and reachable."""
        pass
        
    @abc.abstractmethod
    async def query(self, indicator_value: str, indicator_type: str) -> Dict[str, Any]:
        """
        Query the intelligence source for the indicator.
        Should return a dictionary with keys:
        - 'reputation_score': float (0-100)
        - 'confidence': float (0-100)
        - 'threat_classification': str or None
        - 'raw_data': dict (the original response)
        """
        pass
