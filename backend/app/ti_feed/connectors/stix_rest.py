import requests
from typing import Iterator, Dict, Any
from app.ti_feed.connectors.base import FeedConnector

class STIX21RESTConnector(FeedConnector):
    """
    Connects to a REST API providing STIX 2.1 bundles.
    Expects STIX objects (indicators, malware, threat-actors).
    """

    def connect(self) -> bool:
        if not self.feed_config.source_uri:
            raise ValueError("Source URI must be provided for REST Connector.")
        
        # Test connection (e.g. TAXII discovery or generic REST ping)
        headers = self._get_auth_headers()
        response = requests.get(self.feed_config.source_uri, headers=headers, timeout=10)
        # Some APIs return 401/403 if unauthorized, so raise for those
        response.raise_for_status()
        return True

    def _get_auth_headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/stix+json;version=2.1"}
        
        if self.auth_config:
            auth_type = self.auth_config.get("type")
            if auth_type == "bearer":
                headers["Authorization"] = f"Bearer {self.auth_config.get('token')}"
            elif auth_type == "api_key":
                key_name = self.auth_config.get("key_name", "X-API-Key")
                headers[key_name] = self.auth_config.get("api_key")
                
        return headers

    def fetch(self, since: str = None) -> Iterator[Dict[str, Any]]:
        headers = self._get_auth_headers()
        params = {}
        if since:
            params["added_after"] = since # TAXII style param
            
        response = requests.get(self.feed_config.source_uri, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        bundle = response.json()
        
        if bundle.get("type") == "bundle" and "objects" in bundle:
            for obj in bundle["objects"]:
                # We mainly care about indicators for the feed, but could process others
                if obj.get("type") == "indicator":
                    yield self._map_stix_indicator(obj)
        elif isinstance(bundle, list):
             # Some custom REST APIs return a list of STIX objects directly
             for obj in bundle:
                 if obj.get("type") == "indicator":
                    yield self._map_stix_indicator(obj)

    def _map_stix_indicator(self, stix_obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps a STIX 2.1 Indicator to our internal format.
        """
        return {
            "value": stix_obj.get("pattern"), # In STIX 2.1, value is often in the pattern (e.g. [ipv4-addr:value = '...'])
            "type": "STIX Pattern", # Will require a complex normalizer to parse STIX patterns
            "stix_id": stix_obj.get("id"),
            "valid_from": stix_obj.get("valid_from"),
            "raw_data": stix_obj
        }

    def get_health(self) -> Dict[str, Any]:
        try:
            self.connect()
            return {"status": "healthy", "error": None}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
