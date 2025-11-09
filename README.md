# API Bancária Assíncrona com FastAPI

API REST assíncrona para gerenciamento de contas correntes e transações bancárias (depósitos e saques) com autenticação JWT.

## 🚀 Funcionalidades

- ✅ **Autenticação JWT**: Sistema completo de autenticação com tokens JWT
- ✅ **Gerenciamento de Contas**: Criação e listagem de contas correntes
- ✅ **Transações**: Depósitos e saques com validações de saldo
- ✅ **Extrato**: Histórico completo de transações por conta
- ✅ **Validações**: Impede valores negativos e saques sem saldo suficiente
- ✅ **Documentação**: Documentação automática com Swagger UI e ReDoc

## 📋 Pré-requisitos

- Python 3.8+
- pip

## 🔧 Instalação

1. Clone o repositório ou navegue até o diretório do projeto:
```bash
cd api_bank
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. (Opcional) Configure variáveis de ambiente criando um arquivo `.env`:
```env
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite+aiosqlite:///./bank.db
```

## 🏃 Executando a API

Para iniciar o servidor de desenvolvimento:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Endpoints

### Autenticação

- `POST /api/v1/auth/register` - Registrar novo usuário
- `POST /api/v1/auth/login` - Fazer login e obter token JWT
- `GET /api/v1/auth/me` - Obter informações do usuário atual

### Contas

- `POST /api/v1/contas` - Criar nova conta corrente
- `GET /api/v1/contas` - Listar todas as contas do usuário
- `GET /api/v1/contas/{conta_id}` - Obter detalhes de uma conta

### Transações

- `POST /api/v1/transacoes?conta_id={conta_id}` - Criar transação (depósito ou saque)
- `GET /api/v1/transacoes/extrato/{conta_id}` - Obter extrato completo da conta

## 📖 Tutoriais Completos

Para aprender a usar cada funcionalidade da API, consulte os tutoriais detalhados:

### 🚀 Início Rápido
- [Índice de Tutoriais](INDICE_TUTORIAIS.md) - Visão geral de todos os tutoriais
- [Guia Rápido](GUIA_RAPIDO.md) - Comece aqui para uma visão geral
- [Tutorial: Fazer Login](TUTORIAL_FAZER_LOGIN.md) - Como fazer login e obter tokens

### 👤 Autenticação
- [Tutorial: Criar Usuário](TUTORIAL_CRIAR_USUARIO.md) - Como criar um novo usuário
- [Tutorial: Fazer Login](TUTORIAL_FAZER_LOGIN.md) - Como fazer login e obter token JWT
- [Tutorial: Obter Usuário](TUTORIAL_OBTER_USUARIO.md) - Como obter informações do usuário autenticado

### 💳 Contas Correntes
- [Tutorial: Criar Conta](TUTORIAL_CRIAR_CONTA.md) - Como criar uma conta corrente
- [Tutorial: Listar Contas](TUTORIAL_LISTAR_CONTAS.md) - Como listar todas as suas contas
- [Tutorial: Obter Conta Específica](TUTORIAL_OBTER_CONTA.md) - Como ver detalhes de uma conta

### 💰 Transações
- [Tutorial: Criar Transação](TUTORIAL_CRIAR_TRANSACAO.md) - Como fazer depósitos e saques
- [Tutorial: Ver Extrato](TUTORIAL_VER_EXTRATO.md) - Como ver o histórico completo de transações

### 🧪 Scripts de Teste

Todos os tutoriais incluem scripts Python para testes:

- `teste_criar_usuario.py` - Criar usuário
- `teste_fazer_login.py` - Fazer login
- `teste_obter_usuario.py` - Obter informações do usuário
- `teste_criar_conta.py` - Criar conta
- `teste_listar_contas.py` - Listar contas
- `teste_obter_conta.py` - Obter conta específica
- `teste_criar_transacao.py` - Criar transação
- `teste_ver_extrato.py` - Ver extrato

## 🔐 Autenticação

A maioria dos endpoints requer autenticação JWT. Para usar:

### 1. Criar Usuário

**Opção A: Usando a interface web (mais fácil)**
1. Acesse http://localhost:8000/docs
2. Encontre `POST /api/v1/auth/register`
3. Clique em "Try it out"
4. Preencha os dados e clique em "Execute"

**Opção B: Usando o script Python**
```bash
python criar_usuario.py
```

**Opção C: Usando cURL/PowerShell**
```bash
POST /api/v1/auth/register
{
  "username": "joao_silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

### 2. Fazer Login

Faça login para obter o token:
```bash
POST /api/v1/auth/login
{
  "username": "joao_silva",
  "password": "senha123"
}
```

### 3. Usar o Token

Use o token nos headers das requisições:
```
Authorization: Bearer <seu_token>
```

📖 **Veja o guia completo:** [GUIA_RAPIDO.md](GUIA_RAPIDO.md)

## 📝 Exemplos de Uso

### 1. Criar uma conta

```bash
POST /api/v1/contas
Authorization: Bearer <token>
{
  "numero": "12345-6",
  "titular": "João Silva"
}
```

### 2. Fazer um depósito

```bash
POST /api/v1/transacoes?conta_id=1
Authorization: Bearer <token>
{
  "tipo": "deposito",
  "valor": 1000.00,
  "descricao": "Depósito inicial"
}
```

### 3. Fazer um saque

```bash
POST /api/v1/transacoes?conta_id=1
Authorization: Bearer <token>
{
  "tipo": "saque",
  "valor": 100.00,
  "descricao": "Saque para compras"
}
```

### 4. Obter extrato

```bash
GET /api/v1/transacoes/extrato/1
Authorization: Bearer <token>
```

## ✅ Validações

- ✅ Valores de transação devem ser maiores que zero
- ✅ Saques só são permitidos quando há saldo suficiente
- ✅ Contas e usuários têm validações de unicidade
- ✅ Usuários só podem acessar suas próprias contas e transações

## 🏗️ Estrutura do Projeto

```
api_bank/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação principal FastAPI
│   ├── config.py               # Configurações
│   ├── database.py             # Configuração do banco de dados
│   ├── auth.py                 # Autenticação JWT
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── conta.py
│   │   └── transacao.py
│   ├── schemas/                # Schemas Pydantic
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── conta.py
│   │   └── transacao.py
│   └── routers/                # Rotas/Endpoints
│       ├── __init__.py
│       ├── auth.py
│       ├── contas.py
│       └── transacoes.py
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validação de dados
- **JWT**: Autenticação com tokens
- **Bcrypt**: Hash de senhas
- **SQLite**: Banco de dados (pode ser facilmente alterado para PostgreSQL, MySQL, etc.)

## 📄 Licença

Este projeto é um exemplo educacional.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

