from typing import Optional

def _add_claims_as_query_param(url: str, claims: Optional[dict[str, str]]) -> str:
    if claims:
        for key, value in claims.items():
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{key}={value}"

    return url