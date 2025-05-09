Repo Structure

loanboat/
│
├── backend/
│   ├── app.py
│   ├── collected_data.json (generated)
│   ├── questions.csv
│   ├── requirements.txt
│   └── logic/
│       └── engine.py
│
├── frontend/
│   └── index.html
│
└── README.md
# LoanBoat 🛥️ – Loan Profiling Chatbot

A simple, voice-enabled intelligent chatbot for loan profiling using Flask (Python) backend and HTML/JS frontend.

## 🌐 Live Features

- Collects user data through a structured conversation
- Uses dynamic CSV-driven logic
- Converts bot responses to speech using Web Speech API

---
This project uses Web Speech API (built into most modern browsers). No external TTS API or billing required.

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/udaykiran4383/loanboat.git
cd loanboat
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
#Frontend Setup
cd frontend
open index.html




