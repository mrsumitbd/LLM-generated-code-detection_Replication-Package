def _default_http_error(
    request: HttpRequest, exc: HttpError, api: "NinjaAPI"
) -> HttpResponse:
    status_code = exc.status_code
    detail = exc.detail
    
    if isinstance(detail, dict):
        body = detail
    elif isinstance(detail, (list, tuple)):
        body = {"detail": detail}
    else:
        body = {"detail": str(detail) if detail else ""}
    
    return HttpResponse(
        content=json.dumps(body),
        status=status_code,
        content_type="application/json",
    )