# Sistema de Reserva de Hotel

API REST desenvolvida com **FastAPI**, **SQLAlchemy** e **Oracle Database**, seguindo o padrão de arquitetura **MVC (Model-View-Controller)**.  
O sistema permite **gerenciar quartos e reservas de um hotel**, com regras de negócio completas e migrações automatizadas via **Alembic**.

---
## Integrantes
- **Erick Molina** – RM 553852  
- **Felipe Castro Salazar** – RM 553464  
- **Marcelo Vieira de Melo** – RM 552953  
- **Rayara Amaro Figueiredo** – RM 552635  
- **Victor Rodrigues** – RM 554158  

---
### Funcionalidades Principais

| Categoria | Funcionalidade |
|------------|----------------|
| Quartos | • Listar todos os quartos <br>• Cadastrar novo quarto <br>• Atualizar status (ATIVO/INATIVO) |
| Reservas | • Criar reserva validando disponibilidade e datas <br>• Listar reservas existentes <br>• Realizar check-in e check-out <br>• Cancelar reserva |
| Banco & Infra | • Migrações automáticas com Alembic <br>• Script de **seed** para dados iniciais <br>• UUIDs como chaves primárias |

---

### Arquitetura do Projeto

O projeto segue o padrão **MVC**, organizado da seguinte forma:
```
hotel_reservas/
│
├── app/
│   ├── main.py                     # Inicialização da aplicação FastAPI
│   ├── controllers/                # Camada Controller (rotas)
│   │   ├── quarto_controller.py
│   │   └── reserva_controller.py
│   ├── services/                   # Camada Service (regras de negócio)
│   │   ├── quarto_service.py
│   │   └── reserva_service.py
│   ├── repositories/               # Camada Repository (acesso ao banco)
│   │   ├── quarto_repository.py
│   │   └── reserva_repository.py
│   ├── models/                     # Modelos ORM (SQLAlchemy)
│   │   ├── quarto_model.py
│   │   └── reserva_model.py
│   ├── schemas/                    # Modelos Pydantic (validação e resposta)
│   │   ├── quarto_schema.py
│   │   └── reserva_schema.py
│   └── database/                   # Configuração e migrações
│       ├── config.py
│       ├── seed.py
│       └── alembic/
│           └── versions/           # Scripts de migração Alembic
│
├── .env
│
├── .env.example
│
├── alembic.ini
│
├── requirements.txt
│
└── README.md
```
---
### Fluxo da Arquitetura:

```
[Cliente/Swagger]
        │
        ▼
[Controller] → Define endpoints e recebe requisições HTTP
        │
        ▼
[Service] → Aplica regras de negócio e validações
        │
        ▼
[Repository] → Interage com o banco de dados via SQLAlchemy
        │
        ▼
[Oracle Database] → Banco de dados
```
---
## Banco de Dados

O sistema utiliza **Oracle Database** e gerencia as tabelas abaixo:

---

### TB_QUARTO
| Campo | Tipo | Descrição |
|--------|------|-----------|
| `id` | CHAR(36) | Identificador único (UUID) |
| `numero` | INTEGER | Número do quarto |
| `tipo` | ENUM | STANDARD, DELUXE, SUITE |
| `capacidade` | INTEGER | Número de hóspedes |
| `valor_diaria` | FLOAT | Valor da diária |
| `status` | ENUM | ATIVO, INATIVO |

### TB_RESERVA
| Campo | Tipo | Descrição |
|--------|------|-----------|
| `id` | CHAR(36) | Identificador único (UUID) |
| `quarto_id` | CHAR(36) | Chave estrangeira para TB_QUARTO |
| `nome_hospede` | VARCHAR(100) | Nome do hóspede |
| `data_checkin_previsto` | DATE | Data prevista de entrada |
| `data_checkout_previsto` | DATE | Data prevista de saída |
| `status` | ENUM | CREATED, CHECKED_IN, CHECKED_OUT, CANCELED |
| `valor_total` | FLOAT | Valor calculado no check-out |

---

### Script de Migração de Dados (Alembic)

O projeto utiliza **Alembic** para versionar e aplicar alterações no banco de dados.

---

### Criar nova migração:

```bash
alembic revision --autogenerate -m "mensagem da migração"
```
Aplicar migração:

```
alembic upgrade head
```

---
### Seed de Dados Iniciais

O arquivo app/database/seed.py insere automaticamente alguns quartos de exemplo ao iniciar o sistema:

```
    [
    {"numero": 101, "tipo": "STANDARD", "capacidade": 2, "valor_diaria": 250.0, "status": "ATIVO"},
    {"numero": 102, "tipo": "DELUXE", "capacidade": 3, "valor_diaria": 350.0, "status": "ATIVO"},
    {"numero": 201, "tipo": "SUITE", "capacidade": 4, "valor_diaria": 550.0, "status": "ATIVO"}
    ]
```

---
### Como Executar o Projeto

1. Criar e ativar o ambiente virtual

```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

2. Instalar dependências

```
pip install -r requirements.txt
```

3. Configurar o banco Oracle

```
No .env.example adicione suas credencias para conectar no banco Oracle
```
4. Executar o servidor

```
uvicorn app.main:app --reload

ou

python app/main.py
```

---

### Documentação da API

Após rodar o servidor, acesse:

**Swagger UI: http://127.0.0.1:8000/docs**

---

### Tecnologias Utilizadas

- FastAPI — framework principal da aplicação

- SQLAlchemy ORM — mapeamento objeto-relacional

- Alembic — controle de migrações

- Oracle Database — banco de dados relacional

- Pydantic v2 — validação e serialização de dados

- Uvicorn — servidor ASGI para FastAPI

---

### Regras de Negócio Principais

- `data_checkout_previsto` deve ser posterior ao `data_checkin_previsto`.

- Um quarto **não pode ter reservas sobrepostas nas datas**.

---

#### Fluxos de status permitidos:

- CREATED → CHECKED_IN → CHECKED_OUT

- CREATED → CANCELED

- Tentativas de transição inválidas retornam 409 Conflict.


#### Desenvolvido para a disciplina SOA - FIAP (2025)


