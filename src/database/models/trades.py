import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, uuid_pk, datetime_create, price
from database.models.enums.type import TradeType, CouponDividendType
from .enums.type import Currency


class TradesModel(Base):
    __tablename__ = "trades"

    id: Mapped[uuid_pk]
    created_at: Mapped[datetime_create]
    currency: Mapped[Currency] = mapped_column(default=Currency.RUB)
    quantity: Mapped[int] = mapped_column(default=0)
    amount: Mapped[price] = mapped_column(default=0)
    commission: Mapped[price] = mapped_column(default=0)
    tax: Mapped[price] = mapped_column(default=0)
    balance_before: Mapped[price] = mapped_column(default=0)
    balance_after: Mapped[price] = mapped_column(default=0)
    trade_type: Mapped[TradeType] = mapped_column(
        default=TradeType.UNKNOWN,
        index=True
    )
    ticker: Mapped[str] = mapped_column(default="", index=True)
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE"),
        index=True
    )
    instrument_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="instrument.id", ondelete="CASCADE"),
        index=True,
    )

    # ForeignKey
    instrument: Mapped["InstrumentModel"] = relationship(
        back_populates="trades"
    )
    # ForeignKey
    account: Mapped["AccountModel"] = relationship(back_populates="trades")


class CouponDividendModel(Base):
    __tablename__ = "coupon_dividend"

    id: Mapped[uuid_pk]
    date: Mapped[datetime_create]
    amount: Mapped[price] = mapped_column(default=0)
    currency: Mapped[Currency] = mapped_column(default=Currency.RUB)
    ticker: Mapped[str] = mapped_column(default="")
    type: Mapped[CouponDividendType] = mapped_column(
        default=CouponDividendType.UNKNOWN
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE"),
        index=True,
    )
    instrument_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="instrument.id", ondelete="CASCADE"),
        index=True,
    )

    # ForeignKey
    account: Mapped["AccountModel"] = relationship(
        back_populates="coupon_dividend"
    )
    instrument: Mapped["InstrumentModel"] = relationship(
        back_populates="coupon_dividend"
    )
