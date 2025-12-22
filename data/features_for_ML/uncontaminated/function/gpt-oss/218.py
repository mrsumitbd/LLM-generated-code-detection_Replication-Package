def async_wrapper(page):
    async def _():
        return page
    return _()