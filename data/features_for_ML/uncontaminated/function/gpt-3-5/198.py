def _add_claims_as_query_param(url: str, claims: Optional[dict[str, str]]) -> str:
    if not claims:
        return url
    query_params = '&'.join([f"{key}={value}" for key, value in claims.items()])
    if '?' in url:
        return f"{url}&{query_params}"
    else:
        return f"{url}?{query_params}"