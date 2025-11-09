# 📙 Tutorial: Obter Conta Específica

## 📋 Visão Geral

Este tutorial mostra como obter os detalhes de uma conta corrente específica pelo seu ID.

## ⚠️ Pré-requisitos

1. ✅ Ter um usuário criado na API
2. ✅ Ter feito login e obtido um token JWT
3. ✅ Ter pelo menos uma conta criada
4. ✅ Conhecer o ID da conta (pode obter listando as contas)
5. ✅ API rodando (http://localhost:8000)

## 🚀 Método 1: Interface Web (Swagger UI) - Mais Fácil

### Passo a Passo

1. **Acesse a documentação**: http://localhost:8000/docs

2. **Autorize com seu token**:
   - Clique no botão **"Authorize"** (cadeado) no topo da página
   - Cole seu token JWT (sem a palavra "Bearer")
   - Clique em **"Authorize"**

3. **Encontre o endpoint**: `GET /api/v1/contas/{conta_id}`

4. **Clique em "Try it out"**

5. **Informe o ID da conta**:
   - No campo `conta_id`, digite o ID da conta (ex: `1`)

6. **Clique em "Execute"**

7. **Veja os detalhes da conta**!

### Resposta Esperada

```json
{
  "id": 1,
  "numero": "12345-6",
  "titular": "João Silva",
  "saldo": 1000.50,
  "created_at": "2025-11-09T00:30:00.000Z",
  "updated_at": null,
  "usuario_id": 1
}
```

---

## 🐍 Método 2: Script Python

Execute o script de teste:

```bash
python teste_obter_conta.py
```

O script irá:
1. Fazer login automaticamente
2. Listar suas contas
3. Permitir escolher uma conta
4. Mostrar os detalhes da conta escolhida

---

## 💻 Método 3: Requisição HTTP Direta

### cURL

```bash
curl -X GET "http://localhost:8000/api/v1/contas/1" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### PowerShell

```powershell
$headers = @{
    "Authorization" = "Bearer SEU_TOKEN_AQUI"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/contas/1" `
    -Method GET `
    -Headers $headers
```

### Python (requests)

```python
import requests

conta_id = 1
url = f"http://localhost:8000/api/v1/contas/{conta_id}"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI"
}

response = requests.get(url, headers=headers)
conta = response.json()
print(f"Conta {conta['numero']}: {conta['titular']} - Saldo: R$ {conta['saldo']:.2f}")
```

---

## 📝 Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `conta_id` | integer | Sim | ID da conta (path parameter) | `1` |

---

## ✅ Características

- ✅ **Segurança**: Só retorna contas do usuário autenticado
- ✅ **Autenticação**: Requer token JWT válido
- ✅ **Detalhes completos**: Retorna todas as informações da conta

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

### Exemplo 1: Obter conta por ID

```bash
GET /api/v1/contas/1
Authorization: Bearer <token>
```

**Resposta:**
```json
{
  "id": 1,
  "numero": "12345-6",
  "titular": "João Silva",
  "saldo": 1000.50,
  "created_at": "2025-11-09T00:30:00.000Z",
  "usuario_id": 1
}
```

### Exemplo 2: Obter conta e processar dados (Python)

```python
import requests

def obter_conta(token: str, conta_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"http://localhost:8000/api/v1/contas/{conta_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        conta = response.json()
        print(f"Conta: {conta['numero']}")
        print(f"Titular: {conta['titular']}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        return conta
    else:
        print(f"Erro: {response.status_code}")
        return None
```

---

## 📊 Estrutura da Resposta

```json
{
  "id": 1,                    // ID único da conta
  "numero": "12345-6",        // Número da conta
  "titular": "João Silva",    // Nome do titular
  "saldo": 1000.50,           // Saldo atual da conta
  "created_at": "2025-11-09T00:30:00.000Z",  // Data de criação
  "updated_at": null,         // Data da última atualização (null se nunca atualizado)
  "usuario_id": 1             // ID do usuário dono da conta
}
```

---

## 🔄 Diferença entre Listar e Obter

| Operação | Endpoint | Retorna |
|----------|----------|---------|
| **Listar** | `GET /api/v1/contas` | Array com todas as contas (resumo) |
| **Obter** | `GET /api/v1/contas/{id}` | Objeto com detalhes completos de uma conta |

---

## 🔄 Próximos Passos

Após obter os detalhes de uma conta, você pode:

1. **Fazer uma transação**: `POST /api/v1/transacoes?conta_id={conta_id}`
2. **Ver extrato da conta**: `GET /api/v1/transacoes/extrato/{conta_id}`
3. **Listar todas as contas**: `GET /api/v1/contas`

---

## 📚 Veja Também

- [Tutorial: Criar Conta](TUTORIAL_CRIAR_CONTA.md)
- [Tutorial: Listar Contas](TUTORIAL_LISTAR_CONTAS.md)
- [Tutorial: Criar Transação](TUTORIAL_CRIAR_TRANSACAO.md)
- [Guia Completo da API](README.md)

