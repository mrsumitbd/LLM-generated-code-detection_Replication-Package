from django.http import JsonResponse

def get(request):
    """
    Simple Django view that returns the GET parameters as JSON.
    """
    # Convert QueryDict to a plain dict
    params = request.GET.dict()
    return JsonResponse({"params": params})