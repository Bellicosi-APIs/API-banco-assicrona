# 📗 Tutorial: Listar Contas

## 📋 Visão Geral

Este tutorial mostra como listar todas as contas correntes do usuário autenticado.

## ⚠️ Pré-requisitos

1. ✅ Ter um usuário criado na API
2. ✅ Ter feito login e obtido um token JWT
3. ✅ Ter pelo menos uma conta criada (opcional, mas recomendado)
4. ✅ API rodando (http://localhost:8000)

## 🚀 Método 1: Interface Web (Swagger UI) - Mais Fácil

### Passo a Passo

1. **Acesse a documentação**: http://localhost:8000/docs

2. **Autorize com seu token**:
   - Clique no botão **"Authorize"** (cadeado) no topo da página
   - Cole seu token JWT (sem a palavra "Bearer")
   - Clique em **"Authorize"**

3. **Encontre o endpoint**: `GET /api/v1/contas`

4. **Clique em "Try it out"**

5. **Clique em "Execute"**

6. **Veja a lista de contas**!

### Resposta Esperada

```json
[
  {
    "id": 1,
    "numero": "12345-6",
    "titular": "João Silva",
    "saldo": 1000.50,
    "created_at": "2025-11-09T00:30:00.000Z"
  },
  {
    "id": 2,
    "numero": "67890-1",
    "titular": "Maria Santos",
    "saldo": 500.00,
    "created_at": "2025-11-09T01:00:00.000Z"
  }
]
```

---

## 🐍 Método 2: Script Python

Execute o script de teste:

```bash
python teste_listar_contas.py
```

O script irá:
1. Fazer login automaticamente
2. Listar todas as contas do usuário
3. Mostrar os detalhes de cada conta

---

## 💻 Método 3: Requisição HTTP Direta

### cURL

```bash
curl -X GET "http://localhost:8000/api/v1/contas" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### PowerShell

```powershell
$headers = @{
    "Authorization" = "Bearer SEU_TOKEN_AQUI"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/contas" `
    -Method GET `
    -Headers $headers
```

### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/contas"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI"
}

response = requests.get(url, headers=headers)
contas = response.json()

for conta in contas:
    print(f"Conta {conta['numero']}: {conta['titular']} - Saldo: R$ {conta['saldo']:.2f}")
```

---

## 📝 Parâmetros

Este endpoint **não requer parâmetros**. Ele retorna automaticamente todas as contas do usuário autenticado.

---

## ✅ Características

- ✅ **Filtro automático**: Retorna apenas as contas do usuário autenticado
- ✅ **Autenticação**: Requer token JWT válido
- ✅ **Lista vazia**: Se você não tiver contas, retorna uma lista vazia `[]`

---

## ❌ Erros Comuns

### Erro 401 - Unauthorized
```json
{
  "detail": "Not authenticated"
}
```
**Solução**: Verifique se você passou o token JWT no header `Authorization`

### Lista Vazia
```json
[]
```
**Não é um erro!** Significa que você ainda não criou nenhuma conta. Crie uma conta primeiro usando `POST /api/v1/contas`

---

## 🎯 Exemplos de Uso

### Exemplo 1: Listar todas as contas

```bash
GET /api/v1/contas
Authorization: Bearer <token>
```

**Resposta:**
```json
[
  {
    "id": 1,
    "numero": "12345-6",
    "titular": "João Silva",
    "saldo": 1000.50,
    "created_at": "2025-11-09T00:30:00.000Z"
  }
]
```

### Exemplo 2: Processar lista de contas (Python)

```python
import requests

headers = {"Authorization": "Bearer SEU_TOKEN"}
response = requests.get("http://localhost:8000/api/v1/contas", headers=headers)
contas = response.json()

print(f"Total de contas: {len(contas)}")
for conta in contas:
    print(f"\nConta: {conta['numero']}")
    print(f"Titular: {conta['titular']}")
    print(f"Saldo: R$ {conta['saldo']:.2f}")
```

---

## 📊 Estrutura da Resposta

A resposta é um **array de objetos**, onde cada objeto representa uma conta:

```json
{
  "id": 1,                    // ID único da conta
  "numero": "12345-6",        // Número da conta
  "titular": "João Silva",    // Nome do titular
  "saldo": 1000.50,           // Saldo atual da conta
  "created_at": "2025-11-09T00:30:00.000Z"  // Data de criação
}
```

**Nota**: A resposta não inclui `usuario_id` por questões de segurança.

---

## 🔄 Próximos Passos

Após listar suas contas, você pode:

1. **Ver detalhes de uma conta específica**: `GET /api/v1/contas/{conta_id}`
2. **Fazer uma transação**: `POST /api/v1/transacoes?conta_id={conta_id}`
3. **Ver extrato de uma conta**: `GET /api/v1/transacoes/extrato/{conta_id}`

---

## 📚 Veja Também

- [Tutorial: Criar Conta](TUTORIAL_CRIAR_CONTA.md)
- [Tutorial: Obter Conta Específica](TUTORIAL_OBTER_CONTA.md)
- [Tutorial: Criar Transação](TUTORIAL_CRIAR_TRANSACAO.md)
- [Guia Completo da API](README.md)

