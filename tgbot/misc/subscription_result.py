from tgbot.misc import subscription


async def generate_result(config, bot, telegram_id) -> str:
    positive_result = str()
    negative_result = str()

    channels = config.tg_bot.channel_ids

    for channel in channels:
        status = await subscription.check(user_id=telegram_id, channel=channel)
        channel = await bot.get_chat(channel)

        if status:
            positive_result += f"Подписка на канал <b>{channel.title}</b> - " \
                               f"Оформлена!\n\n"
        else:
            invite_link = await channel.export_invite_link()
            negative_result += f"Подписка на канал <b>{channel.title}</b> - " \
                               f"<b>НЕ</b> Оформлена!\n" \
                               f"Подпишитесь на канал - <a href='{invite_link}'>{channel.title}</a>\n\n"

    if negative_result:
        return negative_result + "!"

    return positive_result

