from .types import Request, Response, RouteHandler

def decorator(handler: RouteHandler):
            self.add_route(
                "PUT", path, handler, overwrite=overwrite, middleware=middleware
            )
            return handler