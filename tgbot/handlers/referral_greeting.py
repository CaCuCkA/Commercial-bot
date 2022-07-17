import re

from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery

from tgbot.infrastructure.database.functions.users import get_subscription, get_fullname, update_user, get_one_user
from tgbot.infrastructure.database.models import User
from tgbot.keyboards.inline import get_answer, get_check_markup_deep_link, get_pay_now_or_free_deep_link, get_back, \
    get_check_amount
from tgbot.keyboards.inline_calback import check_callback
from tgbot.misc.subscription_result import generate_result


async def referral_greeting(message: types.Message, session, config, bot: Bot, user: User):
    referrer_id = int(message.get_args())
    user_id = message.from_user.id

    if referrer_id == user_id:
        await message.answer(f"Вы не можете быть преглашенным по этой ссылке,\n"
                             f"так как вы её создатель) ")
        return

    if user.subscription:
        await message.answer(f"Вы уже подписались на все каналы)\n"
                             f"Больше вы не можете быть приглашенным.")
        await message.answer("Не хотите ли вы курс пройти курс по крипте?",
                             reply_markup=get_answer())

        return

    channels = config.tg_bot.channel_ids
    channels_format = str()

    for channel in channels:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f"Канал <a href='{invite_link}'>{chat.title}</a>\n\n"

    friend = await get_fullname(session, referrer_id)

    await message.answer(f"Привет, {message.from_user.full_name}\n"
                         f"Ты перешел по реферальной ссылки {friend}.\n"
                         f"Чтобы ему помочь ты должен подписаться на эти каналы:\n"
                         f"{channels_format}",
                         reply_markup=get_check_markup_deep_link(str(referrer_id)))


async def checker(call: CallbackQuery, callback_data: dict, session, user: User, config, bot: Bot):
    await call.answer(cache_time=60)

    referrer_id = callback_data.get("user_id")
    user_id = call.from_user.id

    result = await generate_result(config, bot, user_id)

    if result[-1] == "!":
        result = result[:-1]
        await call.message.answer("Вы не подписались на эти каналы: \n"
                                  f"{result}", reply_markup=get_check_markup_deep_link(str(referrer_id)))
        await call.message.delete()

        return

    await call.message.answer(f"Отлично! Вы подписались на все каналы)\n"
                              f"{result}")

    referrer = await get_one_user(session, telegram_id=referrer_id)
    await update_user(session, User.telegram_id == referrer_id, amount_of_referrals=referrer.amount_of_referrals + 1)

    await update_user(session, User.telegram_id == user_id, referrer_id=referrer_id,
                      subscription=True)

    await session.commit()

    await call.message.answer("Не хотите ли вы курс пройти курс по крипте?",
                              reply_markup=get_answer())

    await call.message.edit_reply_markup(reply_markup=None)


async def answer_no(call: CallbackQuery, bot: Bot):
    """
    Function react if user press 'no'
    """
    await call.answer(cache_time=1)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Хорошо, спасибо!\n",
                                reply_markup=get_back())


async def choice(call: CallbackQuery, bot: Bot):
    """
    Function asks referrals if they want to learn course
    """
    await call.answer(cache_time=1)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Не хотите ли вы курс пройти курс по крипте?",
                                reply_markup=get_answer())


async def answer_yes(call: CallbackQuery, bot: Bot):
    """
    Function react if user press 'yes'
    """
    await call.answer(cache_time=60)

    text = "Отлично,\n" \
           " Хотите купить курс либо получить бесплатно?"

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=get_pay_now_or_free_deep_link())


async def for_free(call: CallbackQuery, bot: Bot):
    await call.answer(cache_time=60)

    referral_link = f"https://t.me/check_subscription_bot?start={call.from_user.id}"

    text = f"Ваша реферальная ссылка создана, пригласите 7 человек: \n" \
           f"{referral_link}\n"

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=get_check_amount())


def register_referral_greeting_handlers(dp: Dispatcher):
    dp.register_message_handler(referral_greeting, CommandStart(deep_link=re.compile(r"^[0-9]{9}$")))
    dp.register_callback_query_handler(checker, check_callback.filter(check_sub="check_sub_d"))
    dp.register_callback_query_handler(choice, text="back")
    dp.register_callback_query_handler(answer_no, text="no")
    dp.register_callback_query_handler(answer_yes, text="yes")
    dp.register_callback_query_handler(for_free, text="free_d")
