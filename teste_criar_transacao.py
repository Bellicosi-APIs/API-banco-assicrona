"""
Script de teste para criar transações (depósito ou saque)

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
    """Obtém os detalhes de uma conta"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/api/v1/contas/{conta_id}", headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def criar_transacao(token: str, conta_id: int, tipo: str, valor: float, descricao: str = None):
    """
    Cria uma transação (depósito ou saque)
    
    Args:
        token: Token JWT
        conta_id: ID da conta
        tipo: "deposito" ou "saque"
        valor: Valor da transação
        descricao: Descrição opcional
    
    Returns:
        dict: Dados da transação criada ou None em caso de erro
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "tipo": tipo,
        "valor": valor
    }
    
    if descricao:
        data["descricao"] = descricao
    
    try:
        tipo_nome = "DEPOSITO" if tipo == "deposito" else "SAQUE"
        print(f"\nCriando {tipo_nome} de R$ {valor:.2f}...")
        
        response = requests.post(
            f"{API_URL}/api/v1/transacoes",
            params={"conta_id": conta_id},
            json=data,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 201:
            transacao = response.json()
            print("\n" + "=" * 60)
            print("SUCESSO! Transacao criada!")
            print("=" * 60)
            print(f"\nID: {transacao['id']}")
            print(f"Tipo: {transacao['tipo'].upper()}")
            print(f"Valor: R$ {transacao['valor']:.2f}")
            if transacao.get('descricao'):
                print(f"Descricao: {transacao['descricao']}")
            print(f"Data: {transacao.get('created_at', 'N/A')}")
            print(f"Conta ID: {transacao['conta_id']}")
            
            # Mostrar saldo atualizado
            conta = obter_conta(token, conta_id)
            if conta:
                print(f"\nSaldo atual da conta: R$ {conta['saldo']:.2f}")
            
            return transacao
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
    print("TESTE: Criar Transacao (Deposito ou Saque)")
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
    conta = obter_conta(token, conta_id)
    if not conta:
        print(f"ERRO: Conta ID {conta_id} nao encontrada!")
        sys.exit(1)
    
    print(f"\nConta selecionada: {conta['numero']} - {conta['titular']}")
    print(f"Saldo atual: R$ {conta['saldo']:.2f}")
    
    # Escolher tipo de transação
    print("\n" + "-" * 60)
    print("Tipo de transacao:")
    print("  1 - Deposito")
    print("  2 - Saque")
    tipo_opcao = input("Escolha (1 ou 2): ").strip()
    
    if tipo_opcao == "1":
        tipo = "deposito"
    elif tipo_opcao == "2":
        tipo = "saque"
    else:
        print("ERRO: Opcao invalida!")
        sys.exit(1)
    
    # Valor
    print("\n" + "-" * 60)
    valor_str = input("Digite o valor (ex: 100.50): ").strip()
    
    try:
        valor = float(valor_str)
        if valor <= 0:
            print("ERRO: O valor deve ser maior que zero!")
            sys.exit(1)
    except ValueError:
        print("ERRO: Valor invalido!")
        sys.exit(1)
    
    # Descrição
    descricao = input("Descricao (opcional, pressione Enter para pular): ").strip()
    if not descricao:
        descricao = None
    
    # Criar transação
    transacao = criar_transacao(token, conta_id, tipo, valor, descricao)
    
    if transacao:
        print("\n" + "=" * 60)
        print("PRONTO! Transacao criada com sucesso.")
        print("=" * 60)
        print("\nAgora voce pode:")
        print(f"  - Ver extrato: GET /api/v1/transacoes/extrato/{conta_id}")
        print("  - Criar mais transacoes: python teste_criar_transacao.py")
        print("\nOu acesse a documentacao em: http://localhost:8000/docs")

