from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from typing import Dict
from sqlalchemy.ext.asyncio import sessionmaker

def build_dispatcher(settings: Settings, async_session_factory: sessionmaker) -> tuple[Dispatcher, Bot, Dict]:
    bot = Bot(token=settings.bot_token, parse_mode="HTML")
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)
    
    middleware_data = {
        "session_factory": async_session_factory,
        "settings": settings,
    }
    
    return dispatcher, bot, middleware_data