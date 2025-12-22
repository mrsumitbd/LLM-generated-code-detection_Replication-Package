class DynamicClientRegistration:
    """Dynamic client registration utility."""

    def __init__(self, config: MCPOAuth2ProviderConfig):
        self.config = config

    def _authorization_base_url(self) -> str:
        return f"{self.config.authorization_endpoint}"

    def register_client(self, client_metadata: dict) -> dict:
        """
        Registers a new OAuth2 client with the authorization server.

        Args:
            client_metadata (dict): A dictionary containing the client metadata.

        Returns:
            dict: A dictionary containing the registered client's information.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(
            self.config.registration_endpoint,
            headers=headers,
            data=json.dumps(client_metadata),
            auth=(self.config.client_id, self.config.client_secret),
        )

        response.raise_for_status()
        return response.json()

    def update_client(self, client_id: str, client_metadata: dict) -> dict:
        """
        Updates an existing OAuth2 client with the authorization server.

        Args:
            client_id (str): The ID of the client to update.
            client_metadata (dict): A dictionary containing the updated client metadata.

        Returns:
            dict: A dictionary containing the updated client's information.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.put(
            f"{self.config.registration_endpoint}/{client_id}",
            headers=headers,
            data=json.dumps(client_metadata),
            auth=(self.config.client_id, self.config.client_secret),
        )

        response.raise_for_status()
        return response.json()

    def delete_client(self, client_id: str) -> None:
        """
        Deletes an existing OAuth2 client from the authorization server.

        Args:
            client_id (str): The ID of the client to delete.
        """
        response = requests.delete(
            f"{self.config.registration_endpoint}/{client_id}",
            auth=(self.config.client_id, self.config.client_secret),
        )

        response.raise_for_status()