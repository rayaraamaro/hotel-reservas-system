import uuid
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.database.config import SessionLocal
from app.models.quarto_model import Quarto, TipoQuartoEnum, StatusQuartoEnum
from app.models.reserva_model import Reserva, StatusReservaEnum


def seed_data():
    """Insere dados iniciais (seed) apenas se o banco estiver vazio."""
    db: Session = SessionLocal()
    try:
        # -----------------------------
        # QUARTOS INICIAIS
        # -----------------------------
        if db.query(Quarto).count() == 0:
            quartos = [
                Quarto(
                    id=str(uuid.uuid4()),
                    numero=101,
                    tipo=TipoQuartoEnum.STANDARD,
                    capacidade=2,
                    valor_diaria=250.0,
                    status=StatusQuartoEnum.ATIVO
                ),
                Quarto(
                    id=str(uuid.uuid4()),
                    numero=102,
                    tipo=TipoQuartoEnum.DELUXE,
                    capacidade=3,
                    valor_diaria=350.0,
                    status=StatusQuartoEnum.ATIVO
                ),
                Quarto(
                    id=str(uuid.uuid4()),
                    numero=201,
                    tipo=TipoQuartoEnum.SUITE,
                    capacidade=4,
                    valor_diaria=550.0,
                    status=StatusQuartoEnum.ATIVO
                )
            ]
            db.add_all(quartos)
            db.commit()
            print("Quartos iniciais inseridos com sucesso.")
        else:
            print("Quartos já existentes — seed ignorado.")

        # -----------------------------
        # RESERVAS INICIAIS
        # -----------------------------
        if db.query(Reserva).count() == 0:
            quarto_exemplo = db.query(Quarto).first()
            if quarto_exemplo:
                reserva = Reserva(
                    id=str(uuid.uuid4()),
                    quarto_id=quarto_exemplo.id,
                    nome_hospede="João da Silva",
                    data_checkin_previsto=date.today(),
                    data_checkout_previsto=date.today() + timedelta(days=3),
                    status=StatusReservaEnum.CREATED,
                    valor_total=quarto_exemplo.valor_diaria * 3
                )
                db.add(reserva)
                db.commit()
                print("Reserva inicial inserida com sucesso.")
            else:
                print("Nenhum quarto encontrado — reserva não criada.")
        else:
            print("Reservas já existentes — seed ignorado.")

    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir dados iniciais: {e}")
    finally:
        db.close()
