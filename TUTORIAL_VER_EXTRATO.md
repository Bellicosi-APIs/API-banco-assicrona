# 📊 Tutorial: Ver Extrato da Conta

## 📋 Visão Geral

Este tutorial mostra como obter o extrato completo de uma conta corrente, incluindo todas as transações (depósitos e saques) realizadas.

## ⚠️ Pré-requisitos

1. ✅ Ter um usuário criado na API
2. ✅ Ter feito login e obtido um token JWT
3. ✅ Ter pelo menos uma conta criada
4. ✅ Conhecer o ID da conta
5. ✅ Ter realizado pelo menos uma transação (opcional, mas recomendado)
6. ✅ API rodando (http://localhost:8000)

## 🚀 Método 1: Interface Web (Swagger UI) - Mais Fácil

### Passo a Passo

1. **Acesse a documentação**: http://localhost:8000/docs

2. **Autorize com seu token**:
   - Clique no botão **"Authorize"** (cadeado) no topo da página
   - Cole seu token JWT (sem a palavra "Bearer")
   - Clique em **"Authorize"**

3. **Encontre o endpoint**: `GET /api/v1/transacoes/extrato/{conta_id}`

4. **Clique em "Try it out"**

5. **Informe o ID da conta**:
   - No campo `conta_id`, digite o ID da conta (ex: `1`)

6. **Clique em "Execute"**

7. **Veja o extrato completo** com todas as transações!

### Resposta Esperada

```json
{
  "conta_id": 1,
  "numero_conta": "12345-6",
  "titular": "João Silva",
  "saldo_atual": 900.00,
  "total_transacoes": 3,
  "transacoes": [
    {
      "id": 3,
      "tipo": "saque",
      "valor": 100.00,
      "descricao": "Saque para compras",
      "created_at": "2025-11-09T01:00:00.000Z",
      "conta_id": 1
    },
    {
      "id": 2,
      "tipo": "deposito",
      "valor": 500.00,
      "descricao": "Segundo depósito",
      "created_at": "2025-11-09T00:45:00.000Z",
      "conta_id": 1
    },
    {
      "id": 1,
      "tipo": "deposito",
      "valor": 1000.00,
      "descricao": "Depósito inicial",
      "created_at": "2025-11-09T00:30:00.000Z",
      "conta_id": 1
    }
  ]
}
```

---

## 🐍 Método 2: Script Python

Execute o script de teste:

```bash
python teste_ver_extrato.py
```

O script irá:
1. Fazer login automaticamente
2. Listar suas contas
3. Permitir escolher uma conta
4. Mostrar o extrato completo

---

## 💻 Método 3: Requisição HTTP Direta

### cURL

```bash
curl -X GET "http://localhost:8000/api/v1/transacoes/extrato/1" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### PowerShell

```powershell
$headers = @{
    "Authorization" = "Bearer SEU_TOKEN_AQUI"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/transacoes/extrato/1" `
    -Method GET `
    -Headers $headers
```

### Python (requests)

```python
import requests

conta_id = 1
url = f"http://localhost:8000/api/v1/transacoes/extrato/{conta_id}"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI"
}

response = requests.get(url, headers=headers)
extrato = response.json()

print(f"Conta: {extrato['numero_conta']}")
print(f"Titular: {extrato['titular']}")
print(f"Saldo Atual: R$ {extrato['saldo_atual']:.2f}")
print(f"Total de Transações: {extrato['total_transacoes']}")

print("\nTransações:")
for transacao in extrato['transacoes']:
    tipo = "DEPÓSITO" if transacao['tipo'] == 'deposito' else "SAQUE"
    sinal = "+" if transacao['tipo'] == 'deposito' else "-"
    print(f"{sinal} R$ {transacao['valor']:.2f} - {tipo} - {transacao.get('descricao', 'Sem descrição')}")
```

---

## 📝 Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `conta_id` | integer | Sim | ID da conta (path parameter) | `1` |

---

## ✅ Características

- ✅ **Ordenação**: Transações ordenadas por data (mais recentes primeiro)
- ✅ **Histórico completo**: Mostra todas as transações da conta
- ✅ **Informações da conta**: Inclui dados da conta e saldo atual
- ✅ **Segurança**: Só retorna extratos de contas do usuário autenticado
- ✅ **Autenticação**: Requer token JWT válido

---

## ❌ Erros Comuns

### Erro 401 - Unauthorized
```json
{
  "detail": "Not authenticated"
}
```
**Solução**: Verifique se você passou o token JWT no header `Authorization`

### Erro 404 - Not Found
```json
{
  "detail": "Conta não encontrada"
}
```
**Solução**: 
- Verifique se o ID da conta está correto
- Verifique se a conta pertence ao usuário autenticado
- Liste suas contas primeiro para ver os IDs disponíveis

### Erro 422 - Validation Error
```json
{
  "detail": [
    {
      "loc": ["path", "conta_id"],
      "msg": "value is not a valid integer"
    }
  ]
}
```
**Solução**: O `conta_id` deve ser um número inteiro válido

---

## 🎯 Exemplos de Uso

### Exemplo 1: Ver extrato básico

```bash
GET /api/v1/transacoes/extrato/1
Authorization: Bearer <token>
```

### Exemplo 2: Processar extrato (Python)

```python
import requests
from datetime import datetime

def ver_extrato(token: str, conta_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"http://localhost:8000/api/v1/transacoes/extrato/{conta_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        extrato = response.json()
        
        print("=" * 60)
        print("EXTRATO BANCÁRIO")
        print("=" * 60)
        print(f"\nConta: {extrato['numero_conta']}")
        print(f"Titular: {extrato['titular']}")
        print(f"Saldo Atual: R$ {extrato['saldo_atual']:.2f}")
        print(f"Total de Transações: {extrato['total_transacoes']}")
        
        print("\n" + "-" * 60)
        print("TRANSAÇÕES")
        print("-" * 60)
        
        if not extrato['transacoes']:
            print("\nNenhuma transação encontrada.")
        else:
            for transacao in extrato['transacoes']:
                tipo = "DEPÓSITO" if transacao['tipo'] == 'deposito' else "SAQUE"
                sinal = "+" if transacao['tipo'] == 'deposito' else "-"
                data = datetime.fromisoformat(transacao['created_at'].replace('Z', '+00:00'))
                
                print(f"\n{data.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"  {sinal} R$ {transacao['valor']:.2f} - {tipo}")
                if transacao.get('descricao'):
                    print(f"  Descrição: {transacao['descricao']}")
        
        return extrato
    else:
        print(f"Erro: {response.status_code}")
        return None
```

---

## 📊 Estrutura da Resposta

```json
{
  "conta_id": 1,                    // ID da conta
  "numero_conta": "12345-6",        // Número da conta
  "titular": "João Silva",          // Nome do titular
  "saldo_atual": 900.00,            // Saldo atual da conta
  "total_transacoes": 3,            // Total de transações
  "transacoes": [                   // Array de transações (ordenado por data, mais recentes primeiro)
    {
      "id": 3,
      "tipo": "saque",
      "valor": 100.00,
      "descricao": "Saque para compras",
      "created_at": "2025-11-09T01:00:00.000Z",
      "conta_id": 1
    }
  ]
}
```

---

## 💡 Informações Importantes

### Ordenação
- As transações são ordenadas por data/hora
- **Mais recentes primeiro** (ordem decrescente)
- Última transação aparece no topo da lista

### Lista Vazia
- Se a conta não tiver transações, `transacoes` será um array vazio `[]`
- `total_transacoes` será `0`
- O saldo atual será exibido normalmente

### Saldo Atual
- O saldo atual reflete todas as transações realizadas
- É calculado automaticamente pelo sistema
- Inclui depósitos e saques

---

## 🔄 Próximos Passos

Após ver o extrato, você pode:

1. **Criar uma nova transação**: `POST /api/v1/transacoes?conta_id={conta_id}`
2. **Ver os detalhes da conta**: `GET /api/v1/contas/{conta_id}`
3. **Listar todas as contas**: `GET /api/v1/contas`

---

## 📚 Veja Também

- [Tutorial: Criar Transação](TUTORIAL_CRIAR_TRANSACAO.md)
- [Tutorial: Criar Conta](TUTORIAL_CRIAR_CONTA.md)
- [Tutorial: Listar Contas](TUTORIAL_LISTAR_CONTAS.md)
- [Guia Completo da API](README.md)

