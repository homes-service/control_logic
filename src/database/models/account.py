import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, uuid_pk, datetime_create, price, datetime_update, str_50, str_255
from .enums.type import BalanceOperationType, Currency


class AccountBalanceModel(Base):
    __tablename__ = "account_balance"

    id: Mapped[uuid_pk]
    updated_at: Mapped[datetime_update]
    amount: Mapped[price]
    currency: Mapped[Currency] = mapped_column(default=Currency.RUB, index=True)
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="account.id", ondelete="CASCADE"),
        index=True
    )

    # ForeignKey
    account: Mapped["AccountModel"] = relationship(
        back_populates="account_balance"
    )
    history: Mapped[list["BalanceHistoryModel"]] = relationship(
        back_populates="account_balance"
    )


class AccountModel(Base):
    __tablename__ = "account"

    id: Mapped[uuid_pk]
    name: Mapped[str_50] = mapped_column(index=True)
    comment: Mapped[Optional[str_255]] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime_create]
    updated_at: Mapped[datetime_update]
    is_activate: Mapped[bool] = mapped_column(default=True)
    account_user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="portfolio.id", ondelete="CASCADE"),
        index=True
    )

    # ForeignKey
    trades: Mapped[list["TradesModel"]] = relationship(
        back_populates="account")
    account_balance: Mapped[list["AccountBalanceModel"]] = relationship(
        back_populates="account")
    coupon_dividend: Mapped[list["CouponDividendModel"]] = relationship(
        back_populates="account")
    instrument: Mapped[list["InstrumentModel"]] = relationship(
        back_populates="account")
    instrument_group: Mapped[list["InstrumentGroupModel"]] = relationship(
        back_populates="account")
    portfolio: Mapped[list["PortfolioModel"]] = relationship(
        back_populates="account"
    )


class BalanceHistoryModel(Base):
    __tablename__ = "balance_history"

    id: Mapped[uuid_pk]
    created_at: Mapped[datetime_create]
    type: Mapped[BalanceOperationType] = mapped_column(index=True)
    amount_before: Mapped[price]
    amount: Mapped[price]
    comment: Mapped[Optional[str_255]] = mapped_column(
        nullable=True, default=None
    )
    account_balance_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(column="account_balance.id", ondelete="CASCADE"),
        index=True
    )

    # ForeignKey
    account_balance: Mapped["AccountBalanceModel"] = relationship(
        back_populates="history"
    )
