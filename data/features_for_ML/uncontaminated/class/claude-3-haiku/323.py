import requests
from typing import Dict, Any, List
from .wazuh_config import WazuhConfig

class WazuhIndexerClient:
    """Production-grade client for Wazuh Indexer (OpenSearch/Elasticsearch) API."""

    def __init__(self, config: WazuhConfig):
        self.config = config
        self._validate_ssl_config()
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        if self.config.ssl_verify:
            self.session.verify = self.config.ssl_ca_path
        else:
            self.session.verify = False

    def _validate_ssl_config(self):
        if self.config.ssl_verify and not self.config.ssl_ca_path:
            raise ValueError("SSL verification is enabled, but no SSL CA path is provided.")

    def _validate_response_structure(self, response: Dict[str, Any], endpoint: str):
        if 'hits' not in response or 'total' not in response['hits']:
            raise ValueError(f"Invalid response structure for endpoint: {endpoint}")

    def _validate_alert_response(self, response: Dict[str, Any]) -> List[str]:
        errors = []
        if 'hits' not in response or 'hits' not in response['hits']:
            errors.append("Invalid alert response structure.")
        return errors

    def _transform_alerts_response(self, indexer_response: Dict[str, Any]) -> Dict[str, Any]:
        transformed_response = {
            'total_alerts': indexer_response['hits']['total'],
            'alerts': [hit['_source'] for hit in indexer_response['hits']['hits']]
        }
        return transformed_response

    def _transform_vulnerabilities_response(self, indexer_response: Dict[str, Any]) -> Dict[str, Any]:
        transformed_response = {
            'total_vulnerabilities': indexer_response['hits']['total'],
            'vulnerabilities': [hit['_source'] for hit in indexer_response['hits']['hits']]
        }
        return transformed_response

    def get_metrics(self) -> Dict[str, Any]:
        endpoint = f"{self.config.indexer_url}/_cluster/health"
        response = self.session.get(endpoint).json()
        self._validate_response_structure(response, endpoint)
        return response