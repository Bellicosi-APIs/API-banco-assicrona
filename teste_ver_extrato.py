"""
Script de teste para ver o extrato de uma conta

Requisito: pip install requests
"""
import requests
import json
import sys
from datetime import datetime

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


def ver_extrato(token: str, conta_id: int):
    """
    Obtém o extrato de uma conta
    
    Args:
        token: Token JWT
        conta_id: ID da conta
    
    Returns:
        dict: Dados do extrato ou None em caso de erro
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print(f"\nObtendo extrato da conta ID {conta_id}...")
        response = requests.get(
            f"{API_URL}/api/v1/transacoes/extrato/{conta_id}",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            extrato = response.json()
            
            print("\n" + "=" * 60)
            print("EXTRATO BANCARIO")
            print("=" * 60)
            print(f"\nConta: {extrato['numero_conta']}")
            print(f"Titular: {extrato['titular']}")
            print(f"Saldo Atual: R$ {extrato['saldo_atual']:.2f}")
            print(f"Total de Transacoes: {extrato['total_transacoes']}")
            
            print("\n" + "-" * 60)
            print("TRANSACOES")
            print("-" * 60)
            
            if not extrato['transacoes']:
                print("\nNenhuma transacao encontrada.")
            else:
                for i, transacao in enumerate(extrato['transacoes'], 1):
                    tipo = "DEPOSITO" if transacao['tipo'] == 'deposito' else "SAQUE"
                    sinal = "+" if transacao['tipo'] == 'deposito' else "-"
                    
                    # Formatar data
                    try:
                        data_str = transacao.get('created_at', '')
                        if data_str:
                            # Remover Z e converter
                            data_str = data_str.replace('Z', '+00:00')
                            data = datetime.fromisoformat(data_str)
                            data_formatada = data.strftime('%d/%m/%Y %H:%M:%S')
                        else:
                            data_formatada = "N/A"
                    except:
                        data_formatada = transacao.get('created_at', 'N/A')
                    
                    print(f"\n{i}. {data_formatada}")
                    print(f"   {sinal} R$ {transacao['valor']:.2f} - {tipo}")
                    if transacao.get('descricao'):
                        print(f"   Descricao: {transacao['descricao']}")
                    print(f"   ID: {transacao['id']}")
            
            return extrato
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
    print("TESTE: Ver Extrato da Conta")
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
    
    # Listar contas
    print("\n" + "-" * 60)
    print("Listando suas contas...")
    print("-" * 60)
    contas = listar_contas(token)
    
    if not contas:
        print("\nVoce nao possui contas cadastradas.")
        print("Crie uma conta primeiro usando: python teste_criar_conta.py")
        sys.exit(1)
    
    print("\nSuas contas:")
    for conta in contas:
        print(f"  ID {conta['id']}: {conta['numero']} - {conta['titular']} (Saldo: R$ {conta['saldo']:.2f})")
    
    # Escolher conta
    print("\n" + "-" * 60)
    conta_id_str = input("Digite o ID da conta: ").strip()
    
    try:
        conta_id = int(conta_id_str)
    except ValueError:
        print("ERRO: ID deve ser um numero inteiro!")
        sys.exit(1)
    
    # Verificar se a conta existe
    conta_existe = any(c['id'] == conta_id for c in contas)
    if not conta_existe:
        print(f"AVISO: Conta ID {conta_id} nao encontrada na sua lista de contas.")
        resposta = input("Deseja continuar mesmo assim? (s/n): ").strip().lower()
        if resposta != 's':
            sys.exit(0)
    
    # Ver extrato
    extrato = ver_extrato(token, conta_id)
    
    if extrato:
        print("\n" + "=" * 60)
        print("PRONTO!")
        print("=" * 60)
        print("\nAgora voce pode:")
        print(f"  - Criar transacoes: POST /api/v1/transacoes?conta_id={conta_id}")
        print(f"  - Ver detalhes da conta: GET /api/v1/contas/{conta_id}")
        print("\nOu acesse a documentacao em: http://localhost:8000/docs")

