import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.forwarded_message import IsForwarded
from tgbot.handlers.admin import register_add_channels, register_find_channel
from tgbot.handlers.buy_course import register_buy_course_handlers
from tgbot.handlers.check_subscribers import register_check_subscribers
from tgbot.handlers.greeting import register_greeting_handlers
from tgbot.handlers.referral_greeting import register_referral_greeting_handlers
from tgbot.infrastructure.database.functions.setup import create_session_pool
from tgbot.middlewares.bot_tools import ToolMiddleware
from tgbot.middlewares.database import DbMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, session_pool, config, bot):
    dp.setup_middleware(DbMiddleware(session_pool))
    dp.setup_middleware(ToolMiddleware(config, bot))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsForwarded)


def register_all_handlers(dp):
    # admin`s handlers
    register_add_channels(dp)
    register_find_channel(dp)

    # greeting`s handler with deep link
    register_referral_greeting_handlers(dp)

    # greeting`s handler
    register_greeting_handlers(dp)

    # check handler
    register_check_subscribers(dp)

    # buy handler
    register_buy_course_handlers(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    session_pool = await create_session_pool(config.db, echo=False)

    register_all_middlewares(
        dp,
        session_pool=session_pool,
        bot=bot,
        config=config
    )
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
