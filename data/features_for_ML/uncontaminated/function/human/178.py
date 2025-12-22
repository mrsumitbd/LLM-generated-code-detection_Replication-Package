from django.http import Http404, HttpRequest, HttpResponse

def _default_http_error(
    request: HttpRequest, exc: HttpError, api: "NinjaAPI"
) -> HttpResponse:
    return api.create_response(request, {"detail": str(exc)}, status=exc.status_code)