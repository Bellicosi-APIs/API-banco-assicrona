# 📘 Tutorial: Criar Usuário

## 📋 Visão Geral

Este tutorial mostra como criar um novo usuário na API Bancária. Um usuário é necessário para fazer login e acessar as funcionalidades da API.

## ⚠️ Pré-requisitos

1. ✅ API rodando (http://localhost:8000)

## 🚀 Método 1: Interface Web (Swagger UI) - Mais Fácil

### Passo a Passo

1. **Acesse a documentação**: http://localhost:8000/docs

2. **Encontre o endpoint**: `POST /api/v1/auth/register`

3. **Clique em "Try it out"**

4. **Preencha os dados**:
   ```json
   {
     "username": "joao_silva",
     "email": "joao@example.com",
     "password": "senha123"
   }
   ```

5. **Clique em "Execute"**

6. **Veja a resposta** com os dados do usuário criado!

### Resposta Esperada

```json
{
  "id": 1,
  "username": "joao_silva",
  "email": "joao@example.com"
}
```

---

## 🐍 Método 2: Script Python

Execute o script de teste:

```bash
python teste_criar_usuario.py
```

O script irá criar um usuário automaticamente com dados únicos.

---

## 💻 Método 3: Requisição HTTP Direta

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"joao_silva\", \"email\": \"joao@example.com\", \"password\": \"senha123\"}"
```

### PowerShell

```powershell
$body = @{
    username = "joao_silva"
    email = "joao@example.com"
    password = "senha123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/auth/register"
data = {
    "username": "joao_silva",
    "email": "joao@example.com",
    "password": "senha123"
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 📝 Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `username` | string | Sim | Nome de usuário único (mínimo 3 caracteres) | `"joao_silva"` |
| `email` | string | Sim | Email único do usuário (deve ser válido) | `"joao@example.com"` |
| `password` | string | Sim | Senha (mínimo 6 caracteres) | `"senha123"` |

---

## ✅ Validações

- ✅ **Username único**: O username deve ser único no sistema
- ✅ **Email único**: O email deve ser único no sistema
- ✅ **Username mínimo**: Mínimo de 3 caracteres
- ✅ **Password mínimo**: Mínimo de 6 caracteres
- ✅ **Email válido**: Deve ser um email válido

---

## ❌ Erros Comuns

### Erro 400 - Bad Request - Username em uso
```json
{
  "detail": "Username já está em uso"
}
```
**Solução**: Escolha outro username

### Erro 400 - Bad Request - Email em uso
```json
{
  "detail": "Email já está em uso"
}
```
**Solução**: Escolha outro email

### Erro 422 - Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "ensure this value has at least 3 characters"
    }
  ]
}
```
**Solução**: Verifique se todos os campos atendem aos requisitos mínimos

---

## 🎯 Exemplos de Uso

### Exemplo 1: Criar usuário básico

```json
POST /api/v1/auth/register
{
  "username": "joao_silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

### Exemplo 2: Criar usuário com dados diferentes

```json
POST /api/v1/auth/register
{
  "username": "maria_santos",
  "email": "maria@example.com",
  "password": "minhasenha456"
}
```

---

## 📊 Estrutura da Resposta

```json
{
  "id": 1,                    // ID único do usuário
  "username": "joao_silva",   // Nome de usuário
  "email": "joao@example.com" // Email do usuário
}
```

**Nota**: A senha não é retornada por questões de segurança.

---

## 🔄 Próximos Passos

Após criar um usuário, você pode:

1. **Fazer login**: `POST /api/v1/auth/login` para obter o token JWT
2. **Usar o token**: Acessar endpoints protegidos da API
3. **Criar contas**: `POST /api/v1/contas` (com token)
4. **Fazer transações**: `POST /api/v1/transacoes` (com token)

---

## 📚 Veja Também

- [Tutorial: Fazer Login](TUTORIAL_FAZER_LOGIN.md)
- [Tutorial: Obter Usuário](TUTORIAL_OBTER_USUARIO.md)
- [Guia Rápido](GUIA_RAPIDO.md)
- [Guia Completo da API](README.md)

