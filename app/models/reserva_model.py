import uuid
from sqlalchemy import Column, String, Enum, Float, Date, ForeignKey
from sqlalchemy.dialects.oracle import CHAR
from sqlalchemy.orm import relationship
from app.database.config import Base
from enum import Enum as PyEnum


# ===========================
# ENUM DE STATUS DA RESERVA
# ===========================
class StatusReservaEnum(PyEnum):
    CREATED = "CREATED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELED = "CANCELED"


# ===========================
# MODELO RESERVA
# ===========================
class Reserva(Base):
    __tablename__ = "TB_RESERVA"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    quarto_id = Column(CHAR(36), ForeignKey("TB_QUARTO.id"), nullable=False)
    nome_hospede = Column(String(100), nullable=False)
    data_checkin_previsto = Column(Date, nullable=False)
    data_checkout_previsto = Column(Date, nullable=False)
    status = Column(Enum(StatusReservaEnum), nullable=False, default=StatusReservaEnum.CREATED)
    valor_total = Column(Float, nullable=True)

    # Relacionamento com o modelo de Quarto
    quarto = relationship("Quarto", back_populates="reservas")
