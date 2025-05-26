# LeakCheck API Interface

A secure web app with a Flask backend acting as a proxy to the LeakCheck API. Keep your API key safe while using a modern, user-friendly interface to check if your data has been leaked.

---

## 🔑 How to Get Your LeakCheck API Key

1. Go to [https://leakcheck.io/](https://leakcheck.io/).
2. Create a free or premium account.
3. Go to your account page: [https://leakcheck.io/account](https://leakcheck.io/account).
4. Copy your API key.

---

## 🔐 How to Configure the API Key

The API key is configured via an **environment variable** using a `.env` file (✅ safer and required):

1. Create a file named `.env` in the project root:

```
LEAKCHECK_API_KEY=YOUR_API_KEY_HERE
```

2. The backend automatically loads this file with:

```python
from dotenv import load_dotenv
load_dotenv()
```

⚠️ If the key is missing, the backend will throw an error and refuse to run.

---

## 🖥️ Features

- 🔐 API key secured in backend (never exposed to frontend)
- 🚫 Rate limiting (default: 10 requests per minute, 5 requests per endpoint)
- 🔍 Query by:
  - Email, username, phone, domain, hash, IP, etc.
- 🎨 Modern UI with dark theme
- 📑 Clean results table with source and last breach info
- 📋 Copy results (formatted or raw JSON)
- 📤 Export to PDF, JSON, TXT
- 🔥 Clear error handling for:
  - Connection errors
  - API timeouts
  - Missing API key
  - Invalid queries

---

## 📂 Project Structure

```
LeakCheckApp/
├── app.py                # Flask backend (API proxy + web server)
├── index.html             # Web frontend
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container (optional)
├── docker-compose.yml     # Docker Compose (optional)
└── README.md              # Documentation
```

---

## 🚀 Installation & Running

### ✅ Prerequisites

- Python 3.8+
- pip
- (Optional) Docker and Docker Compose

### 🔧 Local Run (Recommended)

```bash
cd LeakCheckApp

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\ctivate

pip install -r requirements.txt

# Create .env file with:
# LEAKCHECK_API_KEY=YOUR_API_KEY

python app.py
```

Access the web app at:

```
http://127.0.0.1:5000
```

---

### 🐳 Docker

**Using Docker Compose:**

1. Edit `docker-compose.yml`:

```yaml
environment:
  - LEAKCHECK_API_KEY=YOUR_API_KEY
```

2. Run:

```bash
docker-compose up --build
```

**Manual Docker run:**

```bash
docker build -t leakcheckapp .
docker run -p 5000:5000 -e LEAKCHECK_API_KEY=YOUR_API_KEY leakcheckapp
```

---

## 🌐 Using the Web Interface

1. Visit `http://localhost:5000`.
2. Enter the info (email, username, domain, etc.).
3. Select the type (or use auto).
4. Click **Search**.
5. View leaks, source, and breach date.
6. Copy or export the results (PDF, JSON, TXT).
7. Clear results to start a new search.

---

## 🔗 Using the REST API

**Base URL:**

```
http://localhost:5000/api/v2/query/
```

**Example Request:**

```bash
curl "http://localhost:5000/api/v2/query/example@example.com"
```

**With type:**

```bash
curl "http://localhost:5000/api/v2/query/example.com?type=domain"
```

**Example Response:**

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

## ⚠️ Notes

- Your API key is **required**.
- Key is **never exposed** to the frontend.
- ✅ The backend includes rate limiting and error handling.
- No data is stored locally. This is a read-only proxy.

---

## 📜 License

MIT License