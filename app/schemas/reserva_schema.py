from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import Optional


class StatusReservaEnum(str, Enum):
    CREATED = "CREATED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELED = "CANCELED"


class ReservaBase(BaseModel):
    quarto_id: str
    nome_hospede: str
    data_checkin_previsto: date
    data_checkout_previsto: date
    status: StatusReservaEnum
    valor_total: Optional[float] = None


class ReservaCreate(ReservaBase):
    pass


class ReservaResponse(ReservaBase):
    id: str

    class Config:
        from_attributes = True
