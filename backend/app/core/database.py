"""MongoDB repository with a transparent in-memory fallback for local demos."""
from datetime import datetime, timedelta, timezone
import random, uuid
from pymongo import MongoClient, ASCENDING, DESCENDING
from .config import settings

class Store:
    def __init__(self):
        self.client = None
        self.db = None
        self.memory = {name: [] for name in ["users","transactions","invoices","vendors","budgets","notifications","audit_logs","forecasts"]}
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
        for collection, field in [("users","email"),("transactions","date"),("transactions","vendor_id"),("invoices","invoice_number"),("invoices","vendor_id"),("vendors","vendor_id"),("audit_logs","timestamp")]:
            self.db[collection].create_index([(field, ASCENDING)])
    def collection(self, name): return self.db[name] if self.db is not None else MemoryCollection(self.memory[name])

class MemoryCollection:
    def __init__(self, items): self.items = items
    def find_one(self, query):
        return next((x for x in self.items if all(x.get(k) == v for k,v in query.items())), None)
    def find(self, query=None):
        query = query or {}
        return [x for x in self.items if all(x.get(k) == v for k,v in query.items())]
    def insert_one(self, doc): self.items.append(doc); return type("Result", (), {"inserted_id": doc["_id"]})()
    def update_one(self, query, update):
        doc = self.find_one(query)
        if doc and "$set" in update: doc.update(update["$set"])
        return type("Result", (), {"modified_count": int(bool(doc))})()
    def delete_one(self, query):
        doc = self.find_one(query)
        if doc: self.items.remove(doc)
        return type("Result", (), {"deleted_count": int(bool(doc))})()
    def count_documents(self, query=None): return len(self.find(query))

store = Store()

def seed_demo():
    if store.collection("transactions").count_documents() or store.collection("users").count_documents(): return
    from .security import hash_password
    users = [{"_id": str(uuid.uuid4()), "email":"demo@finsight.ai", "name":"Demo Finance Manager", "role":"FINANCE_MANAGER", "password_hash":hash_password("Demo123!") }]
    for doc in users: store.collection("users").insert_one(doc)
    vendors = []
    for i in range(1, 21):
        vendors.append({"_id":str(uuid.uuid4()),"vendor_id":f"VEN-{i:03}","vendor_name":f"{['Northstar','Acme','Vertex','Pioneer','Summit'][i%5]} {i}","category":["Technology","Operations","Marketing","Travel"][i%4],"total_spend":round(random.uniform(45000,420000),2),"average_invoice":round(random.uniform(4000,35000),2),"risk_score":random.randint(12,82),"status":"ACTIVE"})
    for d in vendors: store.collection("vendors").insert_one(d)
    now=datetime.now(timezone.utc)
    for i in range(240):
        amount=round(random.uniform(500,18000),2)
        if i == 7: amount=68000
        store.collection("transactions").insert_one({"_id":str(uuid.uuid4()),"transaction_id":f"TX-{i+1:04}","date":(now-timedelta(days=random.randint(0,365))).isoformat(),"amount":amount,"transaction_type":"INCOME" if i%4==0 else "EXPENSE","category":["Salaries","Operations","Marketing","Technology","Vendors","Travel"][i%6],"description":"Demo financial transaction","vendor_id":vendors[i%len(vendors)]["vendor_id"],"account":"Operating","payment_method":"Bank transfer","currency":"INR","status":"COMPLETED","risk_level":"HIGH" if i==7 else ("MEDIUM" if amount>14000 else "LOW"),"risk_score":88 if i==7 else random.randint(5,55)})
    for i in range(55):
        vendor=vendors[i%len(vendors)]
        total=485000 if i==41 else round(random.uniform(8000,70000),2)
        store.collection("invoices").insert_one({"_id":str(uuid.uuid4()),"invoice_number":"INV-1042" if i in (40,41) else f"INV-{1000+i}","vendor_id":vendor["vendor_id"],"vendor_name":vendor["vendor_name"],"invoice_date":(now-timedelta(days=i*3)).date().isoformat(),"due_date":(now+timedelta(days=i-8)).date().isoformat(),"subtotal":round(total*.9,2),"tax":round(total*.1,2),"discount":0,"total_amount":total,"currency":"INR","status":"FLAGGED" if i==41 else ("PAID" if i<20 else "PENDING"),"confidence_score":.94,"risk_score":89 if i==41 else random.randint(5,60),"risk_level":"HIGH" if i==41 else "LOW","issues":["Possible duplicate invoice detected","Amount is 177% above vendor average"] if i==41 else []})
    for category in ["Marketing","Technology","Operations","HR","Sales","Travel","Infrastructure"]:
        allocated=random.randint(50000,250000)
        store.collection("budgets").insert_one({"_id":str(uuid.uuid4()),"category":category,"allocated_budget":allocated,"actual_spending":round(allocated*random.uniform(.65,1.18),2),"business_priority":random.randint(50,95),"performance_score":random.randint(55,92)})
    for item in [{"title":"Potential duplicate invoice INV-1042","description":"Same vendor and amount submitted within 24 hours.","category":"Invoice Risk","severity":"HIGH","evidence":["Vendor historical average ₹175,000","Current invoice ₹485,000","Matching invoice number and amount"],"recommendation":"Review duplicate before approval.","confidence":.96},{"title":"Cash balance may fall below threshold","description":"Forecast indicates a pressure point in 32 days.","category":"Cash Flow Risk","severity":"MEDIUM","evidence":["Expense growth 14%","Upcoming payables exceed trailing average"],"recommendation":"Prioritize receivables and defer non-critical spend.","confidence":.87}]:
        item.update({"_id":str(uuid.uuid4()),"created_at":now.isoformat()}); store.collection("notifications").insert_one(item)
