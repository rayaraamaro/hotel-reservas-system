import subprocess
import uvicorn
from fastapi import FastAPI
from app.controllers import quarto_controller, reserva_controller
from app.database.config import Base, engine
from app.database.seed import seed_data


def run_migrations():
    """Executa automaticamente as migrações Alembic na inicialização."""
    try:
        print("Executando migrações Alembic automaticamente...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migrações aplicadas com sucesso!")
    except Exception as e:
        print(f"Erro ao aplicar migrações: {e}")


# Executa as migrações e insere os dados iniciais
run_migrations()
seed_data()

# Cria as tabelas localmente (caso não existam)
Base.metadata.create_all(bind=engine)

# Inicializa o app FastAPI
app = FastAPI(title="Hotel Reservas API", version="1.0.0")

# Inclui as rotas
app.include_router(quarto_controller.router)
app.include_router(reserva_controller.router)


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Bem-vinda à API de Hotel Reservas! Acesse /docs para ver os endpoints."
    }

if __name__ == "__main__":
    """Permite rodar o servidor diretamente com `python app/main.py`."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )