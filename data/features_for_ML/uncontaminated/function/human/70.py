from rest_framework.response import Response

def get(request):
        del request
        return Response(_get_group_alerts())