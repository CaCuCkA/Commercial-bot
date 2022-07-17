import logging

from aiogram import types, Bot, Dispatcher
from aiogram.types import CallbackQuery

from tgbot.infrastructure.database.functions.users import update_user
from tgbot.infrastructure.database.models import User
from tgbot.keyboards.inline import get_pay_now_or_free, get_check_markup, get_check_amount
from tgbot.misc.subscription_result import generate_result


async def greeting(message: types.Message):
    await message.answer(
        f"Привет {message.from_user.full_name}!\n"
        f"Вы хотите купить курс либо получить бесплано?"
        f"https://www.youtube.com/watch?v=zUuoZxo1q04",
        reply_markup=get_pay_now_or_free()
    )


async def take_for_free(call: CallbackQuery, bot: Bot, config):
    await call.answer()

    channels = config.tg_bot.channel_ids
    channels_format = str()

    for channels_id_or_username in channels:
        chat = await bot.get_chat(channels_id_or_username)
        invite_link = await chat.export_invite_link()
        channels_format += f"Канал <a href='{invite_link}'>{chat.title}</a>\n\n"

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f"Каналы на которые нужно подписаться: \n" \
                                     f" {channels_format}",
                                reply_markup=get_check_markup())


async def checker(call: CallbackQuery, session, bot: Bot, config, user: User):
    await call.answer()

    user_id = call.from_user.id

    result = await generate_result(config, bot, user_id)

    if result[-1] == "!":
        result = result[:-1]
        await call.message.answer("Вы не подписались на эти каналы: \n"
                                  f"{result}", reply_markup=get_check_markup())
        await call.message.delete()

        return

    referral_link = f"https://t.me/check_subscription_bot?start={call.from_user.id}"

    logging.info(user.subscription)
    logging.info(user.telegram_id)

    if user.subscription:
        text = f"Вы уже подписанны на канлы.\n" \
               f"Ваша реферальная ссылка: \n" \
               f"{referral_link}\n"

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=get_check_amount()
                                    )
        return

    text = f"Отлично! Вы подписались на все каналы)\n" \
           f"{result}" \
           f"Вам так же нужно пригласить 10 людей на вышестоящие каналы\n" \
           f"{referral_link}\n"

    await update_user(session, User.telegram_id == user.telegram_id, subscription=False)
    await session.commit()

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=get_check_amount()
                                )


def register_greeting_handlers(dp: Dispatcher):
    dp.register_message_handler(greeting, commands=["start"])
    dp.register_callback_query_handler(take_for_free, text="free")
    dp.register_callback_query_handler(checker, text="check_subs")
