from sqlalchemy.orm import Session
from app.models.quarto_model import Quarto
from app.schemas.quarto_schema import QuartoCreate

# ===========================
# Camada de acesso ao banco (Repository)
# ===========================

def get_all_quartos(db: Session):
    """Lista todos os quartos cadastrados."""
    return db.query(Quarto).all()


def get_quarto_by_id(db: Session, quarto_id: str):
    """Busca um quarto específico pelo ID (UUID)."""
    return db.query(Quarto).filter(Quarto.id == quarto_id).first()


def get_quarto_by_numero(db: Session, numero: int):
    """Busca um quarto pelo número (único)."""
    return db.query(Quarto).filter(Quarto.numero == numero).first()


def create_quarto(db: Session, quarto_data: QuartoCreate):
    """Cria um novo quarto."""
    novo_quarto = Quarto(**quarto_data.model_dump())  # Usa Pydantic v2
    db.add(novo_quarto)
    db.commit()
    db.refresh(novo_quarto)
    return novo_quarto


def update_quarto_status(db: Session, quarto_id: str, novo_status: str):
    """Atualiza o status de um quarto (ATIVO/INATIVO)."""
    quarto = get_quarto_by_id(db, quarto_id)
    if not quarto:
        return None

    quarto.status = novo_status
    db.commit()
    db.refresh(quarto)
    return quarto
