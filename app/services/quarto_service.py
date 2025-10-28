from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import quarto_repository
from app.schemas.quarto_schema import QuartoCreate
from app.models.quarto_model import StatusQuartoEnum

# ===========================
# Camada de regras de negócio (Service)
# ===========================

def listar_quartos(db: Session):
    """Retorna todos os quartos cadastrados."""
    return quarto_repository.get_all_quartos(db)


def buscar_quarto_por_id(db: Session, quarto_id: str):
    """Busca um quarto pelo ID (UUID), ou lança erro se não encontrado."""
    quarto = quarto_repository.get_quarto_by_id(db, quarto_id)
    if not quarto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quarto com ID {quarto_id} não encontrado."
        )
    return quarto


def criar_quarto(db: Session, quarto_data: QuartoCreate):
    """Cria um novo quarto, garantindo que o número seja único."""
    quarto_existente = quarto_repository.get_quarto_by_numero(db, quarto_data.numero)
    if quarto_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"O número {quarto_data.numero} já está cadastrado."
        )

    return quarto_repository.create_quarto(db, quarto_data)


def atualizar_status_quarto(db: Session, quarto_id: str, novo_status: StatusQuartoEnum):
    """Atualiza o status (ATIVO/INATIVO) de um quarto."""
    quarto = quarto_repository.get_quarto_by_id(db, quarto_id)
    if not quarto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quarto com ID {quarto_id} não encontrado."
        )

    if quarto.status == novo_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O quarto já está com status {novo_status.value}."
        )

    return quarto_repository.update_quarto_status(db, quarto_id, novo_status)
