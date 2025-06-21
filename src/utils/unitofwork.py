from abc import ABC, abstractmethod
from typing import Type

from database.database import async_session
from repositories.account import (
    AccountRepository,
    BalanceHistoryRepository,
    AccountBalanceRepository,
)
from repositories.portfolio import PortfolioRepository
from repositories.instrument import (
    InstrumentRepository,
    InstrumentGroupRepository,
)
from repositories.trades import TradesRepository, CouponDividendRepository


class IUnitOfWork(ABC):
    account: Type[AccountRepository]
    account_balance: Type[AccountBalanceRepository]
    balance_history: Type[BalanceHistoryRepository]
    portfolio: Type[PortfolioRepository]
    instrument: Type[InstrumentRepository]
    instrument_group: Type[InstrumentGroupRepository]
    trades: Type[TradesRepository]
    coupon_dividends: Type[CouponDividendRepository]

    
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        self.session = self.session_factory()

        self.account = AccountRepository(self.session)
        self.account_balance = AccountBalanceRepository(self.session)
        self.balance_history = BalanceHistoryRepository(self.session)
        self.portfolio = PortfolioRepository(self.session)
        self.instrument = InstrumentRepository(self.session)
        self.instrument_group = InstrumentGroupRepository(self.session)
        self.trades = TradesRepository(self.session)
        self.coupon_dividends = CouponDividendRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
