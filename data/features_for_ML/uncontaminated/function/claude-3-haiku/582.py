from typing import Dispatcher, Bot, Dict
from sqlalchemy.orm import sessionmaker
from settings import Settings

def build_dispatcher(settings: Settings, async_session_factory: sessionmaker) -> tuple[Dispatcher, Bot, Dict]:
    from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
    from telegram import Bot

    bot = Bot(token=settings.BOT_TOKEN)
    dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

    handlers = {
        'start': CommandHandler('start', start_command),
        'echo': MessageHandler(Filters.text & ~Filters.command, echo_message),
    }

    for name, handler in handlers.items():
        dispatcher.add_handler(handler)

    return dispatcher, bot, handlers