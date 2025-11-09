"""Script de teste para criar usuário"""
import requests
import json
import time
import sys

# Configuração
API_URL = "http://localhost:8000"

def criar_usuario_teste():
    """Cria um usuário de teste"""
    # Gerar username e email únicos
    timestamp = str(int(time.time()))
    username = f"usuario_teste_{timestamp}"
    email = f"teste_{timestamp}@example.com"
    password = "senha123"
    
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    print("=" * 60)
    print("TESTE: Criando Usuario")
    print("=" * 60)
    print(f"\nDados do usuario:")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print("\nEnviando requisicao...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/auth/register",
            json=data,
            timeout=5
        )
        
        if response.status_code == 201:
            usuario = response.json()
            print("\n" + "=" * 60)
            print("SUCESSO! Usuario criado!")
            print("=" * 60)
            print(f"\nID: {usuario['id']}")
            print(f"Username: {usuario['username']}")
            print(f"Email: {usuario['email']}")
            
            # Agora fazer login
            print("\n" + "-" * 60)
            print("Fazendo login para obter token...")
            print("-" * 60)
            
            login_data = {
                "username": username,
                "password": password
            }
            
            login_response = requests.post(
                f"{API_URL}/api/v1/auth/login",
                json=login_data,
                timeout=5
            )
            
            if login_response.status_code == 200:
                token_data = login_response.json()
                token = token_data['access_token']
                print("\nLogin realizado com sucesso!")
                print(f"\nToken JWT (primeiros 50 caracteres): {token[:50]}...")
                print(f"Token completo: {token}")
                print("\n" + "=" * 60)
                print("PRONTO! Voce pode usar este token nas requisicoes protegidas")
                print("=" * 60)
                print(f"\nHeader: Authorization: Bearer {token}")
                return True
            else:
                print(f"\nErro no login: {login_response.status_code}")
                print(login_response.text)
                return False
        else:
            print(f"\nErro ao criar usuario: {response.status_code}")
            try:
                error = response.json()
                print(f"Detalhes: {error.get('detail', 'Erro desconhecido')}")
            except:
                print(f"Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\nERRO: Nao foi possivel conectar a API.")
        print("Certifique-se de que a API esta rodando:")
        print("  python run.py")
        return False
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        return False

if __name__ == "__main__":
    criar_usuario_teste()

