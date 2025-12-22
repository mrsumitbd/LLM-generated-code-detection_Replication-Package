from aiohttp import web

class WatcherHealthServer:
    """Simple HTTP health endpoint for watcher monitoring."""

    def __init__(self, watcher, port=8080):
        self.watcher = watcher
        self.port = port
        self.app = web.Application()
        self.app.add_routes([web.get('/health', self.health_check)])

    async def health_check(self, request):
        return web.json_response({'status': 'ok'})

    def setup_routes(self):
        runner = web.AppRunner(self.app)
        return runner

# Example usage:
# watcher = SomeWatcherClass()
# server = WatcherHealthServer(watcher)
# runner = server.setup_routes()
# web.run_app(server.app, port=server.port)