def build_dispatcher(settings: Settings, async_session_factory: sessionmaker) -> tuple[Dispatcher, Bot, Dict]:
    dispatcher = Dispatcher(settings)
    bot = Bot(dispatcher, async_session_factory)
    plugins = load_plugins()
    return dispatcher, bot, plugins