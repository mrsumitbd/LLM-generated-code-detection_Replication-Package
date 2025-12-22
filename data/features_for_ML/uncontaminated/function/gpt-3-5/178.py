def _default_http_error(request: HttpRequest, exc: HttpError, api: "NinjaAPI") -> HttpResponse:
    import json
    from django.http import HttpResponse

    error_message = {"error": str(exc)}
    return HttpResponse(json.dumps(error_message), status=exc.status_code)