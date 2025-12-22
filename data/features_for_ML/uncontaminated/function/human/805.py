from typing import Any, Dict, List, Optional, Union

def twitter_tweets_search_recent_get(
        auth: OAuth1AuthConfig,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        client = Executor.create_client(auth, **kwargs)
        return client.search_recent_tweets(query=query, **kwargs)