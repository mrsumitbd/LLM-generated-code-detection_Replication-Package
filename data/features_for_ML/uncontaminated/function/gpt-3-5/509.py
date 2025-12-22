def fix_asyncio():
    import os
    os.environ['PYTHONASYNCIODEBUG'] = '1'