from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.schemas.reserva_schema import ReservaCreate, ReservaResponse
from app.services import reserva_service

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    """Lista todas as reservas cadastradas."""
    return reserva_service.listar_reservas(db)


@router.get("/{reserva_id}", response_model=ReservaResponse)
def buscar_reserva(reserva_id: str, db: Session = Depends(get_db)):
    """Busca uma reserva específica pelo ID."""
    return reserva_service.buscar_reserva_por_id(db, reserva_id)


@router.post("/", response_model=ReservaResponse, status_code=201)
def criar_reserva(reserva_data: ReservaCreate, db: Session = Depends(get_db)):
    """Cria uma nova reserva validando datas e disponibilidade."""
    return reserva_service.criar_reserva(db, reserva_data)


@router.patch("/{reserva_id}/checkin", response_model=ReservaResponse)
def realizar_checkin(reserva_id: str, db: Session = Depends(get_db)):
    """Realiza o check-in de uma reserva (status: CREATED → CHECKED_IN)."""
    return reserva_service.realizar_checkin(db, reserva_id)


@router.patch("/{reserva_id}/checkout", response_model=ReservaResponse)
def realizar_checkout(reserva_id: str, db: Session = Depends(get_db)):
    """Realiza o check-out de uma reserva (status: CHECKED_IN → CHECKED_OUT)."""
    return reserva_service.realizar_checkout(db, reserva_id)


@router.patch("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(reserva_id: str, db: Session = Depends(get_db)):
    """Cancela uma reserva (status: CREATED → CANCELED)."""
    return reserva_service.cancelar_reserva(db, reserva_id)
