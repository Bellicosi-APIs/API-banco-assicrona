# 📘 Tutorial: Criar Conta Corrente

## 📋 Visão Geral

Este tutorial mostra como criar uma conta corrente na API Bancária. Uma conta corrente é necessária para realizar transações (depósitos e saques).

## ⚠️ Pré-requisitos

1. ✅ Ter um usuário criado na API
2. ✅ Ter feito login e obtido um token JWT
3. ✅ API rodando (http://localhost:8000)

## 🚀 Método 1: Interface Web (Swagger UI) - Mais Fácil

### Passo a Passo

1. **Acesse a documentação**: http://localhost:8000/docs

2. **Autorize com seu token**:
   - Clique no botão **"Authorize"** (cadeado) no topo da página
   - Cole seu token JWT (sem a palavra "Bearer")
   - Clique em **"Authorize"**

3. **Encontre o endpoint**: `POST /api/v1/contas`

4. **Clique em "Try it out"**

5. **Preencha os dados**:
   ```json
   {
     "numero": "12345-6",
     "titular": "João Silva"
   }
   ```

6. **Clique em "Execute"**

7. **Veja a resposta** com os dados da conta criada!

### Resposta Esperada

```json
{
  "id": 1,
  "numero": "12345-6",
  "titular": "João Silva",
  "saldo": 0.0,
  "created_at": "2025-11-09T00:30:00.000Z",
  "usuario_id": 1
}
```

---

## 🐍 Método 2: Script Python

Execute o script de teste:

```bash
python teste_criar_conta.py
```

O script irá:
1. Fazer login automaticamente
2. Criar uma conta
3. Mostrar os detalhes da conta criada

---

## 💻 Método 3: Requisição HTTP Direta

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/contas" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI" ^
  -H "Content-Type: application/json" ^
  -d "{\"numero\": \"12345-6\", \"titular\": \"João Silva\"}"
```

### PowerShell

```powershell
$headers = @{
    "Authorization" = "Bearer SEU_TOKEN_AQUI"
    "Content-Type" = "application/json"
}

$body = @{
    numero = "12345-6"
    titular = "João Silva"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/contas" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/contas"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI",
    "Content-Type": "application/json"
}
data = {
    "numero": "12345-6",
    "titular": "João Silva"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

---

## 📝 Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `numero` | string | Sim | Número da conta corrente (único) | "12345-6" |
| `titular` | string | Sim | Nome do titular da conta | "João Silva" |

---

## ✅ Validações

- ✅ **Número único**: O número da conta deve ser único no sistema
- ✅ **Autenticação**: Requer token JWT válido
- ✅ **Saldo inicial**: Sempre inicia com saldo 0.0

---

## ❌ Erros Comuns

### Erro 401 - Unauthorized
```json
{
  "detail": "Not authenticated"
}
```
**Solução**: Verifique se você passou o token JWT no header `Authorization`

### Erro 400 - Bad Request
```json
{
  "detail": "Número de conta já está em uso"
}
```
**Solução**: Escolha outro número de conta

### Erro 422 - Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "numero"],
      "msg": "field required"
    }
  ]
}
```
**Solução**: Certifique-se de enviar todos os campos obrigatórios

---

## 🎯 Exemplos de Uso

### Exemplo 1: Criar conta básica

```json
POST /api/v1/contas
Authorization: Bearer <token>

{
  "numero": "0001-1",
  "titular": "Maria Santos"
}
```

### Exemplo 2: Criar múltiplas contas

Você pode criar quantas contas quiser (desde que os números sejam únicos):

```json
{
  "numero": "0002-2",
  "titular": "Pedro Oliveira"
}
```

---

## 📊 Estrutura da Resposta

```json
{
  "id": 1,                    // ID único da conta
  "numero": "12345-6",        // Número da conta
  "titular": "João Silva",    // Nome do titular
  "saldo": 0.0,               // Saldo inicial (sempre 0.0)
  "created_at": "2025-11-09T00:30:00.000Z",  // Data de criação
  "usuario_id": 1             // ID do usuário dono da conta
}
```

---

## 🔄 Próximos Passos

Após criar uma conta, você pode:

1. **Fazer um depósito**: `POST /api/v1/transacoes?conta_id=1`
2. **Fazer um saque**: `POST /api/v1/transacoes?conta_id=1`
3. **Ver o extrato**: `GET /api/v1/transacoes/extrato/1`
4. **Listar suas contas**: `GET /api/v1/contas`

---

## 📚 Veja Também

- [Tutorial: Listar Contas](TUTORIAL_LISTAR_CONTAS.md)
- [Tutorial: Criar Transação](TUTORIAL_CRIAR_TRANSACAO.md)
- [Tutorial: Ver Extrato](TUTORIAL_VER_EXTRATO.md)
- [Guia Completo da API](README.md)

