def _parser(resp: SyncPageT) -> SyncPageT:
    """
    Parses the response from the server and returns the parsed data.

    Args:
        resp (SyncPageT): The response from the server.

    Returns:
        SyncPageT: The parsed data.
    """
    data = resp.json()
    parsed_data = {
        "page": data["page"],
        "per_page": data["per_page"],
        "total": data["total"],
        "total_pages": data["total_pages"],
        "data": [
            {
                "id": item["id"],
                "email": item["email"],
                "first_name": item["first_name"],
                "last_name": item["last_name"],
                "avatar": item["avatar"],
            }
            for item in data["data"]
        ],
    }
    return SyncPageT(**parsed_data)