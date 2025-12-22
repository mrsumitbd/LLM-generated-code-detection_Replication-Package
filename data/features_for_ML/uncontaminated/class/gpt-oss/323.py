import os
import json
import logging
from typing import Dict, Any, List, Optional

import requests
from requests.auth import HTTPBasicAuth

# Assuming WazuhConfig is defined elsewhere with the following attributes:
# host: str
# port: int
# username: Optional[str]
# password: Optional[str]
# ssl_verify: bool
# ssl_ca_path: Optional[str]
# indexer_path: str (e.g., "/")
# timeout: int (seconds)
# headers: Dict[str, str] (optional)

log = logging.getLogger(__name__)


class WazuhIndexerClient:
    """Production-grade client for Wazuh Indexer (OpenSearch/Elasticsearch) API."""

    def __init__(self, config: Any):
        """
        Initialize the client with a configuration object.

        :param config: Configuration object containing connection parameters.
        """
        self.config = config
        self.base_url = f"https://{config.host}:{config.port}{config.indexer_path}"
        self.session = requests.Session()
        if getattr(config, "username", None) and getattr(config, "password", None):
            self.session.auth = HTTPBasicAuth(config.username, config.password)
        self.session.headers.update(getattr(config, "headers", {}))
        self.session.verify = config.ssl_verify
        if config.ssl_verify and config.ssl_ca_path:
            self.session.verify = config.ssl_ca_path
        self._validate_ssl_config()

    def _validate_ssl_config(self):
        """
        Validate SSL configuration. Raises an exception if SSL verification is enabled
        but the CA path does not exist.
        """
        if self.config.ssl_verify:
            ca_path = getattr(self.config, "ssl_ca_path", None)
            if ca_path and not os.path.isfile(ca_path):
                raise ValueError(f"SSL CA file not found: {ca_path}")
        else:
            log.warning("SSL verification is disabled. This is insecure for production.")

    def _validate_response_structure(self, response: Dict[str, Any], endpoint: str):
        """
        Validate that the response from the indexer has the expected structure.

        :param response: JSON-decoded response from the indexer.
        :param endpoint: The endpoint that was queried.
        :raises ValueError: If the response structure is invalid.
        """
        if not isinstance(response, dict):
            raise ValueError(f"Response from {endpoint} is not a JSON object.")
        if "hits" not in response or "hits" not in response["hits"]:
            raise ValueError(f"Response from {endpoint} missing 'hits' structure.")
        if not isinstance(response["hits"]["hits"], list):
            raise ValueError(f"Response from {endpoint} 'hits' is not a list.")

    def _validate_alert_response(self, response: Dict[str, Any]) -> List[str]:
        """
        Validate that the alert response contains alert IDs.

        :param response: JSON-decoded response from the indexer.
        :return: List of alert IDs.
        :raises ValueError: If no alert IDs are found.
        """
        alert_ids = []
        for hit in response["hits"]["hits"]:
            source = hit.get("_source", {})
            alert_id = source.get("alert_id") or source.get("id")
            if alert_id:
                alert_ids.append(str(alert_id))
        if not alert_ids:
            raise ValueError("No alert IDs found in response.")
        return alert_ids

    def _transform_alerts_response(self, indexer_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform the raw alerts response into a simplified structure.

        :param indexer_response: Raw JSON response from the indexer.
        :return: Transformed dictionary containing alert data.
        """
        transformed = {"alerts": []}
        for hit in indexer_response["hits"]["hits"]:
            source = hit.get("_source", {})
            alert = {
                "id": source.get("alert_id") or source.get("id"),
                "timestamp": source.get("timestamp"),
                "rule": source.get("rule", {}).get("id"),
                "description": source.get("rule", {}).get("description"),
                "severity": source.get("rule", {}).get("severity"),
                "source_ip": source.get("source", {}).get("ip"),
                "destination_ip": source.get("destination", {}).get("ip"),
            }
            transformed["alerts"].append(alert)
        return transformed

    def _transform_vulnerabilities_response(self, indexer_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform the raw vulnerabilities response into a simplified structure.

        :param indexer_response: Raw JSON response from the indexer.
        :return: Transformed dictionary containing vulnerability data.
        """
        transformed = {"vulnerabilities": []}
        for hit in indexer_response["hits"]["hits"]:
            source = hit.get("_source", {})
            vuln = {
                "id": source.get("id"),
                "cve": source.get("cve"),
                "severity": source.get("severity"),
                "description": source.get("description"),
                "published": source.get("published"),
                "updated": source.get("updated"),
            }
            transformed["vulnerabilities"].append(vuln)
        return transformed

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                 data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Internal helper to perform HTTP requests.

        :param method: HTTP method (GET, POST, etc.).
        :param endpoint: API endpoint relative to base_url.
        :param params: Query parameters.
        :param data: JSON body.
        :return: JSON-decoded response.
        :raises requests.HTTPError: If the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            resp = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=getattr(self.config, "timeout", 30),
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            log.error(f"Request to {url} failed: {e}")
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """
        Retrieve cluster metrics from the indexer.

        :return: Dictionary containing cluster health and node stats.
        """
        # Cluster health
        health = self._request("GET", "/_cluster/health")
        # Node stats
        nodes = self._request("GET", "/_nodes/stats")
        return {"health": health, "nodes": nodes}