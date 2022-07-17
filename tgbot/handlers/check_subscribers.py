from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline import get_check_amount, get_start_course


async def check_subscribers(call: CallbackQuery, config, user):
    await call.answer()

    # take your and global amounts of referral users
    amount_of_referrals = config.tg_bot.amount_of_referrals
    your_amount = user.amount_of_referrals

    # give access to the channel
    if your_amount >= amount_of_referrals:

        await call.message.answer(
            f"Супер!\n"
            f"Вы справились) Держите ваш курс!\n",
            reply_markup=get_start_course()
        )

    else:
        if user.referrals:
            referrals = '\n'.join(
                f"{num}. {referral.first_name} {referral.last_name} - {referral.created_at.strftime('%d.%m.%Y %H:%M')}"
                for num, referral in enumerate(user.referrals, start=1))
            await call.message.answer(
                f"Вы привели {your_amount} новых пользователей.\n"
                f"{referrals}"
                f"Осталось {amount_of_referrals - your_amount}",
                reply_markup=get_check_amount()
            )
        else:
            await call.message.answer(
                f"Вы привели 0 новых пользователей.\n"
                f"Осталось {amount_of_referrals}",
                reply_markup=get_check_amount()
            )


def register_check_subscribers(dp: Dispatcher):
    dp.register_callback_query_handler(check_subscribers, text="check")
