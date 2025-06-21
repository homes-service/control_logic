import uuid

from typing import Optional

from utils.utils import PydanticDictModel


class InstrumentGroupsSchema(PydanticDictModel):
    id: uuid.UUID
    name: str
    comment: Optional[str]
    value: float = 0
    percentage: float = 0
    account_id: uuid.UUID

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "2086c549-77a6-4b1c-98a2-e71670e17a2d",
                    "name": "Группа инструментов",
                    "comment": "Финансовый сектор",
                    "value": 0,
                    "percentage": 0,
                    "account_id": "94f4c1f5-bce4-4148-b762-83e14938778f"
                }
            ]
        }
    }


class InstrumentGroupsSchemaAdd(PydanticDictModel):
    name: str
    comment: Optional[str]
    value: float = 0
    percentage: float = 0
    account_id: uuid.UUID

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Новая группа инструментов",
                "comment": "Финансовый сектор",
                "value": 7,
                "percentage": 12.6,
                "account_id": "2086c549-77a6-4b1c-98a2-e71670e17a2d"
            }]
        }
    }


class InstrumentGroupsSchemaAddResponse(PydanticDictModel):
    instrument_group_id: uuid.UUID

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "instrument_group_id": "f23a56d4-39ec-4f57-95b6-362508852931"
            }]
        }
    }


class InstrumentGroupSchemaUpdate(PydanticDictModel):
    name: Optional[str] = None
    comment: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Новое название группы инструментов",
                "comment": "Новый кооментарий группы"
            }]
        }
    }
