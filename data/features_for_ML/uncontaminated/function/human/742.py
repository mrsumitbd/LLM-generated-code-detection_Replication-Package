from os.path import dirname, join
import aiohttp
import aiohttp_jinja2
import jinja2

def create_app():
    app = aiohttp.web.Application()
    add_routes(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(join(dirname(__file__), "templates")))
    return loop.run_until_complete(loop.create_server(app.make_handler(), host="0.0.0.0", port=web_cfg.port))