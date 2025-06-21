from database.models.instrument import InstrumentModel, InstrumentGroupModel
from utils.repository import SQLAlchemyRepository


class InstrumentGroupRepository(SQLAlchemyRepository):
    model = InstrumentGroupModel
