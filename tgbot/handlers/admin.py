from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.filters.forwarded_message import IsForwarded


async def add_channels(message: types.Message, state: FSMContext):
    await message.answer(
        f"Это функция доступна лишь админам бота\n"
        f"Для добавления нового канала перешлите сюда"
        f"любое сообщение с этого канала."
    )

    await state.set_state("get_channel_post")


async def find_channel(message: types.Message, state: FSMContext):
    await message.answer(
        f"Сообщение прислано из канала {message.forward_from_chat.title}\n"
        f"Channel`s username: {message.forward_from_chat.username}\n"
        f"Channel`s Id: {message.forward_from_chat.id}"
    )
    await state.finish()


def register_add_channels(dp: Dispatcher):
    dp.register_message_handler(add_channels, commands=['add_channel'], is_admin=True)


def register_find_channel(dp: Dispatcher):
    dp.register_message_handler(find_channel, IsForwarded(), state="get_channel_post",
                                content_types=types.ContentType.ANY)
