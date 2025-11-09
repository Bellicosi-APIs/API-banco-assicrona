# 💰 Tutorial: Criar Transação (Depósito ou Saque)

## 📋 Visão Geral

Este tutorial mostra como criar transações bancárias (depósitos e saques) em uma conta corrente.

## ⚠️ Pré-requisitos

1. ✅ Ter um usuário criado na API
2. ✅ Ter feito login e obtido um token JWT
3. ✅ Ter pelo menos uma conta criada
4. ✅ Conhecer o ID da conta
5. ✅ API rodando (http://localhost:8000)

## 🚀 Método 1: Interface Web (Swagger UI) - Mais Fácil

### Passo a Passo

1. **Acesse a documentação**: http://localhost:8000/docs

2. **Autorize com seu token**:
   - Clique no botão **"Authorize"** (cadeado) no topo da página
   - Cole seu token JWT (sem a palavra "Bearer")
   - Clique em **"Authorize"**

3. **Encontre o endpoint**: `POST /api/v1/transacoes`

4. **Clique em "Try it out"**

5. **Preencha os dados**:
   - **conta_id** (query parameter): ID da conta (ex: `1`)
   - **Body**:
     ```json
     {
       "tipo": "deposito",
       "valor": 1000.00,
       "descricao": "Depósito inicial"
     }
     ```

6. **Clique em "Execute"**

7. **Veja a resposta** com os dados da transação criada!

### Resposta Esperada

```json
{
  "id": 1,
  "tipo": "deposito",
  "valor": 1000.00,
  "descricao": "Depósito inicial",
  "created_at": "2025-11-09T00:30:00.000Z",
  "conta_id": 1
}
```

---

## 🐍 Método 2: Script Python

Execute o script de teste:

```bash
python teste_criar_transacao.py
```

O script irá:
1. Fazer login automaticamente
2. Listar suas contas
3. Permitir escolher uma conta
4. Permitir escolher o tipo de transação (depósito ou saque)
5. Criar a transação

---

## 💻 Método 3: Requisição HTTP Direta

### cURL - Depósito

```bash
curl -X POST "http://localhost:8000/api/v1/transacoes?conta_id=1" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI" ^
  -H "Content-Type: application/json" ^
  -d "{\"tipo\": \"deposito\", \"valor\": 1000.00, \"descricao\": \"Depósito inicial\"}"
```

### cURL - Saque

```bash
curl -X POST "http://localhost:8000/api/v1/transacoes?conta_id=1" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI" ^
  -H "Content-Type: application/json" ^
  -d "{\"tipo\": \"saque\", \"valor\": 100.00, \"descricao\": \"Saque para compras\"}"
```

### PowerShell - Depósito

```powershell
$headers = @{
    "Authorization" = "Bearer SEU_TOKEN_AQUI"
    "Content-Type" = "application/json"
}

$body = @{
    tipo = "deposito"
    valor = 1000.00
    descricao = "Depósito inicial"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/transacoes?conta_id=1" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/transacoes"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI",
    "Content-Type": "application/json"
}

# Depósito
data_deposito = {
    "tipo": "deposito",
    "valor": 1000.00,
    "descricao": "Depósito inicial"
}

response = requests.post(
    url,
    params={"conta_id": 1},
    json=data_deposito,
    headers=headers
)
print(response.json())

# Saque
data_saque = {
    "tipo": "saque",
    "valor": 100.00,
    "descricao": "Saque para compras"
}

response = requests.post(
    url,
    params={"conta_id": 1},
    json=data_saque,
    headers=headers
)
print(response.json())
```

---

## 📝 Parâmetros

### Query Parameters

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `conta_id` | integer | Sim | ID da conta corrente | `1` |

### Body Parameters

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `tipo` | string | Sim | Tipo de transação: `"deposito"` ou `"saque"` | `"deposito"` |
| `valor` | float | Sim | Valor da transação (deve ser maior que zero) | `1000.00` |
| `descricao` | string | Não | Descrição opcional da transação | `"Depósito inicial"` |

---

## ✅ Validações

- ✅ **Valor positivo**: O valor deve ser maior que zero
- ✅ **Saldo suficiente**: Para saques, o saldo da conta deve ser suficiente
- ✅ **Conta válida**: A conta deve existir e pertencer ao usuário autenticado
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

### Erro 400 - Bad Request - Saldo Insuficiente
```json
{
  "detail": "Saldo insuficiente. Saldo atual: R$ 50.00"
}
```
**Solução**: Verifique o saldo da conta antes de fazer o saque

### Erro 400 - Bad Request - Valor Inválido
```json
{
  "detail": "O valor da transação deve ser maior que zero"
}
```
**Solução**: O valor deve ser maior que zero

### Erro 404 - Not Found
```json
{
  "detail": "Conta não encontrada"
}
```
**Solução**: Verifique se o `conta_id` está correto e se a conta pertence ao usuário autenticado

### Erro 422 - Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "tipo"],
      "msg": "value is not a valid enumeration member"
    }
  ]
}
```
**Solução**: O tipo deve ser exatamente `"deposito"` ou `"saque"` (minúsculas)

---

## 🎯 Exemplos de Uso

### Exemplo 1: Fazer um Depósito

```json
POST /api/v1/transacoes?conta_id=1
Authorization: Bearer <token>

{
  "tipo": "deposito",
  "valor": 1000.00,
  "descricao": "Depósito inicial"
}
```

**Resposta:**
```json
{
  "id": 1,
  "tipo": "deposito",
  "valor": 1000.00,
  "descricao": "Depósito inicial",
  "created_at": "2025-11-09T00:30:00.000Z",
  "conta_id": 1
}
```

### Exemplo 2: Fazer um Saque

```json
POST /api/v1/transacoes?conta_id=1
Authorization: Bearer <token>

{
  "tipo": "saque",
  "valor": 100.00,
  "descricao": "Saque para compras"
}
```

**Resposta:**
```json
{
  "id": 2,
  "tipo": "saque",
  "valor": 100.00,
  "descricao": "Saque para compras",
  "created_at": "2025-11-09T00:35:00.000Z",
  "conta_id": 1
}
```

### Exemplo 3: Depósito sem Descrição

```json
POST /api/v1/transacoes?conta_id=1
Authorization: Bearer <token>

{
  "tipo": "deposito",
  "valor": 500.00
}
```

---

## 📊 Estrutura da Resposta

```json
{
  "id": 1,                    // ID único da transação
  "tipo": "deposito",         // Tipo: "deposito" ou "saque"
  "valor": 1000.00,           // Valor da transação
  "descricao": "Depósito inicial",  // Descrição (opcional)
  "created_at": "2025-11-09T00:30:00.000Z",  // Data/hora da transação
  "conta_id": 1               // ID da conta
}
```

---

## 💡 Como Funciona

### Depósito
- ✅ **Aumenta** o saldo da conta
- ✅ Sempre permitido (desde que o valor seja positivo)

### Saque
- ✅ **Diminui** o saldo da conta
- ✅ Só permitido se houver saldo suficiente
- ❌ Bloqueado se o saldo for insuficiente

---

## 🔄 Próximos Passos

Após criar uma transação, você pode:

1. **Ver o extrato da conta**: `GET /api/v1/transacoes/extrato/{conta_id}`
2. **Ver os detalhes da conta**: `GET /api/v1/contas/{conta_id}`
3. **Criar mais transações**: `POST /api/v1/transacoes?conta_id={conta_id}`

---

## 📚 Veja Também

- [Tutorial: Ver Extrato](TUTORIAL_VER_EXTRATO.md)
- [Tutorial: Criar Conta](TUTORIAL_CRIAR_CONTA.md)
- [Tutorial: Listar Contas](TUTORIAL_LISTAR_CONTAS.md)
- [Guia Completo da API](README.md)

