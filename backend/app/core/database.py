"""MongoDB repository with a transparent in-memory fallback for local development."""
import json
import uuid
from pathlib import Path
from pymongo import MongoClient, ASCENDING, DESCENDING
from .config import settings

class Store:
    def __init__(self):
        self.client = None
        self.db = None
        self.memory_path = Path(__file__).resolve().parents[2] / "data" / "store.json"
        self.memory = self._load_memory()
        if settings.mongodb_uri:
            try:
                self.client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=1200)
                self.client.admin.command("ping")
                self.db = self.client[settings.database_name]
                self._indexes()
            except Exception:
                self.client, self.db = None, None
    @property
    def demo_mode(self): return self.db is None
    def _indexes(self):
        for collection, field in [("users","email"),("transactions","date"),("transactions","vendor_id"),("transactions","department"),("invoices","invoice_number"),("invoices","vendor_id"),("invoices","department"),("invoices","file_hash"),("vendors","vendor_id"),("audit_logs","timestamp")]:
            self.db[collection].create_index([(field, ASCENDING)])
    def _load_memory(self):
        if self.memory_path.exists():
            try:
                with self.memory_path.open("r", encoding="utf-8") as file:
                    stored = json.load(file)
                if isinstance(stored, dict):
                    return {name: list(stored.get(name, [])) for name in [
                        "users", "transactions", "invoices", "vendors", "budgets",
                        "notifications", "audit_logs", "forecasts", "departments"
                    ]}
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Could not load local database file {self.memory_path}") from exc
        return {name: [] for name in [
            "users", "transactions", "invoices", "vendors", "budgets",
            "notifications", "audit_logs", "forecasts", "departments"
        ]}

    def _persist_memory(self):
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.memory_path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(self.memory, file, ensure_ascii=True, indent=2)
        temporary_path.replace(self.memory_path)

    def collection(self, name):
        return self.db[name] if self.db is not None else MemoryCollection(
            self.memory[name], self._persist_memory
        )

class MemoryCollection:
    def __init__(self, items, persist): self.items, self.persist = items, persist
    def find_one(self, query):
        return next((x for x in self.items if self._matches(x, query)), None)
    def find(self, query=None):
        query = query or {}
        return [x for x in self.items if self._matches(x, query)]
    @staticmethod
    def _matches(document, query):
        for key, expected in query.items():
            actual = document.get(key)
            if isinstance(expected, dict):
                if "$ne" in expected and actual == expected["$ne"]:
                    return False
                if "$in" in expected and actual not in expected["$in"]:
                    return False
            elif actual != expected:
                return False
        return True
    def insert_one(self, doc):
        self.items.append(doc)
        self.persist()
        return type("Result", (), {"inserted_id": doc["_id"]})()
    def update_one(self, query, update):
        doc = self.find_one(query)
        if doc and "$set" in update:
            doc.update(update["$set"])
            self.persist()
        return type("Result", (), {"modified_count": int(bool(doc))})()
    def delete_one(self, query):
        doc = self.find_one(query)
        if doc:
            self.items.remove(doc)
            self.persist()
        return type("Result", (), {"deleted_count": int(bool(doc))})()
    def count_documents(self, query=None): return len(self.find(query))

store = Store()

def seed_demo():
    """Kept for backwards compatibility; production and local starts are empty by default."""
    return None
