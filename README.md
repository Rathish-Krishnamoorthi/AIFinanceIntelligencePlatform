# FinSight AI

FinSight AI is a production-oriented financial intelligence platform: JWT-protected operations, MongoDB-ready persistence, explainable anomaly/risk scoring, invoice workflow, cash-flow forecasting, budget recommendations, and a data-grounded assistant.

## Features

- FastAPI REST API with OpenAPI at `http://localhost:8000/api/docs`
- React/Vite + MUI responsive executive dashboard with Recharts
- MongoDB Atlas repository with indexes and a transparent in-memory demo fallback
- Secure password hashing and JWT bearer authentication with role claims
- Invoice PDF/image upload validation, extraction fallback, duplicate/risk workflow
- Explainable anomaly detection, vendor risk, forecast confidence ranges, and budget evidence
- Transactions, invoices, vendors, approvals, notifications, audit logs, and assistant endpoints

## Architecture

`frontend/` is a Vite SPA communicating exclusively through Axios with `backend/app/main.py`.
The backend keeps persistence in `core/database.py`, security in `core/security.py`, and analytics calculations behind API services. When `MONGODB_URI` is absent or unavailable, startup seeds realistic demo records in memory and reports `database_mode: demo`; errors are not hidden.

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Optional MongoDB Atlas setup: put a restricted Atlas connection string in `backend/.env` as `MONGODB_URI`, set `DATABASE_NAME`, and allow the development IP in Atlas Network Access. No frontend secret is required.

Seed explicitly with `python seed.py`. Startup also seeds an empty database. Demo credentials are `demo@finsight.ai` / `Demo123!`.

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` to the deployed API URL when deploying. Never put `MONGODB_URI`, `JWT_SECRET`, or an LLM key in frontend variables.

## API highlights

`POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`, dashboard metrics, CRUD transactions, invoice upload/approval, vendors, anomalies, `/api/forecast/cash-flow`, budgets/recommendations, risk overview, `/api/assistant/chat`, approvals, notifications, and audit logs. Every protected route requires the JWT returned by login.

## AI/ML approach

The baseline is intentionally deterministic and auditable: feature/rule scoring uses amount deviation, frequency, risk levels, and vendor history; forecasting uses a moving-average/regression-style baseline and confidence band; budget recommendations use utilization, performance, and projected spend. Responses include evidence, reasoning, recommendation, and confidence and never label an anomaly as confirmed fraud. These modules can be replaced with trained Isolation Forest/LOF or an LLM gateway without changing API contracts.

## Deployment

Run the backend with a production ASGI process (for example `gunicorn -k uvicorn.workers.UvicornWorker app.main:app`) and serve the Vite `dist/` output behind a reverse proxy. Configure HTTPS, a strong random `JWT_SECRET`, restrictive CORS, Atlas TLS/IP rules, log aggregation, and object storage for uploaded documents before production.
