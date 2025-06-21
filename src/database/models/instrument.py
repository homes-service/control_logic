import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import (
    Base,
    uuid_pk,
    str_20,
    price,
    str_50,
    str_255,
    datetime_create
)
from .enums.type import Currency


class InstrumentModel(Base):
    __tablename__ = "instrument"

    id: Mapped[uuid_pk]
    ticker: Mapped[str_20] = mapped_column(index=True)
    count: Mapped[int] = mapped_column(default=1)
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE"),
        index=True
    )
    instrument_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("instrument_group.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ForeignKey
    account: Mapped["AccountModel"] = relationship(
        back_populates="instrument"
    )
    instrument_group: Mapped[Optional["InstrumentGroupModel"]] = relationship(
        back_populates="instrument")
    coupon_dividend: Mapped[list["CouponDividendModel"]] = relationship(
        back_populates="instrument")
    trades: Mapped[Optional["TradesModel"]] = relationship(
        back_populates="instrument"
    )


class InstrumentGroupModel(Base):
    __tablename__ = "instrument_group"

    id: Mapped[uuid_pk]
    name: Mapped[str_50] = mapped_column(index=True)
    comment: Mapped[Optional[str_255]] = mapped_column(
        nullable=True, default=None
    )
    value: Mapped[price]
    percentage: Mapped[float]
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE"),
        index=True
    )

    # ForeignKey
    account: Mapped["AccountModel"] = relationship(
        back_populates="instrument_group"
    )
    instrument: Mapped[list["InstrumentModel"]] = relationship(
        back_populates="instrument_group")
