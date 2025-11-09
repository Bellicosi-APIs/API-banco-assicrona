"""
Script de teste para criar uma conta corrente

Requisito: pip install requests
"""
import requests
import json
import sys
import time

# Configuração
API_URL = "http://localhost:8000"


def fazer_login(username: str, password: str):
    """Faz login e retorna o token"""
    try:
        response = requests.post(
            f"{API_URL}/api/v1/auth/login",
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return None


def criar_conta(token: str, numero: str, titular: str):
    """
    Cria uma conta corrente
    
    Args:
        token: Token JWT
        numero: Número da conta
        titular: Nome do titular
    
    Returns:
        dict: Dados da conta criada ou None em caso de erro
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "numero": numero,
        "titular": titular
    }
    
    try:
        print(f"\nCriando conta: {numero} - {titular}...")
        response = requests.post(
            f"{API_URL}/api/v1/contas",
            json=data,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 201:
            conta = response.json()
            print("\n" + "=" * 60)
            print("SUCESSO! Conta criada!")
            print("=" * 60)
            print(f"\nID: {conta['id']}")
            print(f"Numero: {conta['numero']}")
            print(f"Titular: {conta['titular']}")
            print(f"Saldo: R$ {conta['saldo']:.2f}")
            print(f"Usuario ID: {conta['usuario_id']}")
            print(f"Criada em: {conta.get('created_at', 'N/A')}")
            return conta
        else:
            print(f"\nERRO: {response.status_code}")
            try:
                error = response.json()
                print(f"Detalhes: {error.get('detail', 'Erro desconhecido')}")
            except:
                print(f"Resposta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("\nERRO: Nao foi possivel conectar a API.")
        print("   Certifique-se de que a API esta rodando: python run.py")
        return None
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("TESTE: Criar Conta Corrente")
    print("=" * 60)
    
    # Credenciais (altere conforme necessário)
    print("\nPreencha as credenciais:")
    username = input("Username: ").strip()
    if not username:
        print("ERRO: Username nao pode estar vazio!")
        sys.exit(1)
    
    password = input("Password: ").strip()
    if not password:
        print("ERRO: Password nao pode estar vazio!")
        sys.exit(1)
    
    # Fazer login
    print("\nFazendo login...")
    token = fazer_login(username, password)
    
    if not token:
        print("\nERRO: Nao foi possivel fazer login.")
        print("   Verifique se o username e password estao corretos.")
        sys.exit(1)
    
    print("Login realizado com sucesso!")
    
    # Dados da conta
    print("\n" + "-" * 60)
    print("Dados da conta:")
    print("-" * 60)
    
    numero = input("Numero da conta (ex: 12345-6): ").strip()
    if not numero:
        # Gerar número único baseado em timestamp
        timestamp = str(int(time.time()))
        numero = f"{timestamp[-6:]}-{timestamp[-1]}"
        print(f"Usando numero gerado: {numero}")
    
    titular = input("Nome do titular: ").strip()
    if not titular:
        titular = "Titular Teste"
        print(f"Usando titular padrao: {titular}")
    
    # Criar conta
    conta = criar_conta(token, numero, titular)
    
    if conta:
        print("\n" + "=" * 60)
        print("PRONTO! Conta criada com sucesso.")
        print("=" * 60)
        print("\nAgora voce pode:")
        print("  - Fazer depositos: POST /api/v1/transacoes?conta_id=" + str(conta['id']))
        print("  - Fazer saques: POST /api/v1/transacoes?conta_id=" + str(conta['id']))
        print("  - Ver extrato: GET /api/v1/transacoes/extrato/" + str(conta['id']))
        print("\nOu acesse a documentacao em: http://localhost:8000/docs")

