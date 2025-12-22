def get_route_handler() -> dict[str, str]:
    routes = {
        "/": "home",
        "/about": "about",
        "/contact": "contact",
        "/products": "products",
        "/cart": "cart",
        "/checkout": "checkout"
    }
    return routes