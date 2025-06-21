from enum import Enum


class Currency(Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    CNY = 'CNY'


class BalanceOperationType(Enum):
    ADDING = 'ADDING'
    DEDUCTION = 'DEDUCTION'
    BUY = 'BUY'  # Покупка
    SELL = 'SELL'  # Продажа
    COUPON_PAYMENT = 'COUPON_PAYMENT'  # Выплата купонов
    DIVIDEND_PAYMENT = 'DIVIDEND_PAYMENT'  # Выплата дивидентов
    TAX_WRITE_OFF = 'TAX_WRITE_OFF'  # Списание налогов
    COMMISSION_WRITE_OFF = 'COMMISSION_WRITE_OFF'  # списание комиссий
    DENOMINATION_PYMENT = 'DENOMINATION_PYMENT'  # Выплата номинала
    BOND_AMORTIZATION = 'BOND_AMORTIZATION'  # Амортизация
    UNKNOWN = 'UNKNOWN'  # Неизвестно


class TradeType(Enum):
    BUY = 'BUY'  # Покупка
    SELL = 'SELL'  # Продажа
    COUPON_PAYMENT = 'COUPON_PAYMENT'  # Выплата купонов
    DIVIDEND_PAYMENT = 'DIVIDEND_PAYMENT'  # Выплата дивидентов
    TAX_WRITE_OFF = 'TAX_WRITE_OFF'  # Списание налогов
    DENOMINATION_PYMENT = 'DENOMINATION_PYMENT'  # Выплата номинала
    BOND_AMORTIZATION = 'BOND_AMORTIZATION'  # Амортизация
    UNKNOWN = 'UNKNOWN'  # Неизвестно


class CouponDividendType(Enum):
    COUPON = "COUPON"
    DIVIDEND = "DIVIDEND"
    UNKNOWN = "UNKNOWN"


TRADE_TO_BALANCE_OPERATION = {
    TradeType.BUY: BalanceOperationType.BUY,
    TradeType.SELL: BalanceOperationType.SELL,
    TradeType.COUPON_PAYMENT: BalanceOperationType.COUPON_PAYMENT,
    TradeType.DIVIDEND_PAYMENT: BalanceOperationType.DIVIDEND_PAYMENT,
    TradeType.TAX_WRITE_OFF: BalanceOperationType.TAX_WRITE_OFF,
    TradeType.DENOMINATION_PYMENT: BalanceOperationType.DENOMINATION_PYMENT,
    TradeType.BOND_AMORTIZATION: BalanceOperationType.BOND_AMORTIZATION,
    TradeType.UNKNOWN: BalanceOperationType.UNKNOWN,
}


def trade_type_to_balance_operation(trade_type: TradeType) \
        -> BalanceOperationType:
    """Конвертирует TradeType в BalanceOperationType."""
    return TRADE_TO_BALANCE_OPERATION.get(
        trade_type, BalanceOperationType.UNKNOWN
    )
