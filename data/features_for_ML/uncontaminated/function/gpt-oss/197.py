from django.http import JsonResponse

def get(request):
    """
    Handle a GET request and return the query parameters as JSON.
    """
    # Extract query parameters from the request
    params = request.GET.dict()

    # Prepare the response data
    response_data = {
        "status": "success",
        "params": params
    }

    # Return a JSON response
    return JsonResponse(response_data)