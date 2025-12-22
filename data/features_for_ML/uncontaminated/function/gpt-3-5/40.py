def get_volumes(self) -> list[tuple[str, str]]:
    return [
        ("/host/home", "/container/home"),
        ("/host/workspace", "/container/workspace")
    ]