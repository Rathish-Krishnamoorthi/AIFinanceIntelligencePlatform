"""Populate the configured MongoDB database (or demo fallback) with safe sample data."""
from app.core.database import seed_demo, store
seed_demo()
print(f"Seed complete ({'MongoDB' if not store.demo_mode else 'in-memory demo fallback'}). Demo login: demo@finsight.ai / Demo123!")
