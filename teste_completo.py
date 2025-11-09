"""
Script para testar todas as funcionalidades da API em sequência
"""
import requests
import json
import time
import sys

API_URL = "http://localhost:8000"

# Cores para output (simplificado para Windows)
class Colors:
    OK = ""
    ERROR = ""
    INFO = ""
    RESET = ""

def print_success(msg):
    print(f"[OK] {msg}")

def print_error(msg):
    print(f"[ERRO] {msg}")

def print_info(msg):
    print(f"[INFO] {msg}")

def teste_criar_usuario():
    """Teste 1: Criar usuário"""
    print("\n" + "=" * 60)
    print("TESTE 1: CRIAR USUARIO")
    print("=" * 60)
    
    timestamp = str(int(time.time()))
    username = f"teste_{timestamp}"
    email = f"teste_{timestamp}@example.com"
    password = "senha123"
    
    data = {"username": username, "email": email, "password": password}
    
    try:
        response = requests.post(f"{API_URL}/api/v1/auth/register", json=data, timeout=5)
        if response.status_code == 201:
            usuario = response.json()
            print_success(f"Usuario criado: {usuario['username']} (ID: {usuario['id']})")
            return {"username": username, "password": password, "user_id": usuario['id']}
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_fazer_login(credenciais):
    """Teste 2: Fazer login"""
    print("\n" + "=" * 60)
    print("TESTE 2: FAZER LOGIN")
    print("=" * 60)
    
    data = {"username": credenciais["username"], "password": credenciais["password"]}
    
    try:
        response = requests.post(f"{API_URL}/api/v1/auth/login", json=data, timeout=5)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            print_success(f"Login realizado! Token obtido (primeiros 30 chars: {token[:30]}...)")
            return token
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_obter_usuario(token):
    """Teste 3: Obter informações do usuário"""
    print("\n" + "=" * 60)
    print("TESTE 3: OBTER USUARIO")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_URL}/api/v1/auth/me", headers=headers, timeout=5)
        if response.status_code == 200:
            usuario = response.json()
            print_success(f"Usuario obtido: {usuario['username']} ({usuario['email']})")
            return usuario
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_criar_conta(token):
    """Teste 4: Criar conta"""
    print("\n" + "=" * 60)
    print("TESTE 4: CRIAR CONTA")
    print("=" * 60)
    
    timestamp = str(int(time.time()))
    numero = f"{timestamp[-6:]}-{timestamp[-1]}"
    data = {"numero": numero, "titular": "Titular Teste"}
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{API_URL}/api/v1/contas", json=data, headers=headers, timeout=5)
        if response.status_code == 201:
            conta = response.json()
            print_success(f"Conta criada: {conta['numero']} - Saldo: R$ {conta['saldo']:.2f}")
            return conta['id']
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_listar_contas(token):
    """Teste 5: Listar contas"""
    print("\n" + "=" * 60)
    print("TESTE 5: LISTAR CONTAS")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_URL}/api/v1/contas", headers=headers, timeout=5)
        if response.status_code == 200:
            contas = response.json()
            print_success(f"Contas listadas: {len(contas)} conta(s) encontrada(s)")
            for conta in contas:
                print(f"  - Conta {conta['id']}: {conta['numero']} - Saldo: R$ {conta['saldo']:.2f}")
            return contas[0]['id'] if contas else None
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_obter_conta(token, conta_id):
    """Teste 6: Obter conta específica"""
    print("\n" + "=" * 60)
    print("TESTE 6: OBTER CONTA ESPECIFICA")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_URL}/api/v1/contas/{conta_id}", headers=headers, timeout=5)
        if response.status_code == 200:
            conta = response.json()
            print_success(f"Conta obtida: {conta['numero']} - Titular: {conta['titular']} - Saldo: R$ {conta['saldo']:.2f}")
            return conta
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_criar_deposito(token, conta_id):
    """Teste 7: Criar depósito"""
    print("\n" + "=" * 60)
    print("TESTE 7: CRIAR DEPOSITO")
    print("=" * 60)
    
    data = {"tipo": "deposito", "valor": 1000.00, "descricao": "Deposito de teste"}
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/transacoes?conta_id={conta_id}",
            json=data,
            headers=headers,
            timeout=5
        )
        if response.status_code == 201:
            transacao = response.json()
            print_success(f"Deposito criado: R$ {transacao['valor']:.2f} - ID: {transacao['id']}")
            return transacao
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_criar_saque(token, conta_id):
    """Teste 8: Criar saque"""
    print("\n" + "=" * 60)
    print("TESTE 8: CRIAR SAQUE")
    print("=" * 60)
    
    data = {"tipo": "saque", "valor": 100.00, "descricao": "Saque de teste"}
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/transacoes?conta_id={conta_id}",
            json=data,
            headers=headers,
            timeout=5
        )
        if response.status_code == 201:
            transacao = response.json()
            print_success(f"Saque criado: R$ {transacao['valor']:.2f} - ID: {transacao['id']}")
            return transacao
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def teste_ver_extrato(token, conta_id):
    """Teste 9: Ver extrato"""
    print("\n" + "=" * 60)
    print("TESTE 9: VER EXTRATO")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_URL}/api/v1/transacoes/extrato/{conta_id}", headers=headers, timeout=5)
        if response.status_code == 200:
            extrato = response.json()
            print_success(f"Extrato obtido: {extrato['total_transacoes']} transacao(oes) - Saldo: R$ {extrato['saldo_atual']:.2f}")
            print(f"\nTransacoes:")
            for i, trans in enumerate(extrato['transacoes'], 1):
                tipo = "DEPOSITO" if trans['tipo'] == 'deposito' else "SAQUE"
                sinal = "+" if trans['tipo'] == 'deposito' else "-"
                print(f"  {i}. {sinal} R$ {trans['valor']:.2f} - {tipo} - {trans.get('descricao', 'Sem descricao')}")
            return extrato
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Excecao: {e}")
        return None

def main():
    print("=" * 60)
    print("TESTE COMPLETO DA API BANCARIA")
    print("=" * 60)
    print("\nVerificando se a API esta rodando...")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print_error("API nao esta respondendo corretamente!")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print_error("API nao esta rodando! Execute: python run.py")
        sys.exit(1)
    
    print_success("API esta rodando!")
    
    # Executar testes em sequência
    resultados = {}
    
    # Teste 1: Criar usuário
    credenciais = teste_criar_usuario()
    if not credenciais:
        print_error("Falha ao criar usuario. Abortando testes.")
        sys.exit(1)
    resultados['credenciais'] = credenciais
    
    # Teste 2: Fazer login
    token = teste_fazer_login(credenciais)
    if not token:
        print_error("Falha ao fazer login. Abortando testes.")
        sys.exit(1)
    resultados['token'] = token
    
    # Teste 3: Obter usuário
    usuario = teste_obter_usuario(token)
    if not usuario:
        print_error("Falha ao obter usuario.")
    resultados['usuario'] = usuario
    
    # Teste 4: Criar conta
    conta_id = teste_criar_conta(token)
    if not conta_id:
        print_error("Falha ao criar conta. Abortando testes de contas.")
        sys.exit(1)
    resultados['conta_id'] = conta_id
    
    # Teste 5: Listar contas
    conta_id_lista = teste_listar_contas(token)
    if not conta_id_lista:
        print_error("Falha ao listar contas.")
    
    # Teste 6: Obter conta
    conta = teste_obter_conta(token, conta_id)
    if not conta:
        print_error("Falha ao obter conta.")
    
    # Teste 7: Criar depósito
    deposito = teste_criar_deposito(token, conta_id)
    if not deposito:
        print_error("Falha ao criar deposito.")
    
    # Teste 8: Criar saque
    saque = teste_criar_saque(token, conta_id)
    if not saque:
        print_error("Falha ao criar saque.")
    
    # Teste 9: Ver extrato
    extrato = teste_ver_extrato(token, conta_id)
    if not extrato:
        print_error("Falha ao ver extrato.")
    
    # Resumo final
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"\nUsuario criado: {credenciais['username']}")
    print(f"Token obtido: Sim")
    print(f"Conta criada: ID {conta_id}")
    print(f"Deposito criado: {'Sim' if deposito else 'Nao'}")
    print(f"Saque criado: {'Sim' if saque else 'Nao'}")
    print(f"Extrato obtido: {'Sim' if extrato else 'Nao'}")
    
    if extrato:
        print(f"\nSaldo final: R$ {extrato['saldo_atual']:.2f}")
        print(f"Total de transacoes: {extrato['total_transacoes']}")
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUIDOS!")
    print("=" * 60)

if __name__ == "__main__":
    main()

