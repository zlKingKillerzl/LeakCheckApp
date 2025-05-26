
# LeakCheck API Interface

Uma aplicação web com backend em Flask que serve como um proxy seguro para consultas na API LeakCheck, protegendo sua chave de API e oferecendo uma interface amigável.

---

## 🔑 Como Obter Sua Chave da API LeakCheck

1. Acesse o site [https://leakcheck.io/](https://leakcheck.io/).
2. Crie uma conta gratuita ou premium (dependendo das suas necessidades).
3. Após login, acesse: [https://leakcheck.io/account](https://leakcheck.io/account).
4. Copie sua chave da API no painel.

---

## 🔐 Como Configurar Sua Chave no Projeto

### ✅ Opção 1 — Diretamente no Código (Simples)

Abra o arquivo `app.py` e localize:

```python
LEAKCHECK_API_KEY = "SUA_CHAVE_LEAKCHECK_AQUI"
```

Substitua `"SUA_CHAVE_LEAKCHECK_AQUI"` pela sua chave real da API LeakCheck.

### ✅ Opção 2 — Usando Variável de Ambiente (Recomendado)

No arquivo `app.py`, altere:

```python
LEAKCHECK_API_KEY = os.getenv("LEAKCHECK_API_KEY")
```

Depois, crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
LEAKCHECK_API_KEY=SUA_CHAVE_AQUI
```

E adicione no topo do `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

Instale o pacote se necessário:

```bash
pip install python-dotenv
```

---

## 🖥️ Funcionalidades

- 🔍 **Consulta à API LeakCheck:** Pesquise por e-mail, domínio, nome de usuário, telefone, IP, hash, etc.
- 🖥️ **Interface Moderna:** Tema escuro com roxo e azul.
- 📊 **Exibição de Resultados:** Tabela limpa, com filtros e ordenação.
- 📤 **Exportação de Dados:** PDF, JSON ou TXT.
- 📋 **Botões de Cópia:** Copia dados formatados ou JSON bruto.
- 🔐 **Backend Proxy (Flask):** Sua chave da API nunca vai para o frontend.

---

## 📂 Estrutura do Projeto

```
LeakCheckApp/
├── app.py                # Backend Flask (API Proxy e servidor web)
├── index.html             # Frontend (interface web)
├── requirements.txt       # Dependências Python
├── Dockerfile             # Dockerfile
├── docker-compose.yml     # Docker Compose
└── README.md              # Este arquivo
```

---

## 🚀 Instalação e Execução

### ✅ Pré-requisitos

- Python 3.8+
- pip
- (Opcional) Conda
- Docker e Docker Compose (opcional)

### 🔧 Opção 1 — Executando Localmente com Python

#### ▶️ Usando Virtual Environment (`venv`)

```bash
cd LeakCheckApp

python -m venv venv

# Ativar:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

python app.py
```

Acesse:

```
http://127.0.0.1:5000
```

#### ▶️ Usando Conda

```bash
conda create -n leakcheck python=3.10
conda activate leakcheck
pip install -r requirements.txt
python app.py
```

---

### 🐳 Executando com Docker

#### ▶️ Usando Docker Compose (Recomendado)

1. Configure sua chave da API no `docker-compose.yml`:

```yaml
environment:
  - LEAKCHECK_API_KEY=SUA_CHAVE_AQUI
```

2. Execute:

```bash
docker-compose up --build
```

Acesse:

```
http://localhost:5000
```

#### ▶️ Docker Manual

```bash
docker build -t leakcheckapp .
docker run -p 5000:5000 -e LEAKCHECK_API_KEY=SUA_CHAVE_AQUI leakcheckapp
```

---

## 🌐 Como Usar a Interface Web

1. Acesse:

```
http://localhost:5000
```

2. No campo **"Informação"**, insira:
   - E-mail, domínio, nome de usuário, telefone, hash ou IP.
3. No dropdown, selecione o tipo:
   - `email`, `username`, `domain`, `phone`, `hash`, `ip`.
4. Clique em **"Pesquisar"**.
5. Visualize os resultados na tabela:
   - Dados vazados.
   - Fonte do vazamento.
   - Data da última violação.
6. Use:
   - **Copy Formatted:** Copia dados formatados.
   - **Copy Raw JSON:** Copia JSON bruto.
7. Exporte os dados:
   - PDF, JSON ou TXT.
8. Clique em **"Limpar Resultados"** para resetar a busca.

---

## 🔗 Como Usar a API REST

### 📍 URL Base

```
http://localhost:5000/api/v2/query/
```

### 📥 Exemplos de Requisição

#### 🔎 Pesquisa por E-mail

```bash
curl -X GET "http://localhost:5000/api/v2/query/example@example.com"
```

#### 🔎 Pesquisa por Domínio

```bash
curl -X GET "http://localhost:5000/api/v2/query/gmail.com?type=domain"
```

#### 🔎 Pesquisa por Nome de Usuário

```bash
curl -X GET "http://localhost:5000/api/v2/query/username_example?type=username"
```

### 🔄 Resposta de Exemplo

```json
{
  "query": "example@example.com",
  "type": "email",
  "success": true,
  "result": [
    {
      "source": "ExampleLeak2022",
      "last_breach": "2022-10-10",
      "data": {
        "password": "hashedpassword123",
        "ip": "192.168.0.1"
      }
    }
  ]
}
```

---

## ⚠️ Observações Importantes

- ✅ Sua chave LeakCheck é **obrigatória** para funcionamento.
- 🔒 Sua chave fica segura, nunca vai para o frontend.
- 🚫 O projeto **não armazena dados localmente**, apenas faz proxy da API LeakCheck.

---

## 📜 Licença

MIT License
