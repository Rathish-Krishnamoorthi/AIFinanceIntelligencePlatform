# MASTER DEVELOPMENT PROMPT

## AI Financial Intelligence Platform

Build a production-quality full-stack web application called **Fintel — AI-Powered Financial Intelligence & Operations Platform**.

The platform must analyze business financial data, detect anomalies and fraud, process invoices, forecast cash flow, optimize budgets, automate financial workflows, and provide explainable AI-powered recommendations.

The application must be implemented using:

* **Frontend:** React.js + Vite
* **UI:** Material UI (MUI) or Tailwind CSS
* **Backend:** Python + FastAPI
* **Database:** MongoDB Atlas
* **Authentication:** JWT
* **AI/ML:** Python-based machine learning models
* **Charts:** Recharts
* **API Communication:** Axios
* **File Processing:** PDF/image invoice extraction
* **Deployment-ready architecture**

Do NOT create a simple CRUD application. The project must clearly demonstrate AI/ML-based financial intelligence, anomaly detection, forecasting, explainability, and automation.

---

# 1. PROJECT VISION

Create a centralized financial intelligence platform for businesses.

The system should allow a finance manager to:

1. Upload and process invoices.
2. Automatically extract invoice information.
3. Validate invoices against business rules.
4. Detect duplicate invoices.
5. Detect unusual vendor behavior.
6. Detect suspicious financial transactions.
7. Forecast future cash flow.
8. Predict upcoming cash requirements.
9. Analyze current budgets.
10. Recommend optimal budget allocation.
11. Monitor financial risks.
12. Ask financial questions through an AI Financial Assistant.
13. Receive explainable recommendations.
14. Automate approval workflows.
15. Monitor all financial operations from one dashboard.

The platform should answer:

> "What is happening with the company's money, what could go wrong, what is likely to happen next, and what should the finance team do?"

---

# 2. MAIN MODULES

Implement the following modules.

## Module 1 — Financial Dashboard

Create a modern executive dashboard.

Display:

* Total Revenue
* Total Expenses
* Net Cash Flow
* Accounts Payable
* Accounts Receivable
* Pending Invoices
* Paid Invoices
* Overdue Invoices
* Suspicious Transactions
* Financial Risk Score
* Forecasted Cash Balance

Include charts:

### Revenue vs Expenses

Line/bar chart showing:

* Revenue
* Expenses
* Profit

over time.

### Cash Flow

Display:

* Historical cash flow
* Forecasted cash flow
* Confidence interval

### Expense Distribution

Pie/donut chart:

* Salaries
* Operations
* Marketing
* Technology
* Vendors
* Travel
* Other

### Risk Overview

Show:

* Low Risk
* Medium Risk
* High Risk

### AI Insights

Generate cards such as:

"Marketing expenses increased 18% compared with the previous month."

"Vendor ABC has submitted 3 invoices with similar amounts within 24 hours."

"Projected cash balance may fall below the minimum threshold in 45 days."

Every insight must explain WHY it was generated.

---

# 3. AUTHENTICATION AND USER MANAGEMENT

Implement JWT authentication.

Roles:

* ADMIN
* FINANCE_MANAGER
* ACCOUNTANT
* AUDITOR

Features:

* Register
* Login
* Logout
* Password hashing
* JWT access token
* Refresh token if appropriate
* Protected routes
* Role-based authorization
* User profile

Frontend should have:

* Login page
* Register page
* Protected dashboard
* Profile page

Backend:

/api/auth/register
/api/auth/login
/api/auth/me

Use bcrypt/passlib or an appropriate secure password hashing mechanism.

---

# 4. FINANCIAL DATA MANAGEMENT

Create financial transaction management.

Transaction fields:

```text
transaction_id
date
amount
transaction_type
category
description
vendor_id
customer_id
account
payment_method
currency
status
created_at
```

Transaction types:

* INCOME
* EXPENSE
* TRANSFER
* REFUND

Create APIs:

```text
POST   /api/transactions
GET    /api/transactions
GET    /api/transactions/{id}
PUT    /api/transactions/{id}
DELETE /api/transactions/{id}
```

Add filtering:

* Date range
* Amount
* Category
* Vendor
* Transaction type
* Risk level
* Status

---

# 5. INTELLIGENT INVOICE PROCESSING

Build an AI-powered invoice processing system.

Users should be able to upload:

* PDF invoices
* JPG invoices
* PNG invoices

The backend should process the invoice automatically.

Extract:

```text
invoice_number
vendor_name
vendor_id
invoice_date
due_date
subtotal
tax
discount
total_amount
currency
payment_terms
bank_details
line_items
```

For line items:

```text
description
quantity
unit_price
tax
total
```

Use:

* PyMuPDF / pypdf for PDFs
* OCR using Tesseract or another suitable OCR engine
* Regex/rule-based extraction
* Optional ML/LLM extraction layer

The system must return:

```json
{
  "invoice_number": "...",
  "vendor": "...",
  "total_amount": 125000,
  "tax": 22500,
  "confidence_score": 0.94
}
```

Display extracted information on the frontend.

Allow the accountant to:

* Review
* Edit
* Approve
* Reject

the extracted invoice.

---

# 6. INVOICE VALIDATION ENGINE

After extraction, automatically validate invoices.

Validation rules:

### Duplicate Invoice

Check:

* Same invoice number
* Same vendor
* Same amount
* Similar invoice date

### Amount Validation

Detect:

* Unexpectedly large invoice
* Unusual tax
* Incorrect totals

### Vendor Validation

Check whether:

* Vendor exists
* Vendor is active
* Vendor bank account changed
* Vendor has unusual activity

### Date Validation

Detect:

* Future invoice date
* Invoice submitted after unusual delay
* Duplicate invoice dates

### Mathematical Validation

Verify:

```text
subtotal + tax - discount = total
```

Generate a validation result:

```json
{
  "status": "WARNING",
  "issues": [
    "Invoice amount is 42% higher than vendor's historical average",
    "Possible duplicate invoice detected"
  ]
}
```

---

# 7. AI FRAUD AND ANOMALY DETECTION

Create a dedicated anomaly detection engine.

Use machine learning algorithms such as:

* Isolation Forest
* Local Outlier Factor
* statistical Z-score
* rolling averages
* transaction frequency analysis

Use features such as:

```text
transaction_amount
transaction_frequency
vendor_frequency
time_of_transaction
category
historical_vendor_amount
amount_deviation
invoice_frequency
```

The model should produce:

```text
anomaly_score
risk_score
risk_level
reason
```

Example:

```json
{
  "anomaly_score": 0.87,
  "risk_score": 82,
  "risk_level": "HIGH",
  "reasons": [
    "Transaction is 3.8x higher than historical average",
    "Vendor normally submits invoices once per month",
    "Three invoices were submitted within 6 hours"
  ]
}
```

IMPORTANT:

Do not simply display:

> "AI detected fraud."

Instead display:

> "High risk because the transaction is 3.8× above the vendor's historical average and occurred outside the vendor's normal transaction pattern."

The system should distinguish between:

* Normal
* Unusual
* Suspicious
* High Risk

Do NOT claim that an anomaly is definitely fraud.

---

# 8. ACCOUNTS PAYABLE INTELLIGENCE

Create an Accounts Payable dashboard.

Display:

* Total payable
* Upcoming payments
* Overdue payments
* High-risk invoices
* Duplicate invoices
* Vendor risk
* Payment priority

Create a payment priority score.

Example:

```text
Payment Priority =

Invoice Urgency
+ Due Date Risk
+ Vendor Importance
+ Late Payment Risk
+ Financial Risk
```

Display:

| Invoice | Vendor   |    Amount | Due Date | Risk | Priority |
| ------- | -------- | --------: | -------- | ---- | -------- |
| INV001  | Vendor A |   ₹80,000 | 3 days   | Low  | High     |
| INV002  | Vendor B | ₹2,40,000 | 15 days  | High | Critical |

---

# 9. VENDOR INTELLIGENCE

Create vendor profiles.

Vendor fields:

```text
vendor_id
vendor_name
category
contact
total_transactions
total_spend
average_invoice
invoice_frequency
payment_history
risk_score
status
```

Generate vendor analytics:

* Total spend
* Average invoice
* Number of invoices
* Average payment delay
* Spending trend
* Anomaly frequency
* Risk score

Detect:

* Sudden price increases
* Unusual invoice frequency
* Duplicate invoices
* Vendor concentration risk
* New vendor risk

---

# 10. CASH FLOW FORECASTING ENGINE

Create a machine-learning cash-flow forecasting system.

Historical data:

```text
date
income
expense
cash_balance
category
```

Forecast:

* 7 days
* 30 days
* 60 days
* 90 days

Possible models:

* Moving Average
* Linear Regression
* Random Forest
* XGBoost if available
* Prophet if appropriate

Start with a reliable baseline model and allow the architecture to be extended.

Output:

```text
forecast_date
predicted_income
predicted_expense
predicted_cash_balance
confidence
```

Display:

### Historical Cash Flow

Solid line.

### Forecast

Dashed line.

### Confidence Range

Upper and lower forecast bounds.

Generate alerts:

> "Cash balance is projected to fall below ₹5,00,000 within 32 days."

> "Expected expenses are likely to increase by 14% next month."

---

# 11. DYNAMIC BUDGET OPTIMIZATION

Create a budget optimization engine.

Users can define budgets for:

* Marketing
* Technology
* Operations
* HR
* Sales
* Travel
* Infrastructure

For each category store:

```text
allocated_budget
actual_spending
historical_spending
business_priority
performance_score
```

Calculate:

```text
budget_utilization
variance
forecasted_spending
recommended_budget
```

Example recommendation:

```text
Marketing

Current Budget: ₹10,00,000
Expected Spend: ₹8,20,000
Performance: 72%

Recommended Budget: ₹8,50,000

Reason:
Historical utilization is 82% and ROI is below the company average.
```

Allow the finance manager to:

* Accept recommendation
* Reject recommendation
* Modify recommendation

Track decisions.

---

# 12. FINANCIAL RISK INTELLIGENCE

Create a Financial Risk Dashboard.

Calculate an overall risk score from:

```text
Cash Flow Risk
Expense Risk
Vendor Risk
Invoice Risk
Transaction Risk
Budget Risk
Payment Risk
```

Example:

```text
Overall Financial Risk: 64 / 100
Risk Level: MEDIUM
```

Display a risk breakdown.

Example:

```text
Cash Flow Risk        72
Vendor Risk           45
Invoice Risk          61
Expense Risk          38
Transaction Risk      79
Budget Risk           51
```

Use a weighted scoring system.

Make weights configurable.

---

# 13. AI FINANCIAL DECISION ASSISTANT

Create an AI-powered financial assistant.

The user can ask questions such as:

```text
Why did expenses increase this month?

Which vendors are high risk?

What will our cash balance look like next month?

Which invoices should we prioritize?

Are there suspicious transactions?

Which department is overspending?

How can we reduce expenses?

Should we increase the marketing budget?

What are our biggest financial risks?
```

The assistant must NOT hallucinate financial information.

It should retrieve structured information from MongoDB and analytics/ML services before generating responses.

Architecture:

```text
User Question
      ↓
Intent Detection
      ↓
Financial Data Retrieval
      ↓
Analytics / ML
      ↓
LLM Reasoning Layer
      ↓
Explainable Answer
```

Responses should include:

### Answer

Short natural-language answer.

### Evidence

Relevant numbers used.

### Reasoning

Why the system reached the conclusion.

### Recommendation

What action should be considered.

### Confidence

Confidence score.

Example:

```text
Question:
Why did expenses increase this month?

Answer:
Expenses increased by 18.4% compared with last month.

Evidence:
• Technology spending increased 31%.
• Vendor expenses increased 22%.
• Two large infrastructure invoices were recorded.

Reasoning:
The majority of the increase came from technology and infrastructure expenses.

Recommendation:
Review the two infrastructure invoices and consider moving non-critical
technology purchases to next month.

Confidence: 91%
```

---

# 14. EXPLAINABLE AI

This is a CORE REQUIREMENT.

Every AI-generated decision must provide explanations.

For anomaly detection show:

```text
Risk Score: 86

Why?
✓ Amount is 3.2× historical average
✓ Transaction occurred outside normal time
✓ Vendor frequency increased significantly
✓ Similar invoice detected
```

For forecasting:

```text
Forecast: ₹4.2M

Main factors:
• Historical seasonal pattern
• Upcoming accounts payable
• Average monthly revenue
• Recent expense growth
```

For budget recommendations:

```text
Recommendation: Reduce Technology Budget by 8%

Reasons:
• 21% under-utilization
• Low recent ROI
• Spending below allocated budget
• Forecasted demand is stable
```

Never display an unexplained AI score.

---

# 15. AUTOMATED APPROVAL WORKFLOW

Implement financial workflows.

Example:

```text
Invoice Uploaded
      ↓
OCR Extraction
      ↓
Validation
      ↓
Anomaly Detection
      ↓
Risk Assessment
      ↓
Approval Decision
      ↓
Payment Queue
```

Rules:

### Low Risk

Automatically move to approval.

### Medium Risk

Require finance manager review.

### High Risk

Block automatic approval and require manual investigation.

Create workflow states:

```text
UPLOADED
PROCESSING
VALIDATED
PENDING_APPROVAL
APPROVED
REJECTED
FLAGGED
PAID
```

---

# 16. NOTIFICATION SYSTEM

Create notifications for:

* High-risk transaction
* Duplicate invoice
* High-risk vendor
* Upcoming payment
* Cash-flow warning
* Budget overrun
* Forecasted financial risk

Display notifications in the frontend.

---

# 17. AUDIT LOG

Every important financial operation must be logged.

Audit fields:

```text
user_id
action
entity_type
entity_id
old_value
new_value
timestamp
reason
```

Examples:

```text
User approved invoice INV-1023.

User rejected AI budget recommendation.

Invoice INV-1002 was automatically flagged as a duplicate.

Transaction TX-883 was classified as high risk.
```

Create an Audit Logs page.

---

# 18. MONGODB ATLAS DATABASE DESIGN

Use MongoDB Atlas.

Create collections:

```text
users
transactions
invoices
invoice_items
vendors
budgets
cash_flow
forecasts
anomalies
risk_assessments
recommendations
approvals
notifications
audit_logs
financial_metrics
```

Use proper indexes.

Important indexes:

```text
users.email
transactions.date
transactions.vendor_id
transactions.category
invoices.invoice_number
invoices.vendor_id
invoices.invoice_date
vendors.vendor_id
anomalies.risk_level
audit_logs.timestamp
```

Use environment variables:

```env
MONGODB_URI=
DATABASE_NAME=financial_intelligence
JWT_SECRET=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
LLM_API_KEY=
```

Never hardcode secrets.

---

# 19. FASTAPI BACKEND STRUCTURE

Use a clean modular architecture.

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── invoice.py
│   │   ├── vendor.py
│   │   ├── budget.py
│   │   ├── forecast.py
│   │   ├── anomaly.py
│   │   └── audit.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── invoice.py
│   │   ├── vendor.py
│   │   ├── budget.py
│   │   └── forecast.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── transactions.py
│   │   ├── invoices.py
│   │   ├── vendors.py
│   │   ├── anomalies.py
│   │   ├── forecasting.py
│   │   ├── budgets.py
│   │   ├── risk.py
│   │   ├── assistant.py
│   │   ├── approvals.py
│   │   ├── notifications.py
│   │   └── audit.py
│   │
│   ├── services/
│   │   ├── invoice_service.py
│   │   ├── ocr_service.py
│   │   ├── anomaly_service.py
│   │   ├── forecasting_service.py
│   │   ├── budget_service.py
│   │   ├── risk_service.py
│   │   ├── recommendation_service.py
│   │   ├── assistant_service.py
│   │   └── workflow_service.py
│   │
│   ├── ml/
│   │   ├── anomaly_model.py
│   │   ├── forecasting_model.py
│   │   ├── risk_model.py
│   │   └── budget_optimizer.py
│   │
│   └── utils/
│       ├── invoice_parser.py
│       ├── validators.py
│       └── helpers.py
│
├── requirements.txt
├── .env
└── README.md
```

Use FastAPI routers with `/api/...` prefixes.

Enable CORS for the React frontend.

Expose:

```text
/api/docs
/api/redoc
```

---

# 20. REACT FRONTEND STRUCTURE

Create:

```text
frontend/
│
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── MetricCard.jsx
│   │   ├── RiskBadge.jsx
│   │   ├── AIInsightCard.jsx
│   │   ├── DataTable.jsx
│   │   ├── Loading.jsx
│   │   └── ErrorMessage.jsx
│   │
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Transactions.jsx
│   │   ├── Invoices.jsx
│   │   ├── InvoiceDetails.jsx
│   │   ├── Vendors.jsx
│   │   ├── VendorDetails.jsx
│   │   ├── Anomalies.jsx
│   │   ├── Forecasting.jsx
│   │   ├── Budgets.jsx
│   │   ├── RiskDashboard.jsx
│   │   ├── Approvals.jsx
│   │   ├── FinancialAssistant.jsx
│   │   ├── Notifications.jsx
│   │   └── AuditLogs.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── hooks/
│   │   └── useAuth.js
│   │
│   ├── utils/
│   │   └── formatters.js
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
└── .env
```

Use Axios for all API requests.

Example:

```javascript
import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
});

export default api;
```

Use an Axios interceptor for JWT authentication.

---

# 21. FRONTEND DESIGN

Create a professional financial SaaS dashboard.

Design characteristics:

* Modern
* Clean
* Responsive
* Desktop-first
* Mobile responsive
* Professional financial analytics appearance

Sidebar:

```text
Dashboard
Transactions
Invoices
Vendors
Anomalies
Cash Flow
Budgets
Risk Intelligence
Approvals
AI Assistant
Notifications
Audit Logs
Settings
```

Top navigation:

* Search
* Notifications
* User profile
* Logout

Use charts extensively.

Do not make every page a table.

Use:

* Cards
* Charts
* Graphs
* Risk indicators
* Timeline
* Progress bars
* AI insight cards
* Interactive filters

---

# 22. DASHBOARD INTERACTIONS

Dashboard filters:

```text
Date Range
Department
Category
Vendor
Risk Level
Transaction Type
```

When filters change, update the charts and metrics through API calls.

Do not hardcode dashboard numbers.

All dashboard values must come from backend APIs.

---

# 23. AI INSIGHT GENERATION

Create a backend service that periodically analyzes financial data.

Generate insights such as:

```text
Expense Growth
Cash Flow Risk
Vendor Risk
Invoice Risk
Budget Variance
Revenue Trend
```

Store generated insights in MongoDB.

Each insight must contain:

```text
title
description
category
severity
evidence
recommendation
confidence
created_at
```

---

# 24. SEED DATA

Create a seed script.

The application must work immediately after setup.

Generate realistic sample data for:

* 20+ vendors
* 200+ transactions
* 50+ invoices
* 12 months of financial history
* Multiple budgets
* Historical cash flow
* Some anomalies
* Some duplicate invoices
* Some high-risk transactions

Make the data realistic.

Include intentional anomalies so that the AI dashboard visibly demonstrates its capabilities.

Examples:

* Transaction 4× normal amount
* Duplicate invoice
* Vendor suddenly increasing invoice frequency
* Unusual transaction time
* Budget overspending
* Cash-flow decline

---

# 25. MACHINE LEARNING PIPELINE

Create reusable ML services.

The ML pipeline should:

```text
Load Data
   ↓
Clean Data
   ↓
Feature Engineering
   ↓
Train Model
   ↓
Evaluate
   ↓
Save Model
   ↓
Inference
   ↓
Explain Prediction
```

Models should not train on every API request.

Implement model loading/caching appropriately.

If a trained model does not exist, automatically train using available historical data.

---

# 26. MODEL EXPLAINABILITY

For every prediction, expose important features.

Example:

```json
{
  "prediction": "HIGH_RISK",
  "score": 0.86,
  "important_factors": [
    {
      "feature": "amount_deviation",
      "impact": 0.42
    },
    {
      "feature": "vendor_frequency",
      "impact": 0.28
    }
  ]
}
```

Frontend should visualize these factors.

Use horizontal bars or explanation cards.

---

# 27. FINANCIAL ASSISTANT ARCHITECTURE

Implement the assistant as a controlled financial RAG/data-query system.

Do NOT allow the LLM to directly invent numbers.

Pipeline:

```text
Question
   ↓
Intent Classification
   ↓
Determine Required Data
   ↓
MongoDB Query
   ↓
Analytics / ML Calculation
   ↓
Build Evidence
   ↓
LLM Explanation
   ↓
Final Answer
```

The LLM receives only relevant structured financial information.

Example:

User:

> Which vendor has the highest risk?

Backend calculates:

```text
Vendor A = 31
Vendor B = 82
Vendor C = 45
```

Then the LLM explains:

> Vendor B currently has the highest risk score of 82 because its invoice frequency increased 2.7× and its average invoice amount increased 41%.

---

# 28. API ENDPOINTS

Implement at minimum:

## Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

## Dashboard

```text
GET /api/dashboard/summary
GET /api/dashboard/expenses
GET /api/dashboard/revenue
GET /api/dashboard/cash-flow
GET /api/dashboard/insights
```

## Transactions

```text
GET /api/transactions
POST /api/transactions
GET /api/transactions/{id}
PUT /api/transactions/{id}
DELETE /api/transactions/{id}
```

## Invoices

```text
POST /api/invoices/upload
GET /api/invoices
GET /api/invoices/{id}
PUT /api/invoices/{id}
POST /api/invoices/{id}/approve
POST /api/invoices/{id}/reject
```

## Vendors

```text
GET /api/vendors
GET /api/vendors/{id}
GET /api/vendors/{id}/risk
```

## Anomalies

```text
GET /api/anomalies
GET /api/anomalies/{id}
POST /api/anomalies/analyze
```

## Forecasting

```text
GET /api/forecast/cash-flow
POST /api/forecast/train
```

## Budgets

```text
GET /api/budgets
POST /api/budgets
PUT /api/budgets/{id}
GET /api/budgets/recommendations
```

## Risk

```text
GET /api/risk/overview
GET /api/risk/vendors
GET /api/risk/transactions
```

## Assistant

```text
POST /api/assistant/chat
```

## Approvals

```text
GET /api/approvals
POST /api/approvals/{id}/approve
POST /api/approvals/{id}/reject
```

## Notifications

```text
GET /api/notifications
PUT /api/notifications/{id}/read
```

## Audit

```text
GET /api/audit-logs
```

---

# 29. ERROR HANDLING

Implement proper error handling.

Backend:

* Pydantic validation
* HTTPException
* centralized exception handling
* structured logging

Frontend:

* API error handling
* Loading states
* Empty states
* Retry states
* Toast notifications

Never allow a backend exception to crash the entire application.

---

# 30. SECURITY

Implement:

* JWT authentication
* Password hashing
* Role-based access
* CORS configuration
* Environment variables
* Input validation
* File type validation
* File size validation
* Secure file handling
* MongoDB connection security

Do not expose:

* MongoDB URI
* JWT secret
* LLM API key

in frontend code.

---

# 31. DEMO MODE

Create a Demo Mode so judges can immediately understand the project.

Provide a button:

> "Load Demo Financial Data"

It should populate the dashboard with realistic sample data.

Include a guided demonstration:

```text
1. Upload invoice
2. Extract invoice data
3. Detect duplicate
4. Calculate risk
5. Approve/reject
6. View anomaly dashboard
7. View cash-flow forecast
8. View budget recommendation
9. Ask AI Assistant
```

---

# 32. IMPORTANT DEMO SCENARIO

Create one complete end-to-end scenario.

Example:

A vendor uploads:

```text
Invoice #INV-1042
Amount: ₹4,85,000
```

System processes it.

### OCR

Extracts invoice information.

### Validation

Finds that the invoice is mathematically valid.

### Duplicate Detection

Finds a similar invoice from the same vendor.

### Anomaly Detection

Detects that:

```text
Current invoice = ₹4,85,000
Vendor historical average = ₹1,75,000
Deviation = +177%
```

### Risk Engine

Produces:

```text
Risk Score: 89
Risk Level: HIGH
```

### Explainability

Shows:

```text
+45% amount deviation
+20% duplicate similarity
+14% increased vendor frequency
+10% unusual submission timing
```

### Workflow

Invoice becomes:

```text
FLAGGED
```

Finance manager receives notification.

The AI Assistant can then answer:

> Why was INV-1042 flagged?

and explain the complete reasoning using actual database data.

---

# 33. RESPONSIVE DESIGN

The application must work on:

* Desktop
* Laptop
* Tablet
* Mobile

Use responsive layouts.

---

# 34. PROJECT CONFIGURATION

Frontend `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Backend `.env`:

```env
MONGODB_URI=your_mongodb_atlas_uri
DATABASE_NAME=financial_intelligence
JWT_SECRET=your_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

LLM_API_KEY=your_api_key
```

Provide `.env.example`.

Never commit `.env`.

---

# 35. REQUIREMENTS.TXT

Include appropriate versions for:

```text
fastapi
uvicorn
pymongo
pydantic
pydantic-settings
python-jose
passlib
bcrypt
python-multipart
pandas
numpy
scikit-learn
joblib
pymupdf
pytesseract
Pillow
python-dotenv
```

Add LLM SDK only if required.

---

# 36. FRONTEND DEPENDENCIES

Use:

```text
react
react-router-dom
axios
recharts
@mui/material
@mui/icons-material
```

Add other dependencies only when necessary.

---

# 37. TESTING

Implement backend tests for:

* Authentication
* Transaction creation
* Invoice validation
* Duplicate detection
* Anomaly detection
* Forecasting
* Budget recommendation
* Risk calculation

Test important frontend flows:

```text
Login
Dashboard loading
Invoice upload
Invoice approval
Anomaly filtering
Forecast display
AI assistant
Logout
```

---

# 38. README

Create a complete README containing:

## Project Overview

## Features

## Architecture

## Tech Stack

## Folder Structure

## MongoDB Atlas Setup

## Environment Variables

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Seed Data

Provide:

```bash
python seed.py
```

## API Documentation

Explain that Swagger is available at:

```text
/api/docs
```

## Demo Credentials

Provide demo credentials generated by the seed process.

## AI/ML Architecture

Explain:

* anomaly detection
* forecasting
* risk scoring
* budget optimization
* explainability
* financial assistant

---

# 39. DEVELOPMENT RULES

Follow these rules strictly:

1. Do not hardcode financial data in React components.
2. All data must come from FastAPI APIs.
3. Store persistent data in MongoDB Atlas.
4. Use Axios for API communication.
5. Use JWT for authentication.
6. Keep frontend and backend separate.
7. Use reusable React components.
8. Use modular FastAPI architecture.
9. Keep ML logic inside dedicated services/modules.
10. Do not place ML code directly inside API routes.
11. Do not expose secrets.
12. Add proper validation.
13. Add loading and error states.
14. Do not claim an anomaly is definitely fraud.
15. Every AI decision must have an explanation.
16. Every recommendation must show supporting evidence.
17. Avoid fake AI responses.
18. Use actual MongoDB data for dashboard calculations.
19. Use realistic seed data.
20. Make the application runnable locally without manual code modifications.

---

# 40. IMPLEMENTATION ORDER

Build the project in this order:

### Phase 1

Create:

* Backend structure
* React structure
* MongoDB Atlas connection
* Environment configuration
* Authentication

### Phase 2

Implement:

* Transactions
* Vendors
* Invoices
* Dashboard

### Phase 3

Implement:

* OCR
* Invoice extraction
* Invoice validation
* Duplicate detection

### Phase 4

Implement:

* Anomaly detection
* Risk scoring
* Vendor risk

### Phase 5

Implement:

* Cash-flow forecasting
* Budget optimization

### Phase 6

Implement:

* Approval workflow
* Notifications
* Audit logs

### Phase 7

Implement:

* AI Financial Assistant
* Explainable recommendations

### Phase 8

Implement:

* Seed/demo data
* Testing
* Error handling
* UI polish
* README
* Deployment configuration

---

# 41. FINAL UI PAGES

The finished application should contain:

```text
/login
/register

/dashboard

/transactions
/transactions/:id

/invoices
/invoices/upload
/invoices/:id

/vendors
/vendors/:id

/anomalies

/cash-flow

/budgets

/risk

/approvals

/ai-assistant

/notifications

/audit-logs

/settings
```

---

# 42. FINAL SUCCESS CRITERIA

The project is considered complete only when a user can:

1. Register/login.
2. Open the financial dashboard.
3. View real financial metrics from MongoDB Atlas.
4. Upload an invoice.
5. Extract invoice information automatically.
6. Validate the invoice.
7. Detect duplicate invoices.
8. Detect unusual transactions.
9. Calculate explainable financial risk.
10. View vendor risk.
11. View cash-flow forecasts.
12. View confidence intervals.
13. Receive budget recommendations.
14. Approve/reject invoices.
15. Receive financial risk notifications.
16. View audit logs.
17. Ask the AI Financial Assistant questions.
18. Receive answers based on actual database data.
19. See evidence behind AI answers.
20. See explanations behind anomaly/risk/recommendation scores.

The final result should feel like a real **AI Financial Operations SaaS platform**, not a college CRUD project.

Prioritize a polished working end-to-end MVP over implementing unnecessary features.

At every stage, ensure the application remains runnable.
