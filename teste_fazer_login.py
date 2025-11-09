"""
Script para fazer login na API Bancária e obter token JWT

Requisito: pip install requests
"""
import requests
import json
import sys

# Configuração
API_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{API_URL}/api/v1/auth/login"


def fazer_login(username: str, password: str):
    """
    Faz login na API e obtém o token JWT
    
    Args:
        username: Nome de usuário
        password: Senha do usuário
    
    Returns:
        str: Token JWT ou None em caso de erro
    """
    data = {
        "username": username,
        "password": password
    }
    
    try:
        print("Fazendo login...")
        response = requests.post(LOGIN_ENDPOINT, json=data, timeout=5)
        response.raise_for_status()
        
        token_data = response.json()
        token = token_data['access_token']
        token_type = token_data.get('token_type', 'bearer')
        
        print("\n" + "=" * 60)
        print("✅ LOGIN REALIZADO COM SUCESSO!")
        print("=" * 60)
        print(f"\nToken Type: {token_type}")
        print(f"\nToken JWT (primeiros 50 caracteres):")
        print(f"  {token[:50]}...")
        print(f"\nToken Completo:")
        print(f"  {token}")
        print("\n" + "-" * 60)
        print("COMO USAR O TOKEN:")
        print("-" * 60)
        print(f"\nHeader Authorization:")
        print(f"  Authorization: Bearer {token}")
        print("\n" + "=" * 60)
        
        return token
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar à API.")
        print("   Certifique-se de que a API está rodando:")
        print("   python run.py")
        return None
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("\n❌ ERRO: Credenciais inválidas!")
            print("   Verifique se o username e senha estão corretos.")
        else:
            print(f"\n❌ ERRO HTTP: {e}")
        try:
            error_detail = e.response.json()
            print(f"   Detalhes: {error_detail.get('detail', 'Erro desconhecido')}")
        except:
            print(f"   Resposta: {e.response.text}")
        return None
    
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")
        return None


def testar_token(token: str):
    """
    Testa se o token está funcionando fazendo uma requisição protegida
    
    Args:
        token: Token JWT
    """
    try:
        print("\n" + "=" * 60)
        print("TESTANDO TOKEN...")
        print("=" * 60)
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Testar endpoint protegido
        response = requests.get(
            f"{API_URL}/api/v1/auth/me",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("\n✅ Token válido!")
            print(f"\nUsuário autenticado:")
            print(f"  ID: {user_data['id']}")
            print(f"  Username: {user_data['username']}")
            print(f"  Email: {user_data['email']}")
        else:
            print(f"\n❌ Token inválido ou expirado (Status: {response.status_code})")
            
    except Exception as e:
        print(f"\n❌ Erro ao testar token: {e}")


if __name__ == "__main__":
    # Verificar se requests está instalado
    try:
        import requests
    except ImportError:
        print("❌ Erro: A biblioteca 'requests' não está instalada.")
        print("   Instale com: pip install requests")
        sys.exit(1)
    
    print("=" * 60)
    print("LOGIN - API Bancária")
    print("=" * 60)
    print()
    
    # Solicitar credenciais
    username = input("Digite o username: ").strip()
    if not username:
        print("❌ Username não pode estar vazio!")
        sys.exit(1)
    
    password = input("Digite a senha: ").strip()
    if not password:
        print("❌ Senha não pode estar vazia!")
        sys.exit(1)
    
    print()
    
    # Fazer login
    token = fazer_login(username, password)
    
    if token:
        # Testar token
        testar_token(token)
        
        print("\n" + "=" * 60)
        print("PRONTO! Você pode usar este token nas requisições protegidas.")
        print("=" * 60)
        print("\nOu acesse a documentação em: http://localhost:8000/docs")
        print("   Clique em 'Authorize' e cole o token!")

