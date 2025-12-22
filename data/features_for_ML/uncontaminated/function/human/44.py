def get_route_handler() -> dict[str, str]:
    return {
        "/": "home",
        "/home": "home",
        "/recordings": "recordings",
        "/settings": "settings",
        "/storage": "storage",
        "/about": "about",
    }