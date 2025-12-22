import asyncio

async def async_wrapper(page):
    async with aiohttp.ClientSession() as session:
        async with session.get(page) as response:
            content = await response.text()
            return content