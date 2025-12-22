def async_wrapper(page):
    import asyncio
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(func(*args, **kwargs))
                return result
            finally:
                loop.close()
        return wrapper
    return decorator