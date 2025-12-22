from django.http import JsonResponse

def get(request):
    """
    Simple Django view that returns the GET parameters as a JSON response.
    """
    # Convert QueryDict to a plain dictionary
    params = request.GET.dict()
    return JsonResponse(params)