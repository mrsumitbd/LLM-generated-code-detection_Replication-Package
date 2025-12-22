def get(request):
    """
    Retrieves data from a server based on the provided request.

    Args:
        request (dict): A dictionary containing the necessary information to make the request, such as the URL, headers, and any query parameters.

    Returns:
        dict: A dictionary containing the response data from the server.
    """
    import requests

    try:
        response = requests.get(**request)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error retrieving data: {e}")