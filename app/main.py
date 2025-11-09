from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.models import Conta, Transacao, Usuario  # Importar modelos para criação das tabelas
from app.routers import auth, contas, transacoes

# Lifespan context manager para inicializar o banco de dados
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: inicializar banco de dados
    await init_db()
    yield
    # Shutdown: cleanup se necessário
    pass


# Criar aplicação FastAPI
app = FastAPI(
    title="API Bancária Assíncrona",
    description="""
    API REST assíncrona para gerenciamento de contas correntes e transações bancárias.
    
    ## Funcionalidades
    
    * **Autenticação JWT**: Sistema completo de autenticação com tokens JWT
    * **Gerenciamento de Contas**: Criação e listagem de contas correntes
    * **Transações**: Depósitos e saques com validações de saldo
    * **Extrato**: Histórico completo de transações por conta
    
    ## Autenticação
    
    A maioria dos endpoints requer autenticação JWT. Para usar:
    
    1. Registre um usuário em `/api/v1/auth/register`
    2. Faça login em `/api/v1/auth/login` para obter o token
    3. Use o token no header: `Authorization: Bearer <seu_token>`
    
    ## Validações
    
    * Valores de transação devem ser maiores que zero
    * Saques só são permitidos quando há saldo suficiente
    * Contas e usuários têm validações de unicidade
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(contas.router)
app.include_router(transacoes.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz da API.
    
    Retorna informações básicas sobre a API.
    """
    return {
        "message": "Bem-vindo à API Bancária Assíncrona",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de health check.
    
    Verifica se a API está funcionando corretamente.
    """
    return {"status": "healthy"}

