class WazuhIndexerClient:
    """Production-grade client for Wazuh Indexer (OpenSearch/Elasticsearch) API."""

    def __init__(self, config: WazuhConfig):
        self.config = config
        self.base_url = f"https://{config.indexer_host}:{config.indexer_port}"
        self.session = requests.Session()
        self.session.verify = config.ssl_certificate_verification
        
        if config.ssl_certificate_path:
            self.session.cert = config.ssl_certificate_path
        
        if config.indexer_username and config.indexer_password:
            self.session.auth = (config.indexer_username, config.indexer_password)
        
        self._validate_ssl_config()

    def _validate_ssl_config(self):
        if not self.config.ssl_certificate_verification and not self.config.ssl_certificate_path:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        if self.config.ssl_certificate_path and not os.path.exists(self.config.ssl_certificate_path):
            raise ValueError(f"SSL certificate not found: {self.config.ssl_certificate_path}")

    def _validate_response_structure(self, response: Dict[str, Any], endpoint: str):
        if not isinstance(response, dict):
            raise ValueError(f"Invalid response structure from {endpoint}: expected dict, got {type(response)}")
        
        if "hits" in response and not isinstance(response.get("hits"), dict):
            raise ValueError(f"Invalid 'hits' structure in response from {endpoint}")
        
        if "aggregations" in response and not isinstance(response.get("aggregations"), dict):
            raise ValueError(f"Invalid 'aggregations' structure in response from {endpoint}")

    def _validate_alert_response(self, response: Dict[str, Any]) -> List[str]:
        errors = []
        
        if "hits" not in response:
            errors.append("Missing 'hits' field in alert response")
        elif not isinstance(response["hits"], dict):
            errors.append("'hits' field must be a dictionary")
        else:
            hits = response["hits"]
            if "hits" not in hits:
                errors.append("Missing 'hits.hits' field in alert response")
            elif not isinstance(hits["hits"], list):
                errors.append("'hits.hits' field must be a list")
        
        return errors

    def _transform_alerts_response(self, indexer_response: Dict[str, Any]) -> Dict[str, Any]:
        self._validate_response_structure(indexer_response, "alerts")
        validation_errors = self._validate_alert_response(indexer_response)
        
        if validation_errors:
            raise ValueError(f"Alert response validation failed: {'; '.join(validation_errors)}")
        
        alerts = []
        for hit in indexer_response.get("hits", {}).get("hits", []):
            alert_data = hit.get("_source", {})
            alerts.append({
                "id": hit.get("_id"),
                "index": hit.get("_index"),
                "score": hit.get("_score"),
                "data": alert_data
            })
        
        return {
            "alerts": alerts,
            "total": indexer_response.get("hits", {}).get("total", {}).get("value", 0),
            "took": indexer_response.get("took", 0)
        }

    def _transform_vulnerabilities_response(self, indexer_response: Dict[str, Any]) -> Dict[str, Any]:
        self._validate_response_structure(indexer_response, "vulnerabilities")
        
        vulnerabilities = []
        for hit in indexer_response.get("hits", {}).get("hits", []):
            vuln_data = hit.get("_source", {})
            vulnerabilities.append({
                "id": hit.get("_id"),
                "index": hit.get("_index"),
                "score": hit.get("_score"),
                "data": vuln_data
            })
        
        return {
            "vulnerabilities": vulnerabilities,
            "total": indexer_response.get("hits", {}).get("total", {}).get("value", 0),
            "took": indexer_response.get("took", 0)
        }

    def get_metrics(self) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/_cluster/stats",
                timeout=self.config.request_timeout
            )
            response.raise_for_status()
            
            data = response.json()
            self._validate_response_structure(data, "_cluster/stats")
            
            return {
                "status": "success",
                "cluster_name": data.get("cluster_name"),
                "nodes": data.get("nodes", {}),
                "indices": data.get("indices", {}),
                "timestamp": data.get("timestamp")
            }
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to get metrics from Wazuh Indexer: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Invalid response from Wazuh Indexer: {str(e)}")