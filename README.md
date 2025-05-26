
# LeakCheck API Interface

A simple web application with a Flask backend that acts as a secure proxy for querying the LeakCheck API, keeping your API key safe and providing a user-friendly interface.

---

## 🔑 How to Get Your LeakCheck API Key

1. Go to [https://leakcheck.io/](https://leakcheck.io/).
2. Create a free or premium account (depending on your needs).
3. After logging in, go to: [https://leakcheck.io/account](https://leakcheck.io/account).
4. Copy your API key from your dashboard.

---

## 🔐 How to Configure Your API Key in the Project

### ✅ Option 1 — Directly in the Code (Simple)

Open the `app.py` file and locate:

```python
LEAKCHECK_API_KEY = "YOUR_LEAKCHECK_API_KEY"
```

Replace `"YOUR_LEAKCHECK_API_KEY"` with your actual API key.

### ✅ Option 2 — Using Environment Variables (Recommended)

In the `app.py` file, change:

```python
LEAKCHECK_API_KEY = os.getenv("LEAKCHECK_API_KEY")
```

Then, create a `.env` file in the project root with:

```
LEAKCHECK_API_KEY=YOUR_API_KEY
```

At the top of `app.py`, add:

```python
from dotenv import load_dotenv
load_dotenv()
```

Install the package if needed:

```bash
pip install python-dotenv
```

---

## 🖥️ Features

- 🔍 **LeakCheck API Queries:** Search by email, domain, username, phone, IP, hash, etc.
- 🖥️ **Modern UI:** Dark theme with purple and blue accents.
- 📊 **Results Display:** Clean table with sorting and filtering.
- 📤 **Data Export:** PDF, JSON, or TXT.
- 📋 **Copy Buttons:** Copy formatted data or raw JSON.
- 🔐 **Backend Proxy (Flask):** Your API key is never exposed to the frontend.

---

## 📂 Project Structure

```
LeakCheckApp/
├── app.py                # Flask Backend (API Proxy and Web Server)
├── index.html             # Web Frontend
├── requirements.txt       # Python Dependencies
├── Dockerfile             # Docker Image
├── docker-compose.yml     # Docker Compose
└── README.md              # This file
```

---

## 🚀 Installation and Running

### ✅ Prerequisites

- Python 3.8+
- pip
- (Optional) Conda
- Docker and Docker Compose (optional)

### 🔧 Option 1 — Running Locally with Python

#### ▶️ Using Virtual Environment (`venv`)

```bash
cd LeakCheckApp

python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

python app.py
```

Access:

```
http://127.0.0.1:5000
```

#### ▶️ Using Conda

```bash
conda create -n leakcheck python=3.10
conda activate leakcheck
pip install -r requirements.txt
python app.py
```

---

### 🐳 Running with Docker

#### ▶️ Using Docker Compose (Recommended)

1. Set your API key in `docker-compose.yml`:

```yaml
environment:
  - LEAKCHECK_API_KEY=YOUR_API_KEY
```

2. Run:

```bash
docker-compose up --build
```

Access:

```
http://localhost:5000
```

#### ▶️ Running with Docker Manually

```bash
docker build -t leakcheckapp .
docker run -p 5000:5000 -e LEAKCHECK_API_KEY=YOUR_API_KEY leakcheckapp
```

---

## 🌐 How to Use the Web Interface

1. Open:

```
http://localhost:5000
```

2. Enter **"Information"** such as:
   - Email, domain, username, phone, hash, or IP.
3. Select the type in the dropdown:
   - `email`, `username`, `domain`, `phone`, `hash`, `ip`.
4. Click **"Search"**.
5. View the results in the table:
   - Leaked data.
   - Source of the leak.
   - Date of the last breach.
6. Use:
   - **Copy Formatted:** Copies nicely formatted data.
   - **Copy Raw JSON:** Copies raw JSON data.
7. Export data:
   - PDF, JSON, or TXT.
8. Click **"Clear Results"** to reset the search.

---

## 🔗 How to Use the REST API

### 📍 Base URL

```
http://localhost:5000/api/v2/query/
```

### 📥 Request Examples

#### 🔎 Search by Email

```bash
curl -X GET "http://localhost:5000/api/v2/query/example@example.com"
```

#### 🔎 Search by Domain

```bash
curl -X GET "http://localhost:5000/api/v2/query/gmail.com?type=domain"
```

#### 🔎 Search by Username

```bash
curl -X GET "http://localhost:5000/api/v2/query/username_example?type=username"
```

### 🔄 Example Response

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

## ⚠️ Important Notes

- ✅ Your LeakCheck API key is **required** for the backend to work.
- 🔒 Your key is safe and never exposed to the frontend.
- 🚫 This project **does not store any data locally**, it only proxies requests to the LeakCheck API.

---

## 📜 License

MIT License
