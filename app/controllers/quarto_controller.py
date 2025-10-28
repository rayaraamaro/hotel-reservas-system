from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.schemas.quarto_schema import QuartoCreate, QuartoResponse, StatusQuartoEnum
from app.services import quarto_service

router = APIRouter(prefix="/quartos", tags=["Quartos"])

# ===========================
# ROTAS DE QUARTOS (Controller)
# ===========================

@router.get("/", response_model=list[QuartoResponse])
def listar_quartos(db: Session = Depends(get_db)):
    """Lista todos os quartos cadastrados."""
    return quarto_service.listar_quartos(db)


@router.get("/{quarto_id}", response_model=QuartoResponse)
def buscar_quarto(quarto_id: str, db: Session = Depends(get_db)):
    """
    Busca um quarto específico pelo ID (UUID).
    """
    quarto = quarto_service.buscar_quarto_por_id(db, quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail=f"Quarto com ID {quarto_id} não encontrado.")
    return quarto


@router.post("/", response_model=QuartoResponse, status_code=201)
def criar_quarto(quarto_data: QuartoCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo quarto.
    - O número do quarto deve ser único.
    - O ID (UUID) é gerado automaticamente.
    """
    return quarto_service.criar_quarto(db, quarto_data)


@router.patch("/{quarto_id}/status", response_model=QuartoResponse)
def atualizar_status_quarto(
    quarto_id: str,
    novo_status: StatusQuartoEnum = Query(..., description="Novo status do quarto (ATIVO / INATIVO)"),
    db: Session = Depends(get_db),
):
    """
    Atualiza o status de um quarto (ATIVO / INATIVO).
    """
    quarto_atualizado = quarto_service.atualizar_status_quarto(db, quarto_id, novo_status)
    if not quarto_atualizado:
        raise HTTPException(status_code=404, detail=f"Quarto com ID {quarto_id} não encontrado.")
    return quarto_atualizado
