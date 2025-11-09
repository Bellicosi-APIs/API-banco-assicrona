"""
Script de teste para obter informações do usuário autenticado

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


def obter_usuario(token: str):
    """
    Obtém as informações do usuário autenticado
    
    Args:
        token: Token JWT
    
    Returns:
        dict: Dados do usuário ou None em caso de erro
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print("\nObtendo informacoes do usuario...")
        response = requests.get(
            f"{API_URL}/api/v1/auth/me",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            usuario = response.json()
            print("\n" + "=" * 60)
            print("SUCESSO! Informacoes do usuario")
            print("=" * 60)
            print(f"\nID: {usuario['id']}")
            print(f"Username: {usuario['username']}")
            print(f"Email: {usuario['email']}")
            return usuario
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
    print("TESTE: Obter Informacoes do Usuario")
    print("=" * 60)
    
    # Credenciais
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
    
    # Obter usuário
    usuario = obter_usuario(token)
    
    if usuario:
        print("\n" + "=" * 60)
        print("PRONTO!")
        print("=" * 60)
        print("\nAgora voce pode:")
        print("  - Criar contas: POST /api/v1/contas")
        print("  - Listar contas: GET /api/v1/contas")
        print("  - Fazer transacoes: POST /api/v1/transacoes")
        print("\nOu acesse a documentacao em: http://localhost:8000/docs")

