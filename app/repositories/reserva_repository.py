from sqlalchemy.orm import Session
from app.models.reserva_model import Reserva

# ===========================
# Camada de acesso ao banco (Repository)
# ===========================

def get_all_reservas(db: Session):
    """Retorna todas as reservas."""
    return db.query(Reserva).all()


def get_reserva_by_id(db: Session, reserva_id: str):
    """Busca uma reserva específica pelo ID."""
    return db.query(Reserva).filter(Reserva.id == reserva_id).first()


def get_reservas_por_quarto(db: Session, quarto_id: str):
    """Busca todas as reservas de um quarto específico."""
    return db.query(Reserva).filter(Reserva.quarto_id == quarto_id).all()


def create_reserva(db: Session, reserva: Reserva):
    """Cria uma nova reserva."""
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


def update_reserva_status(db: Session, reserva: Reserva, novo_status):
    """Atualiza o status de uma reserva existente."""
    reserva.status = novo_status
    db.commit()
    db.refresh(reserva)
    return reserva
