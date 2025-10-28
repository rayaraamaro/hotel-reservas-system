from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.reserva_model import Reserva, StatusReservaEnum
from app.repositories import reserva_repository, quarto_repository
from app.schemas.reserva_schema import ReservaCreate

# ===========================
# Camada de regras de negócio (Service)
# ===========================

def listar_reservas(db: Session):
    """Lista todas as reservas existentes."""
    return reserva_repository.get_all_reservas(db)


def buscar_reserva_por_id(db: Session, reserva_id: str):
    """Busca uma reserva pelo ID."""
    reserva = reserva_repository.get_reserva_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva com ID {reserva_id} não encontrada."
        )
    return reserva


def criar_reserva(db: Session, reserva_data: ReservaCreate):
    """Cria uma reserva validando datas e disponibilidade do quarto."""

    # 1. Validação de datas
    if reserva_data.data_checkout_previsto <= reserva_data.data_checkin_previsto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de check-out deve ser posterior à data de check-in."
        )

    # 2. Verifica se o quarto existe e está ativo
    quarto = quarto_repository.get_quarto_by_id(db, reserva_data.quarto_id)
    if not quarto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto informado não existe."
        )
    if quarto.status.name != "ATIVO":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível reservar um quarto inativo."
        )

    # 3. Verifica disponibilidade (sem sobreposição de datas)
    reservas_existentes = reserva_repository.get_reservas_por_quarto(db, reserva_data.quarto_id)
    for r in reservas_existentes:
        if r.status != StatusReservaEnum.CANCELED:
            if not (
                reserva_data.data_checkout_previsto <= r.data_checkin_previsto or
                reserva_data.data_checkin_previsto >= r.data_checkout_previsto
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="O quarto já está reservado neste período."
                )

    # 4. Cria a reserva
    nova_reserva = Reserva(
        quarto_id=reserva_data.quarto_id,
        nome_hospede=reserva_data.nome_hospede,
        data_checkin_previsto=reserva_data.data_checkin_previsto,
        data_checkout_previsto=reserva_data.data_checkout_previsto,
        status=StatusReservaEnum.CREATED,
        valor_total=reserva_data.valor_total
    )

    return reserva_repository.create_reserva(db, nova_reserva)


def realizar_checkin(db: Session, reserva_id: str):
    """Realiza o check-in de uma reserva (somente se estiver no status CREATED)."""
    reserva = buscar_reserva_por_id(db, reserva_id)

    if reserva.status != StatusReservaEnum.CREATED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Só é possível fazer check-in em reservas com status CREATED."
        )

    return reserva_repository.update_reserva_status(db, reserva, StatusReservaEnum.CHECKED_IN)


def realizar_checkout(db: Session, reserva_id: str):
    """Realiza o check-out de uma reserva (somente se estiver CHECKED_IN)."""
    reserva = buscar_reserva_por_id(db, reserva_id)

    if reserva.status != StatusReservaEnum.CHECKED_IN:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Só é possível fazer check-out em reservas com status CHECKED_IN."
        )

    # Cálculo automático do valor total (dias * valor diária)
    dias = (reserva.data_checkout_previsto - reserva.data_checkin_previsto).days
    quarto = quarto_repository.get_quarto_by_id(db, reserva.quarto_id)
    reserva.valor_total = dias * quarto.valor_diaria

    return reserva_repository.update_reserva_status(db, reserva, StatusReservaEnum.CHECKED_OUT)


def cancelar_reserva(db: Session, reserva_id: str):
    """Cancela uma reserva (somente se ainda não tiver check-in)."""
    reserva = buscar_reserva_por_id(db, reserva_id)

    if reserva.status in [StatusReservaEnum.CHECKED_IN, StatusReservaEnum.CHECKED_OUT]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível cancelar uma reserva já iniciada ou finalizada."
        )

    return reserva_repository.update_reserva_status(db, reserva, StatusReservaEnum.CANCELED)
