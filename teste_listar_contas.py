"""
Script de teste para listar contas correntes

Requisito: pip install requests
"""
import requests
import json
import sys

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


def listar_contas(token: str):
    """
    Lista todas as contas do usuário autenticado
    
    Args:
        token: Token JWT
    
    Returns:
        list: Lista de contas ou None em caso de erro
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print("\nListando contas...")
        response = requests.get(
            f"{API_URL}/api/v1/contas",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            contas = response.json()
            print("\n" + "=" * 60)
            print("SUCESSO! Contas listadas")
            print("=" * 60)
            
            if not contas:
                print("\nVoce nao possui contas cadastradas.")
                print("Crie uma conta usando: python teste_criar_conta.py")
                return []
            
            print(f"\nTotal de contas: {len(contas)}")
            print("\n" + "-" * 60)
            
            for i, conta in enumerate(contas, 1):
                print(f"\nConta {i}:")
                print(f"  ID: {conta['id']}")
                print(f"  Numero: {conta['numero']}")
                print(f"  Titular: {conta['titular']}")
                print(f"  Saldo: R$ {conta['saldo']:.2f}")
                print(f"  Criada em: {conta.get('created_at', 'N/A')}")
            
            return contas
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
    print("TESTE: Listar Contas Correntes")
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
    
    # Listar contas
    contas = listar_contas(token)
    
    if contas is not None:
        print("\n" + "=" * 60)
        print("PRONTO!")
        print("=" * 60)
        if contas:
            print("\nAgora voce pode:")
            print("  - Ver detalhes: GET /api/v1/contas/{conta_id}")
            print("  - Fazer transacoes: POST /api/v1/transacoes?conta_id={conta_id}")
            print("  - Ver extrato: GET /api/v1/transacoes/extrato/{conta_id}")
        print("\nOu acesse a documentacao em: http://localhost:8000/docs")

