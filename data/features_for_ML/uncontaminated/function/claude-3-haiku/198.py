def _add_claims_as_query_param(url: str, claims: Optional[dict[str, str]]) -> str:
    if not claims:
        return url

    query_params = []
    for key, value in claims.items():
        query_params.append(f"{key}={value}")

    if "?" in url:
        return f"{url}&{'&'.join(query_params)}"
    else:
        return f"{url}?{'&'.join(query_params)}"