import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import String, text, Float, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, mapped_column

from database.database import engine


str_20 = Annotated[str, 20]
str_50 = Annotated[str, 50]
str_100 = Annotated[str, 100]
str_255 = Annotated[str, 255]
price = Annotated[float, 0]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_20: String(length=20),
        str_50: String(length=50),
        str_100: String(length=100),
        str_255: String(length=255),
        price: Float(precision=9, decimal_return_scale=2),
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        primary_key=True, index=True, unique=True,
        default=uuid.uuid4
    )
]

# datetime_create = Annotated[
#     datetime,
#     mapped_column(server_default=text("TIMEZONE('utc', now())"),)
# ]

datetime_create = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now()::timestamp)"),
        nullable=False,
    )
]
datetime_update = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now()::timestamp)"),
        nullable=False,
    )
]
