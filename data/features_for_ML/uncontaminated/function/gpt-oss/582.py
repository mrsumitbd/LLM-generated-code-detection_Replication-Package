from __future__ import annotations

from typing import Dict, Tuple

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DBSessionMiddleware:
    """
    Middleware that injects an async SQLAlchemy session into the handler data.
    The session is created from the provided async_session_factory and closed
    automatically after the handler finishes.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def __call__(self, handler, event, data):
        async with self._session_factory() as session:
            data["session"] = session
            return await handler(event, data)


def build_dispatcher(
    settings: "Settings",
    async_session_factory: async_sessionmaker[AsyncSession],
) -> Tuple[Dispatcher, Bot, Dict]:
    """
    Build and configure an aiogram Dispatcher and Bot instance.

    Parameters
    ----------
    settings : Settings
        Application settings containing at least a ``bot_token`` attribute.
    async_session_factory : async_sessionmaker[AsyncSession]
        Factory for creating async SQLAlchemy sessions.

    Returns
    -------
    tuple[Dispatcher, Bot, dict]
        The configured dispatcher, bot, and a dictionary with auxiliary
        objects (currently only the session factory).
    """
    # Create the bot instance
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)

    # Create the dispatcher and attach the bot
    dispatcher = Dispatcher(bot)

    # Register the DB session middleware for all message and callback query handlers
    dispatcher.message.middleware(DBSessionMiddleware(async_session_factory))
    dispatcher.callback_query.middleware(DBSessionMiddleware(async_session_factory))

    # Return the dispatcher, bot, and a dict with the session factory for
    # potential further use (e.g., in tests or other parts of the app).
    return dispatcher, bot, {"session_factory": async_session_factory}