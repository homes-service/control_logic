import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, uuid_pk, datetime_create, price, datetime_update, str_50, str_255
from .enums.type import BalanceOperationType, Currency
from schemas.portfolio import PortfolioSchema

class PortfolioModel(Base):
    __tablename__ = "portfolio"

    id: Mapped[uuid_pk]
    name: Mapped[str_50] = mapped_column(index=True)
    comment: Mapped[Optional[str_255]] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime_create]
    updated_at: Mapped[datetime_update]
    is_activate: Mapped[bool] = mapped_column(default=True)
    account_user_id: Mapped[uuid.UUID] = mapped_column(index=True)

    # ForeignKey
    account: Mapped[list["AccountModel"]] = relationship(back_populates="portfolio")

    def to_read_model(self) -> PortfolioSchema:
        return PortfolioSchema.from_orm(self)