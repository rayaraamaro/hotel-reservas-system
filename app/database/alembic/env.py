from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os
import sys

from app.models.quarto_model import Quarto
from app.models.reserva_model import Reserva

# Adicionar o caminho raiz do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

# Importar Base e config do projeto
from app.database.config import Base, DATABASE_URL

# Carregar variáveis do .env
load_dotenv()

# Configuração padrão Alembic
config = context.config
fileConfig(config.config_file_name)

# Substituir URL da conexão
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata
# Ignorar tabelas antigas existentes no banco Oracle
def include_object(object, name, type_, reflected, compare_to):
    # Só incluir tabelas do projeto (as que começam com TB_)
    if type_ == "table" and not name.startswith("TB_"):
        return False
    return True


def run_migrations_offline():
    """Executa as migrações no modo offline (gera SQL sem executar)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa migrações conectando-se ao banco."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
