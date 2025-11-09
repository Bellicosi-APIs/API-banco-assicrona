# 📘 Tutorial: Obter Informações do Usuário

## 📋 Visão Geral

Este tutorial mostra como obter as informações do usuário autenticado usando o endpoint `/api/v1/auth/me`. Este endpoint retorna os dados do usuário baseado no token JWT fornecido.

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

3. **Encontre o endpoint**: `GET /api/v1/auth/me`

4. **Clique em "Try it out"**

5. **Clique em "Execute"**

6. **Veja as informações do usuário**!

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
python teste_obter_usuario.py
```

O script irá:
1. Fazer login automaticamente
2. Obter as informações do usuário
3. Mostrar os dados do usuário autenticado

---

## 💻 Método 3: Requisição HTTP Direta

### cURL

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### PowerShell

```powershell
$headers = @{
    "Authorization" = "Bearer SEU_TOKEN_AQUI"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/me" `
    -Method GET `
    -Headers $headers
```

### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/auth/me"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI"
}

response = requests.get(url, headers=headers)
usuario = response.json()
print(f"Usuário: {usuario['username']} - Email: {usuario['email']}")
```

---

## 📝 Parâmetros

Este endpoint **não requer parâmetros**. Ele usa o token JWT no header para identificar o usuário.

---

## ✅ Características

- ✅ **Autenticação obrigatória**: Requer token JWT válido
- ✅ **Identificação automática**: Identifica o usuário pelo token
- ✅ **Informações seguras**: Retorna apenas informações não sensíveis

---

## ❌ Erros Comuns

### Erro 401 - Unauthorized
```json
{
  "detail": "Not authenticated"
}
```
**Solução**: Verifique se você passou o token JWT no header `Authorization`

### Erro 401 - Token Inválido
```json
{
  "detail": "Could not validate credentials"
}
```
**Solução**: 
- Verifique se o token está correto
- Verifique se o token não expirou (tokens expiram após 30 minutos)
- Faça login novamente para obter um novo token

---

## 🎯 Exemplos de Uso

### Exemplo 1: Obter informações do usuário

```bash
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Resposta:**
```json
{
  "id": 1,
  "username": "joao_silva",
  "email": "joao@example.com"
}
```

### Exemplo 2: Processar informações do usuário (Python)

```python
import requests

def obter_usuario(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "http://localhost:8000/api/v1/auth/me",
        headers=headers
    )
    
    if response.status_code == 200:
        usuario = response.json()
        print(f"ID: {usuario['id']}")
        print(f"Username: {usuario['username']}")
        print(f"Email: {usuario['email']}")
        return usuario
    else:
        print(f"Erro: {response.status_code}")
        return None
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

## 💡 Como Funciona

1. O cliente envia uma requisição com o token JWT no header `Authorization`
2. A API valida o token JWT
3. A API extrai o username do token
4. A API busca o usuário no banco de dados
5. A API retorna as informações do usuário

---

## 🔄 Próximos Passos

Após obter as informações do usuário, você pode:

1. **Criar uma conta**: `POST /api/v1/contas` (com token)
2. **Listar contas**: `GET /api/v1/contas` (com token)
3. **Fazer transações**: `POST /api/v1/transacoes` (com token)

---

## 📚 Veja Também

- [Tutorial: Criar Usuário](TUTORIAL_CRIAR_USUARIO.md)
- [Tutorial: Fazer Login](TUTORIAL_FAZER_LOGIN.md)
- [Guia Rápido](GUIA_RAPIDO.md)
- [Guia Completo da API](README.md)

