# ⚡ InterviewSignal

> **Developer Reputation Graph & AI-Powered Talent Signal for Students and Engineers**

InterviewSignal ingests GitHub developer telemetry (repositories, commit cadences, pull request activity, test coverage, and language depth) to compute a verifiable reputation graph and produce AI-driven recruiter summaries.

---

## 📦 Architecture & Stack

- **Backend**: FastAPI, SQLAlchemy 2.0 (Async), asyncpg, Pydantic v2, Redis, Celery, PostgreSQL
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, Radix UI
- **AI & Analytics**: Scoring Engine, OpenAI / Llama integration
- **DevOps**: Docker, Docker Compose, GitHub Actions CI/CD

---

## 📁 Repository Structure

```
interviewsignal/
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Environment variables
│   │   ├── database.py              # DB connection & session
│   │   ├── models/                  # SQLAlchemy ORM models (User, Analysis)
│   │   ├── routers/                 # API endpoints (Auth, Analysis, Profile)
│   │   ├── schemas/                 # Pydantic validation schemas
│   │   └── services/                # GitHub API, Scoring Engine, LLM
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── pages/                   # Login, Dashboard, Profile
│   │   ├── components/              # ScoreCard, RepoCard, SummaryPanel, Navbar
│   │   ├── context/                 # AuthContext & state
│   │   └── api/                     # Axios client
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## 🚀 Quickstart

### 1. Run with Docker Compose
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000` (or `http://localhost:5173` in dev mode)
- Backend API Docs: `http://localhost:8000/docs`

### 2. Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🛡️ License
MIT
