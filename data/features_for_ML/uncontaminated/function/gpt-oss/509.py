import sys
import asyncio

def fix_asyncio():
    """
    Apply a safe asyncio event loop policy.

    On Windows, the default ProactorEventLoop can cause issues with
    certain libraries.  We switch to the selector-based policy.
    If uvloop is available, we prefer it for better performance.
    """
    # Prefer uvloop if installed
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        return
    except Exception:
        pass

    # On Windows, use the selector policy to avoid Proactor issues
    if sys.platform == "win32":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            return
        except Exception:
            pass

    # Fallback to the default policy
    try:
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    except Exception:
        # If setting the policy fails, ignore – the default is already set
        pass