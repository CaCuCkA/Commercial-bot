import asyncio
import datetime
import hashlib
import hmac
import json
import logging
import re

import aiohttp
from aiogram import Bot
from aiohttp import web

from tgbot.config import load_config
from tgbot.infrastructure.database.functions.users import get_one_user, get_user_id
from tgbot.keyboards.inline import get_start_course
from tgbot.misc.wb_session_pool import create_session_pool

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


def generate_signature(merchant_key, data_str):
    return hmac.new(merchant_key.encode(), data_str.encode(), hashlib.md5).hexdigest()


async def wayforpay_webhook(request):
    request: aiohttp.web.Request

    data = await request.post()
    for key, value in data.items():
        try:
            data = json.loads(key)
        except json.decoder.JSONDecodeError as error:
            logging.error(f"json.decoder.JSONDecodeError: {error}. Data {data}")
            data = json.loads(repair(key))

    logging.info(f"data = {data}")
    transactionStatus = data.get("transactionStatus")
    card_pan = int(data.get("cardPan")[-4:])
    logging.info(card_pan)
    telegram_id = await get_user_id(session, card_pan)
    logging.info(telegram_id)
    if transactionStatus == "Approved":
        await process_successful_payment(telegram_id, data)

    response_data = generate_response(data)
    logging.info(f"response data: {response_data}")

    return web.json_response(response_data)


async def init_app(loop):
    app = web.Application(loop=loop)
    app.router.add_post('/accept_payment', wayforpay_webhook)
    return app


def generate_response(response):
    time = int(datetime.datetime.now().timestamp())
    data = dict(
        orderReference=response.get("orderReference"),
        status="accept",
        time=time,
    )
    sign = ";".join(str(value) for key, value in data.items())
    signature = generate_signature(config.payments.wayforpay_secret_key, sign)
    data.update(signature=signature)
    return data


invalid_escape = re.compile(r'\\[0-7]{1,3}')


def replace_with_byte(match):
    return chr(int(match.group(0)[1:], 8))


def repair(brokenjson):
    return invalid_escape.sub(replace_with_byte, brokenjson)


async def process_successful_payment(telegram_id, data):
    client_first_name = data.get("clientName")

    text = f"{client_first_name}, \n" \
           f"спасибо, что купили курс!"

    await bot.send_message(text=text, chat_id=telegram_id, reply_markup=get_start_course())


def create_db_amigo():
    return create_session_pool(config.db)


config = load_config()
session_pool = create_db_amigo()
session = session_pool()
loop = asyncio.get_event_loop()
bot = Bot(token=config.tg_bot.token, loop=loop, parse_mode='HTML')
app = loop.run_until_complete(init_app(loop))
web.run_app(app, host='0.0.0.0', port=8080, loop=loop)
