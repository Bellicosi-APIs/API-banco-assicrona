"""
Script de teste para obter detalhes de uma conta específica

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
    """Lista todas as contas do usuário"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/api/v1/contas", headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def obter_conta(token: str, conta_id: int):
    """
    Obtém os detalhes de uma conta específica
    
    Args:
        token: Token JWT
        conta_id: ID da conta
    
    Returns:
        dict: Dados da conta ou None em caso de erro
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print(f"\nObtendo detalhes da conta ID {conta_id}...")
        response = requests.get(
            f"{API_URL}/api/v1/contas/{conta_id}",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            conta = response.json()
            print("\n" + "=" * 60)
            print("SUCESSO! Detalhes da conta")
            print("=" * 60)
            print(f"\nID: {conta['id']}")
            print(f"Numero: {conta['numero']}")
            print(f"Titular: {conta['titular']}")
            print(f"Saldo: R$ {conta['saldo']:.2f}")
            print(f"Usuario ID: {conta['usuario_id']}")
            print(f"Criada em: {conta.get('created_at', 'N/A')}")
            if conta.get('updated_at'):
                print(f"Atualizada em: {conta['updated_at']}")
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
    print("TESTE: Obter Conta Especifica")
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
    
    # Listar contas para ajudar o usuário
    print("\n" + "-" * 60)
    print("Listando suas contas...")
    print("-" * 60)
    contas = listar_contas(token)
    
    if contas:
        print("\nSuas contas:")
        for conta in contas:
            print(f"  ID {conta['id']}: {conta['numero']} - {conta['titular']} (Saldo: R$ {conta['saldo']:.2f})")
    else:
        print("\nVoce nao possui contas cadastradas.")
        print("Crie uma conta primeiro usando: python teste_criar_conta.py")
        sys.exit(1)
    
    # Obter ID da conta
    print("\n" + "-" * 60)
    conta_id_str = input("Digite o ID da conta que deseja ver: ").strip()
    
    try:
        conta_id = int(conta_id_str)
    except ValueError:
        print("ERRO: ID deve ser um numero inteiro!")
        sys.exit(1)
    
    # Verificar se a conta existe na lista
    conta_existe = any(c['id'] == conta_id for c in contas)
    if not conta_existe:
        print(f"AVISO: Conta ID {conta_id} nao encontrada na sua lista de contas.")
        resposta = input("Deseja continuar mesmo assim? (s/n): ").strip().lower()
        if resposta != 's':
            sys.exit(0)
    
    # Obter conta
    conta = obter_conta(token, conta_id)
    
    if conta:
        print("\n" + "=" * 60)
        print("PRONTO!")
        print("=" * 60)
        print("\nAgora voce pode:")
        print(f"  - Fazer transacoes: POST /api/v1/transacoes?conta_id={conta_id}")
        print(f"  - Ver extrato: GET /api/v1/transacoes/extrato/{conta_id}")
        print("\nOu acesse a documentacao em: http://localhost:8000/docs")

