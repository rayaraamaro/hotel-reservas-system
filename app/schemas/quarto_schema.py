from pydantic import BaseModel
from enum import Enum
from typing import Optional


class TipoQuartoEnum(str, Enum):
    STANDARD = "STANDARD"
    DELUXE = "DELUXE"
    SUITE = "SUITE"


class StatusQuartoEnum(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class QuartoBase(BaseModel):
    numero: int
    tipo: TipoQuartoEnum
    capacidade: int
    valor_diaria: float
    status: StatusQuartoEnum


class QuartoCreate(QuartoBase):
    pass


class QuartoResponse(QuartoBase):
    id: str
    
    class Config:
        from_attributes = True
