def _add_claims_as_query_param(url: str, claims: Optional[dict[str, str]]) -> str:
    import json
    import urllib.parse
    
    if not claims:
        return url
    
    claims_json = json.dumps(claims)
    claims_encoded = urllib.parse.quote(claims_json)
    
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}claims={claims_encoded}"