from starlette.responses import JSONResponse

def _default_http_error(
    request: "HttpRequest", exc: "HttpError", api: "NinjaAPI"
) -> "HttpResponse":
    """
    Default error handler for HTTP errors.

    Parameters
    ----------
    request : HttpRequest
        The incoming request.
    exc : HttpError
        The exception raised.
    api : NinjaAPI
        The API instance (unused in this default implementation).

    Returns
    -------
    HttpResponse
        A JSON response containing the error detail and the appropriate status code.
    """
    # The HttpError is expected to expose a `status_code` and a `detail` attribute.
    # We simply return a JSONResponse with those values.
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )