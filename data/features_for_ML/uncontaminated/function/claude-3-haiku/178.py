def _default_http_error(
    request: HttpRequest, exc: HttpError, api: "NinjaAPI"
) -> HttpResponse:
    status_code = exc.status_code
    error_message = str(exc)
    response_data = {
        "error": error_message,
        "status_code": status_code,
    }
    return HttpResponse(
        content=json.dumps(response_data),
        status=status_code,
        content_type="application/json",
    )