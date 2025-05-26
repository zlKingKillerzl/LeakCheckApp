# LeakCheck API Interface

Uma aplicação web com backend em Flask que funciona como proxy seguro para a API LeakCheck. Sua chave fica protegida, enquanto você consulta vazamentos de dados em uma interface bonita e intuitiva.

---

## 🔑 Como Obter Sua Chave da API LeakCheck

1. Acesse: [https://leakcheck.io/](https://leakcheck.io/)
2. Crie uma conta (gratuita ou premium).
3. Vá em: [https://leakcheck.io/account](https://leakcheck.io/account)
4. Copie sua chave da API.

---

## 🔐 Como Configurar Sua Chave

A chave é configurada via **variável de ambiente** usando um arquivo `.env` (✅ mais seguro e obrigatório):

1. Crie um arquivo `.env` na raiz do projeto:

```
LEAKCHECK_API_KEY=SUA_CHAVE_AQUI
```

2. O backend carrega automaticamente esse arquivo com:

```python
from dotenv import load_dotenv
load_dotenv()
```

⚠️ Se a chave não estiver configurada, o servidor não irá rodar.

---

## 🖥️ Funcionalidades

- 🔐 API Key segura (nunca vai para o frontend)
- 🚫 Limitação de requisições:
  - 10 por minuto (global)
  - 5 por minuto por endpoint
- 🔍 Pesquisa por:
  - Email, nome de usuário, telefone, domínio, hash, IP, etc.
- 🎨 Interface moderna (tema escuro com roxo e azul)
- 📑 Tabela de resultados limpa
- 📋 Copiar dados (formatado ou JSON bruto)
- 📤 Exportar resultados (PDF, JSON, TXT)
- 🔥 Tratamento robusto de erros:
  - Falha de conexão
  - API fora do ar
  - Timeout
  - API Key ausente
  - Query inválida

---

## 📂 Estrutura do Projeto

```
LeakCheckApp/
├── app.py                # Backend Flask (proxy da API + servidor web)
├── index.html             # Frontend (interface web)
├── requirements.txt       # Dependências Python
├── Dockerfile             # Docker (opcional)
├── docker-compose.yml     # Docker Compose (opcional)
└── README.md              # Documentação
```

---

## 🚀 Instalação e Execução

### ✅ Pré-requisitos

- Python 3.8+
- pip
- (Opcional) Docker e Docker Compose

### 🔧 Executando Localmente

```bash
cd LeakCheckApp

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\ctivate

pip install -r requirements.txt

# Crie o arquivo .env com:
# LEAKCHECK_API_KEY=SUA_CHAVE_AQUI

python app.py
```

Acesse em:

```
http://127.0.0.1:5000
```

---

### 🐳 Executando com Docker

**Com Docker Compose:**

1. No arquivo `docker-compose.yml`:

```yaml
environment:
  - LEAKCHECK_API_KEY=SUA_CHAVE_AQUI
```

2. Rode:

```bash
docker-compose up --build
```

**Docker manual:**

```bash
docker build -t leakcheckapp .
docker run -p 5000:5000 -e LEAKCHECK_API_KEY=SUA_CHAVE_AQUI leakcheckapp
```

---

## 🌐 Usando a Interface Web

1. Acesse `http://localhost:5000`
2. Insira um dado (email, nome de usuário, domínio, etc.)
3. Selecione o tipo ou deixe em "automático"
4. Clique em **Pesquisar**
5. Veja dados, fonte e data do vazamento
6. Copie ou exporte os resultados (PDF, JSON, TXT)
7. Clique em **Limpar Resultados** para nova busca

---

## 🔗 Usando a API REST

**URL Base:**

```
http://localhost:5000/api/v2/query/
```

**Exemplos:**

```bash
curl "http://localhost:5000/api/v2/query/example@example.com"
curl "http://localhost:5000/api/v2/query/example.com?type=domain"
```

**Resposta de exemplo:**

```json
{
  "query": "example@example.com",
  "type": "email",
  "success": true,
  "result": [
    {
      "source": {
        "name": "ExampleLeak",
        "breach_date": "2023-01-01"
      },
      "email": "example@example.com",
      "password": "hashedpassword"
    }
  ]
}
```

---

## ⚠️ Observações

- A chave da API é **obrigatória**.
- A chave fica **100% protegida** no backend.
- ✅ O backend possui limite de requisições e tratamento de erros.
- 🚫 Nenhum dado é armazenado localmente.

---

## 📜 Licença

MIT License