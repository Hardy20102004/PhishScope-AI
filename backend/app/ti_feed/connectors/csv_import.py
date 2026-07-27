import csv
import io
import requests
from typing import Iterator, Dict, Any
from app.ti_feed.connectors.base import FeedConnector

class CSVImportConnector(FeedConnector):
    """
    Connects to a CSV file either via URL or local path.
    Requires 'indicator_column' and optionally 'type_column' in connector_config.
    """

    def connect(self) -> bool:
        if not self.feed_config.source_uri:
            raise ValueError("Source URI must be provided for CSV Import.")
        
        # Test connection if it's an HTTP URL
        if self.feed_config.source_uri.startswith(('http://', 'https://')):
            response = requests.head(self.feed_config.source_uri, timeout=10)
            response.raise_for_status()
        return True

    def fetch(self, since: str = None) -> Iterator[Dict[str, Any]]:
        uri = self.feed_config.source_uri
        
        if uri.startswith(('http://', 'https://')):
            response = requests.get(uri, stream=True, timeout=30)
            response.raise_for_status()
            
            # Read lines decoding as utf-8
            lines = (line.decode('utf-8') for line in response.iter_lines())
            reader = csv.DictReader(lines)
            
            for row in reader:
                yield self._map_row(row)
        else:
            # Assume local file import
            with open(uri, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield self._map_row(row)

    def _map_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Maps CSV row to a standard internal representation.
        """
        indicator_col = self.connector_config.get("indicator_column", "indicator")
        type_col = self.connector_config.get("type_column", "type")
        
        return {
            "value": row.get(indicator_col),
            "type": row.get(type_col, "Unknown"), # The normalization engine will handle translation
            "raw_data": row
        }

    def get_health(self) -> Dict[str, Any]:
        try:
            self.connect()
            return {"status": "healthy", "error": None}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
