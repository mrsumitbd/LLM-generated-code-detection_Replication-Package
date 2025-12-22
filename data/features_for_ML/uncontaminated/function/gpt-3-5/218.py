def async_wrapper(page):
    async def wrapper():
        return await page()
    
    return wrapper