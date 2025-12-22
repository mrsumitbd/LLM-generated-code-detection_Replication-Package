import requests
from typing import Dict, Any
from requests_oauthlib import OAuth1

def twitter_tweets_search_recent_get(
        auth: OAuth1AuthConfig,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
    """
    Performs a recent search for tweets based on the provided query.

    Args:
        auth (OAuth1AuthConfig): The OAuth1 authentication configuration.
        query (str): The search query.
        **kwargs: Additional parameters to be passed to the Twitter API.

    Returns:
        Dict[str, Any]: The response from the Twitter API.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": query,
        **kwargs
    }

    response = requests.get(url, params=params, auth=OAuth1(
        auth.consumer_key,
        auth.consumer_secret,
        auth.access_token,
        auth.access_token_secret
    ))

    response.raise_for_status()
    return response.json()