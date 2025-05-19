# Investor Chat Assistant

## 📁 Setup Instructions

### 1. Add The Company Data

Create a directory named `company_data` inside the `backend` folder.  
Place all relevant company `.json` files (e.g. `context.json`, `UK.json`, `consolidated.json`, etc.) inside this folder.

### 2. Add The Gemini API Key

Open the `docker-compose.yml` file and add the Gemini API key under the `backend` service

### 3. Run

```bash
docker compose up --build
```
Check Results in http://localhost:5173/