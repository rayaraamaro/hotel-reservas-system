import uuid
from sqlalchemy import Column, String, Enum, Float, Integer
from sqlalchemy.dialects.oracle import CHAR
from sqlalchemy.orm import relationship
from app.database.config import Base
from enum import Enum as PyEnum


# ===========================
# ENUMS
# ===========================
class TipoQuartoEnum(PyEnum):
    STANDARD = "STANDARD"
    DELUXE = "DELUXE"
    SUITE = "SUITE"


class StatusQuartoEnum(PyEnum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


# ===========================
# MODELO QUARTO
# ===========================
class Quarto(Base):
    __tablename__ = "TB_QUARTO"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    numero = Column(Integer, unique=True, nullable=False)
    tipo = Column(Enum(TipoQuartoEnum), nullable=False)
    capacidade = Column(Integer, nullable=False)
    valor_diaria = Column(Float, nullable=False)
    status = Column(Enum(StatusQuartoEnum), nullable=False, default=StatusQuartoEnum.ATIVO)

    # Relacionamento com reservas (1:N)
    reservas = relationship("Reserva", back_populates="quarto", cascade="all, delete-orphan")
