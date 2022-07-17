from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message


class ToolMiddleware(LifetimeControllerMiddleware):
    def __init__(self, config, bot):
        super().__init__()
        self.bot = bot
        self.config = config

    async def pre_process(self, obj: [CallbackQuery, Message], data: Dict, *args: Any):
        config = self.config
        bot = self.bot
        data["config"] = config
        data["bot"] = bot
