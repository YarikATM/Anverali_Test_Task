import asyncio
import logging
import logging.config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.env_reader import config
from handlers import start
from DB.db import Database
from middlewares.database import DBMiddleware
from config.logger_config import LOGGING_CONFIG

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)


async def setup_database() -> Database:
    db = Database(host=config.DB_HOST, user=config.DB_USER.get_secret_value(),
                  password=config.DB_PASSWORD.get_secret_value(), db_name=config.DB_NAME)
    await db.connect()

    return db


def setup_middlewares(dp: Dispatcher, db: Database, bot: Bot) -> None:
    dp.message.middleware(DBMiddleware(db))


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)


async def setup_aiogram(dp: Dispatcher, bot: Bot) -> None:
    logger.debug("Configuring aiogram")

    db = await setup_database()
    setup_middlewares(dp, db, bot)
    setup_handlers(dp)

    logger.info("Configured aiogram")


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher, bot)


def main() -> None:
    setup_logging()

    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="HTML")

    dp = Dispatcher(
        storage=MemoryStorage()
    )

    # start polling
    dp.startup.register(aiogram_on_startup_polling)
    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    main()
