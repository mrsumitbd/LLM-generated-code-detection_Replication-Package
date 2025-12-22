def fix_asyncio():
    """Fix asyncio event loop issues on Windows and ensure proper event loop handling."""
    import sys
    import asyncio
    
    if sys.platform == 'win32':
        # On Windows, use ProactorEventLoop for better subprocess support
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            if sys.platform == 'win32':
                loop = asyncio.new_event_loop()
            else:
                loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        if sys.platform == 'win32':
            loop = asyncio.new_event_loop()
        else:
            loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)