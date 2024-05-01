from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DBMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        data["db"] = self.db
        result = await handler(event, data)
        del data["db"]
        return result
