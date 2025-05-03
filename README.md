# FURIA CS Chatbot

A fan-focused chatbot for the FURIA Counter-Strike team, with a Python/FastAPI backend and React/Vite frontend.  
It answers in Portuguese about next matches, last game stats, player stats, roster, and news, using a static JSON data source.


---

## 🛠️ Backend Setup (Python / FastAPI)

### 1. Prerequisites

- Python 3.9+  
- Git  
- (Optional) Visual Studio C++ Build Tools on Windows  

### 2. Create & activate virtualenv

python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm

### 4. (Re)train the intent model
Whenever you update data/intents.json, run:

python train_intent.py
This generates or refreshes models/intent_pipeline.joblib.

### 5. Run the API server

uvicorn app:app --reload --port 8000
The API will be available at http://localhost:8000/api/chat

CORS is enabled for the frontend origin (http://localhost:5173).