from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseCollector(ABC):
    """
    Abstract base class for all Evidence Collectors.
    """
    
    @abstractmethod
    def collect(self, target: str) -> Dict[str, Any]:
        """
        Executes the collection logic for the specific evidence type.
        Must return a dictionary of collected evidence.
        If it fails, it should return a dict containing an 'error' key.
        """
        pass
