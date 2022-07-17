from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline_calback import check_callback, check_card


def get_pay_now_or_free():
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Купить курс",
                                                callback_data="buy"

                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="Получить бесплатно",
                                                callback_data="free"
                                            )
                                        ]

                                    ]
                                    )

    return keyboard


def get_check_markup():
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Проверить подписку",
                                                callback_data="check_subs"
                                            )
                                        ]
                                    ])
    return keyboard


def get_check_markup_deep_link(user_name: str):
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Проверить подписку",
                                                callback_data=check_callback.new(check_sub="check_sub_d",
                                                                                 user_id=user_name)
                                            )
                                        ]
                                    ])
    return keyboard


def get_answer():
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Да",
                                                callback_data="yes"
                                            ),
                                            InlineKeyboardButton(
                                                text="Нет",
                                                callback_data="no"
                                            )
                                        ]
                                    ])
    return keyboard


def get_pay_now_or_free_deep_link():
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Купить курс",
                                                callback_data="buy"

                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="Получить бесплатно",
                                                callback_data="free_d"
                                            )
                                        ]

                                    ]
                                    )

    return keyboard


def get_start_course():
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Начать курс",
                                                callback_data="start_course"
                                            )
                                        ]
                                    ])

    return keyboard


def get_back():
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Назад",
                                                callback_data="back"
                                            )
                                        ]
                                    ])
    return keyboard


def get_check_amount():
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Проверить",
                                                callback_data="check"
                                            )
                                        ]
                                    ])
    return keyboard


def get_check_card_number(card_number: str):
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Да",
                                                callback_data=check_card.new(result="accept_card",
                                                                             card_number=card_number)
                                            ),

                                            InlineKeyboardButton(
                                                text="Нет",
                                                callback_data="denied_card"
                                            )
                                        ]
                                    ])
    return keyboard


def get_pay_button():
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Оплатить",
                                                url="https://secure.wayforpay.com/button/ba375d9bd61d4"
                                            )
                                        ]
                                    ])
    return keyboard
