# 📘 Tutorial: Fazer Login

## 📋 Visão Geral

Este tutorial mostra como fazer login na API Bancária e obter um token JWT. O token JWT é necessário para acessar endpoints protegidos da API.

## ⚠️ Pré-requisitos

1. ✅ Ter um usuário criado na API
2. ✅ Conhecer o username e password do usuário
3. ✅ API rodando (http://localhost:8000)

## 🚀 Método 1: Interface Web (Swagger UI) - Mais Fácil

### Passo a Passo

1. **Acesse a documentação**: http://localhost:8000/docs

2. **Encontre o endpoint**: `POST /api/v1/auth/login`

3. **Clique em "Try it out"**

4. **Preencha os dados**:
   ```json
   {
     "username": "seu_username",
     "password": "sua_senha"
   }
   ```

5. **Clique em "Execute"**

6. **Copie o token** retornado na resposta!

### Resposta Esperada

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 🐍 Método 2: Script Python

Execute o script de teste:

```bash
python teste_fazer_login.py
```

O script irá solicitar suas credenciais e retornar o token.

---

## 💻 Método 3: Requisição HTTP Direta

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"seu_username\", \"password\": \"sua_senha\"}"
```

### PowerShell

```powershell
$body = @{
    username = "seu_username"
    password = "sua_senha"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/auth/login"
data = {
    "username": "seu_username",
    "password": "sua_senha"
}

response = requests.post(url, json=data)
token_data = response.json()
print(f"Token: {token_data['access_token']}")
```

---

## 📝 Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `username` | string | Sim | Nome de usuário | `"joao_silva"` |
| `password` | string | Sim | Senha do usuário | `"senha123"` |

---

## ✅ Validações

- ✅ **Username existe**: O username deve existir no sistema
- ✅ **Password correto**: A senha deve corresponder à senha cadastrada
- ✅ **Credenciais válidas**: Ambos os campos são obrigatórios

---

## ❌ Erros Comuns

### Erro 401 - Unauthorized
```json
{
  "detail": "Username ou senha incorretos"
}
```
**Solução**: Verifique se o username e senha estão corretos

### Erro 422 - Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required"
    }
  ]
}
```
**Solução**: Certifique-se de enviar ambos os campos (username e password)

### Erro de Conexão
**Solução**: Verifique se a API está rodando:
```bash
python run.py
```

---

## 🎯 Como Usar o Token

### No Swagger UI
1. Clique no botão **"Authorize"** (cadeado) no topo da página
2. Cole o token (sem a palavra "Bearer")
3. Clique em **"Authorize"**
4. Todas as requisições usarão o token automaticamente!

### Em requisições HTTP
```
Authorization: Bearer <seu_token>
```

### Exemplo com Python
```python
headers = {
    "Authorization": f"Bearer {token}"
}
response = requests.get("http://localhost:8000/api/v1/contas", headers=headers)
```

### Exemplo com cURL
```bash
curl -X GET "http://localhost:8000/api/v1/contas" ^
  -H "Authorization: Bearer <seu_token>"
```

---

## 📊 Estrutura da Resposta

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  // Token JWT
  "token_type": "bearer"                                       // Tipo do token
}
```

---

## ⏰ Validade do Token

O token JWT expira após **30 minutos** (configurável em `app/config.py`).

Se o token expirar, você receberá um erro 401. Nesse caso, faça login novamente para obter um novo token.

---

## 🔄 Próximos Passos

Após fazer login e obter o token, você pode:

1. **Criar uma conta**: `POST /api/v1/contas` (com token)
2. **Listar contas**: `GET /api/v1/contas` (com token)
3. **Fazer transações**: `POST /api/v1/transacoes` (com token)
4. **Ver extrato**: `GET /api/v1/transacoes/extrato/{conta_id}` (com token)
5. **Obter informações do usuário**: `GET /api/v1/auth/me` (com token)

---

## 🔑 Endpoints que Requerem Autenticação

- ✅ `POST /api/v1/contas` - Criar conta
- ✅ `GET /api/v1/contas` - Listar contas
- ✅ `GET /api/v1/contas/{conta_id}` - Obter conta
- ✅ `POST /api/v1/transacoes` - Criar transação
- ✅ `GET /api/v1/transacoes/extrato/{conta_id}` - Obter extrato
- ✅ `GET /api/v1/auth/me` - Obter informações do usuário

---

## 📚 Veja Também

- [Tutorial: Criar Usuário](TUTORIAL_CRIAR_USUARIO.md)
- [Tutorial: Obter Usuário](TUTORIAL_OBTER_USUARIO.md)
- [Guia Rápido](GUIA_RAPIDO.md)
- [Guia Completo da API](README.md)

