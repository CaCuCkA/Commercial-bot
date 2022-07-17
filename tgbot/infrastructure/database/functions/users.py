from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from tgbot.infrastructure.database.models import User


async def add_user(session: AsyncSession, telegram_id, first_name, last_name=None,
                   amount_of_referrals=0, card_id=None, subscription=False) -> None:
    insert_stmt = select(
        User
    ).from_statement(
        insert(
            User
        ).values(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            amount_of_referrals=amount_of_referrals,
            card_id=card_id,
            subscription=subscription
        ).returning(User)
    )

    result = await session.scalars(insert_stmt)
    return result.first()


async def get_one_user(session: AsyncSession, **kwargs) -> User:
    statement = select(User).filter_by(**kwargs)
    result: AsyncResult = await session.scalars(statement)
    return result.first()


async def get_fullname(session: AsyncSession, telegram_id) -> str:
    first_name = select(
        User.first_name
    ).where(
        User.telegram_id == telegram_id
    )
    last_name = select(
        User.last_name
    ).where(
        User.telegram_id == telegram_id
    )

    first_name = await session.scalar(first_name)
    last_name = await session.scalar(last_name)

    if last_name is not None:
        full_name = first_name + " " + last_name
    else:
        full_name = first_name
    return full_name


async def update_user(session: AsyncSession, *clauses, **values) -> None:
    statement = update(
        User
    ).where(
        *clauses
    ).values(
        **values
    )
    await session.execute(statement)


async def get_user_id(session: AsyncSession, card_id) -> int:
    statement = select(
        User.telegram_id
    ).where(
        User.card_id == card_id
    )

    result: AsyncResult = await session.scalar(statement)
    return result


# async def update_amount_of_referrals(session: AsyncSession, telegram_id) -> None:
#     statement = update(
#         User
#     ).where(
#         User.telegram_id == telegram_id
#     ).values(
#         amount_of_referrals=User.amount_of_referrals + 1
#     )
#
#     await session.execute(statement)

async def get_amount_of_referrals(session: AsyncSession, telegram_id) -> int:
    statement = select(
        User.amount_of_referrals
    ).where(
        User.telegram_id == telegram_id
    )

    result: AsyncResult = await session.scalar(statement)
    return result


async def get_subscription(session: AsyncSession, telegram_id) -> bool:
    statement = select(
        User.subscription
    ).where(
        User.telegram_id == telegram_id
    )

    result: AsyncResult = await session.scalar(statement)
    return result
