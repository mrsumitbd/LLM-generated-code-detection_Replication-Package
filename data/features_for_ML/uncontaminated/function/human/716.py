from aw.api_endpoints.base import get_api_user, HDR_CACHE_1W, GenericResponse, API_PERMISSION
from aw.model.job import Job, JobUserCredentials, Repository, JobSharedCredentials
from rest_framework.response import Response

def get(request):
        user = get_api_user(request)
        return Response(data=_build_model_defaults_choices(Repository, user), status=200)