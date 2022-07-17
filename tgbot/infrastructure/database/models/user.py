from typing import List

from sqlalchemy import Column, BIGINT, VARCHAR, INTEGER, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from tgbot.infrastructure.database.models.base import DatabaseModel, TimeStampMixin


class User(DatabaseModel, TimeStampMixin):
    telegram_id = Column(BIGINT, nullable=False, primary_key=True)
    first_name = Column(VARCHAR(200), nullable=False)
    last_name = Column(VARCHAR(200), server_default=expression.null(), nullable=True)
    amount_of_referrals = Column(INTEGER, nullable=False)
    card_id = Column(INTEGER, server_default=expression.null(), nullable=True)
    subscription = Column(BOOLEAN, nullable=False)

    referrer_id = Column(
        BIGINT,
        ForeignKey("users.telegram_id", ondelete="SET NULL", name="FK__users_referrer_id"),
        nullable=True
    )  # id of the user who referred this user

    # Referrer is the user who referred this user
    referrer: "User" = relationship(
        "User",
        back_populates="referrals",
        lazy="joined",
        remote_side=[telegram_id],
        join_depth=1
    )

    referrals: List["User"] = relationship(
        "User",
        remote_side=[referrer_id],
        back_populates="referrer",
        lazy="joined",
        join_depth=1,
        order_by="User.created_at.desc()"
    )
