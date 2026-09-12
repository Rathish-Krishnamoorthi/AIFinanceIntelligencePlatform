from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import seed_demo
from .routers import auth, dashboard, transactions, invoices, vendors, intelligence, assistant, approvals, notifications, audit

app = FastAPI(
    title="FinSight AI",
    version="1.0.0",
    description="Explainable financial intelligence and operations API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (auth.router, dashboard.router, transactions.router, invoices.router,
               vendors.router, intelligence.router, assistant.router, approvals.router,
               notifications.router, audit.router):
    app.include_router(router, prefix="/api")


@app.on_event("startup")
def startup():
    seed_demo()


@app.get("/api/health")
def health():
    from .core.database import store
    return {
        "status": "ok",
        "database": "mongodb" if not store.demo_mode else "demo-fallback",
        "message": "Demo data is used only because MongoDB is unavailable."
        if store.demo_mode else "Connected to MongoDB",
    }
