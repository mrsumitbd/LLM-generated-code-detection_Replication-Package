import requests
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class OAuth1AuthConfig:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str

def twitter_tweets_search_recent_get(
        auth: OAuth1AuthConfig,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
    """
    Search for recent tweets using Twitter API v2 with OAuth1 authentication.
    
    Args:
        auth: OAuth1AuthConfig containing Twitter API credentials
        query: Search query string
        **kwargs: Additional parameters like max_results, tweet.fields, etc.
    
    Returns:
        Dictionary containing the API response
    """
    from requests_oauthlib import OAuth1Session
    
    # Create OAuth1 session
    oauth = OAuth1Session(
        client_key=auth.consumer_key,
        client_secret=auth.consumer_secret,
        resource_owner_key=auth.access_token,
        resource_owner_secret=auth.access_token_secret
    )
    
    # Twitter API v2 endpoint for recent search
    url = "https://api.twitter.com/2/tweets/search/recent"
    
    # Prepare parameters
    params = {
        "query": query
    }
    
    # Add any additional parameters
    params.update(kwargs)
    
    # Make the request
    response = oauth.get(url, params=params)
    
    # Return the JSON response
    return response.json()