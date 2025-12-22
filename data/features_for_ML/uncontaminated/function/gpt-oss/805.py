from typing import Dict, Any
import requests
from requests_oauthlib import OAuth1

def twitter_tweets_search_recent_get(
        auth: "OAuth1AuthConfig",
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
    """
    Perform a recent search on Twitter v2 API.

    Parameters
    ----------
    auth : OAuth1AuthConfig
        An object containing OAuth1 credentials with attributes:
        consumer_key, consumer_secret, access_token, access_token_secret.
    query : str
        The search query string.
    **kwargs
        Additional query parameters to pass to the API (e.g., max_results, tweet.fields).

    Returns
    -------
    Dict[str, Any]
        The JSON response from the Twitter API.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"

    # Build query parameters
    params = {"query": query}
    params.update(kwargs)

    # Create OAuth1 authentication object
    oauth = OAuth1(
        auth.consumer_key,
        auth.consumer_secret,
        auth.access_token,
        auth.access_token_secret,
    )

    # Make the request
    response = requests.get(url, params=params, auth=oauth)

    # Raise an error for non-successful status codes
    response.raise_for_status()

    # Return the parsed JSON
    return response.json()