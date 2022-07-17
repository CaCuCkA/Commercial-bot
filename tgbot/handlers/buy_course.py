import asyncpg
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from tgbot.infrastructure.database.functions.users import update_user
from tgbot.infrastructure.database.models import User
from tgbot.keyboards.inline import get_check_card_number, get_pay_button
from tgbot.keyboards.inline_calback import check_card


async def generate_invoice(call: types.CallbackQuery, state: FSMContext, bot: Bot, user: User):
    await call.answer()

    if call.data == "buy" and user.card_id is None:
        text = "Отлично!\n" \
               "Введите последние четыре карты, c которой планируете\n" \
               "производить оплату, для создания платежа"
    elif call.data == "denied_card":
        text = "Введите последние четыре карты, c которой планируете\n" \
               "производить оплату, для создания платежа"

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text)

    await state.set_state("card_number")


async def accept_card(message: types.Message, state: FSMContext):
    card_id = message.text

    await message.answer("Все верно?\n"
                         f"<b>{card_id}</b>", reply_markup=get_check_card_number(card_id))
    await state.finish()


async def create_invoice(call: types.CallbackQuery, callback_data: dict, session, bot: Bot):
    await call.answer()

    card_number = int(callback_data.get("card_number"))
    user_id = call.from_user.id

    await update_user(session, User.telegram_id == user_id, card_id=card_number)

    await session.commit()

    text = "Перейдите по указанной ссылке и оплатите курс:\n"

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=get_pay_button())


def register_buy_course_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(generate_invoice, text=["buy", "denied_card"])
    dp.register_message_handler(accept_card, state="card_number")
    dp.register_callback_query_handler(create_invoice, check_card.filter(result="accept_card"))
