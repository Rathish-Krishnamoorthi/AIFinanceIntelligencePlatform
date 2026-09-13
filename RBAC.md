Implement a complete **Role-Based Access Control (RBAC) system with separate dashboards and navigation views** for my FinSight AI financial intelligence platform.

## Project Context

FinSight AI is an AI-powered financial intelligence platform with modules for:

* Transactions
* Invoices
* Vendors
* Expenses
* Budgets
* Cash Flow Forecasting
* Fraud & Anomaly Detection
* Risk Analysis
* Approvals
* Reports
* AI Decision Assistant
* User Management
* Audit Logs
* System Settings

The application uses:

* React.js frontend
* FastAPI backend
* MongoDB Atlas
* JWT authentication
* REST APIs

Do not create separate React applications for each role. Use **one React application with role-based layouts, routes, navigation, and permissions**.

---

# 1. User Roles

Implement exactly these four primary roles:

### 1. Employee

Purpose:

Normal employee/user who manages their own financial activity.

Access:

* Dashboard
* My Transactions
* My Expenses
* My Budget
* My Cash Flow
* My Reports
* Limited AI Insights

Employees must only be able to access their own financial records.

---

### 2. Finance Manager

Purpose:

Handles day-to-day organizational financial operations.

Access:

* Dashboard
* Transactions
* Invoices
* Vendors
* Approvals
* Budgets
* Cash Flow
* Fraud Detection
* Risk Dashboard
* Reports
* AI Decision Assistant

Finance Managers can manage organizational financial records according to their permissions.

They should NOT have access to:

* User management
* Role management
* System settings

unless explicitly granted through permissions.

---

### 3. CFO

Purpose:

Executive-level financial oversight and decision-making.

Access:

* Executive Dashboard
* Financial Overview
* Transactions
* Invoices
* Vendors
* Approvals
* Budget Analytics
* Cash Flow Forecast
* Fraud & Anomaly Detection
* Vendor Risk
* AI Insights
* AI Decision Assistant
* Executive Reports
* Audit Logs (read-only)

The CFO should primarily see aggregated organization-wide financial intelligence rather than operational CRUD screens by default.

---

### 4. System Admin

Purpose:

Application/platform administration.

Access:

* Admin Dashboard
* Users
* Roles & Permissions
* Audit Logs
* System Monitoring
* System Settings

System Admin is responsible for technical/platform administration.

Do NOT automatically give System Admin financial editing privileges simply because they are an administrator.

---

# 2. Permission-Based RBAC

Do not implement RBAC using only role names.

Create a proper permission system.

Example permissions:

```text
dashboard.view

transactions.view
transactions.create
transactions.update
transactions.delete

invoices.view
invoices.create
invoices.update
invoices.delete
invoices.approve

vendors.view
vendors.create
vendors.update
vendors.delete

budgets.view
budgets.create
budgets.update
budgets.delete

cashflow.view

fraud.view
fraud.investigate

risk.view

reports.view
reports.export

ai.insights.view
ai.decision_assistant.use

approvals.view
approvals.create
approvals.approve
approvals.reject

users.view
users.create
users.update
users.disable

roles.view
roles.update

audit_logs.view

settings.view
settings.update
```

Roles should map to permissions.

---

# 3. Permission Matrix

Implement this initial permission matrix:

| Module                | Employee | Finance Manager | CFO          | System Admin |
| --------------------- | -------- | --------------- | ------------ | ------------ |
| Dashboard             | Own      | Full            | Executive    | Admin        |
| Transactions          | Own      | Full            | View         | No           |
| Expenses              | Own      | Full            | View         | No           |
| Invoices              | Own/View | Full            | View/Approve | No           |
| Vendors               | No       | Full            | View         | No           |
| Approvals             | No       | Manage          | Approve/View | No           |
| Budgets               | Own      | Manage          | Full         | No           |
| Cash Flow             | Own      | Full            | Full         | No           |
| Fraud Detection       | No       | Investigate     | Full         | No           |
| Risk Dashboard        | No       | View            | Full         | No           |
| Reports               | Own      | Full            | Executive    | No           |
| AI Insights           | Limited  | Full            | Advanced     | No           |
| AI Decision Assistant | Limited  | Full            | Advanced     | No           |
| Users                 | No       | No              | Limited/View | Full         |
| Roles                 | No       | No              | No           | Full         |
| Audit Logs            | No       | Limited         | View         | Full         |
| System Settings       | No       | No              | No           | Full         |

Use permission checks rather than hardcoding role checks throughout the application.

---

# 4. Authentication

Create a secure login system using JWT.

Login flow:

```text
User
 ↓
Login Page
 ↓
POST /api/auth/login
 ↓
Validate credentials
 ↓
Generate JWT
 ↓
Return:
    access_token
    user information
    role
    permissions
 ↓
React stores authentication state
 ↓
Redirect based on role
```

Example response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "user": {
    "id": "USR001",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "finance_manager",
    "permissions": [
      "dashboard.view",
      "transactions.view",
      "transactions.create",
      "invoices.view",
      "invoices.create",
      "vendors.view"
    ]
  }
}
```

Do not store passwords in plain text.

Use secure password hashing.

---

# 5. Login Page

Create a professional FinSight login page.

The login page should NOT allow users to freely select their role.

The role must come from the authenticated backend account.

Do NOT implement:

```text
Email
Password
Role dropdown
```

because users could attempt to select a privileged role.

Instead:

```text
Email
Password
        ↓
Login
        ↓
Backend determines role
        ↓
Correct dashboard
```

---

# 6. Role-Based Redirect

After successful authentication:

```text
Employee
    ↓
/employee/dashboard

Finance Manager
    ↓
/finance/dashboard

CFO
    ↓
/cfo/dashboard

System Admin
    ↓
/admin/dashboard
```

If an authenticated user manually enters another dashboard URL, prevent unauthorized access.

Example:

```text
Employee → /admin/dashboard
```

must result in:

```text
403 Forbidden
```

or redirect to the employee dashboard.

---

# 7. Separate Frontend Views

Create separate layouts for each role while keeping the same React application.

## Employee Layout

Route:

```text
/employee/*
```

Sidebar:

```text
FinSight

Dashboard
Transactions
Expenses
Budget
Cash Flow
Reports

Profile
Logout
```

Dashboard should show:

* Personal income
* Personal expenses
* Remaining budget
* Personal cash flow
* Recent transactions
* Spending categories
* Limited AI insights

---

## Finance Manager Layout

Route:

```text
/finance/*
```

Sidebar:

```text
FinSight

Dashboard
Transactions
Invoices
Vendors
Approvals
Budgets
Cash Flow
Fraud Detection
Risk
Reports
AI Assistant

Profile
Logout
```

Dashboard should show:

* Total revenue
* Total expenses
* Outstanding invoices
* Pending approvals
* Vendor risk
* Fraud alerts
* Budget utilization
* Cash-flow forecast

---

## CFO Layout

Route:

```text
/cfo/*
```

Sidebar:

```text
FinSight

Executive Dashboard
Financial Overview
Transactions
Invoices
Vendors
Budget Analytics
Cash Flow
Fraud & Risk
AI Insights
AI Decision Assistant
Reports
Audit Logs

Profile
Logout
```

The CFO dashboard should focus on:

* Revenue
* Expenses
* Profit/cash position
* Outstanding liabilities
* Budget utilization
* Cash-flow forecast
* High-risk vendors
* Fraud/anomaly alerts
* AI-generated recommendations

Use executive-level charts and KPIs.

---

## System Admin Layout

Route:

```text
/admin/*
```

Sidebar:

```text
FinSight Admin

Admin Dashboard
Users
Roles & Permissions
Audit Logs
System Monitoring
Settings

Profile
Logout
```

Admin dashboard should show:

* Total users
* Active users
* Users by role
* Recent logins
* Failed login attempts
* API/system status
* Recent audit events

---

# 8. Frontend Route Protection

Create reusable route protection.

For example:

```text
ProtectedRoute
RoleRoute
PermissionRoute
```

Conceptually:

```text
ProtectedRoute
    ↓
Is authenticated?
    ↓
No → /login
Yes
    ↓
Check permission
    ↓
Allowed → render page
Denied → 403 page
```

Example:

```text
<PermissionRoute permission="vendors.view">
    <VendorPage />
</PermissionRoute>
```

Do not duplicate permission logic across every component.

---

# 9. Backend Authorization

Frontend route protection is NOT sufficient.

Every protected FastAPI endpoint must validate:

1. JWT
2. User
3. Role
4. Permission
5. Resource ownership where applicable

Example:

```text
GET /api/vendors
        ↓
JWT validation
        ↓
Current user
        ↓
vendors.view permission
        ↓
Allow / Reject
```

Return:

```text
401 Unauthorized
```

for unauthenticated users.

Return:

```text
403 Forbidden
```

for authenticated users without sufficient permissions.

---

# 10. Ownership Rules

Employees must only access their own data.

For example:

```text
Employee USR001
```

should only see:

```text
transactions.user_id = USR001
```

They must not be able to modify the API request to:

```text
user_id = USR002
```

and retrieve another user's data.

The backend must enforce ownership.

Do not rely on frontend filtering for security.

---

# 11. MongoDB User Model

Create/update the user model to include:

```json
{
  "user_id": "USR001",
  "name": "John Doe",
  "email": "john@example.com",
  "password_hash": "...",
  "role": "employee",
  "permissions": [],
  "is_active": true,
  "created_at": "...",
  "updated_at": "..."
}
```

Prefer deriving permissions from the role rather than allowing arbitrary privilege escalation by normal users.

---

# 12. Organization Support

Design the system so it can support multiple organizations in the future.

Add:

```text
organization_id
```

to users and relevant financial entities.

For example:

```text
User
 └── organization_id

Vendor
 └── organization_id

Invoice
 └── organization_id

Transaction
 └── organization_id
```

Finance Managers and CFOs should only access data belonging to their organization.

System Admin can manage organizations if that capability is implemented.

---

# 13. Audit Logging

Create an audit log for security-sensitive actions.

Record:

```text
user_id
role
action
module
resource_id
timestamp
IP/address if available
result
```

Examples:

```text
CFO approved invoice INV001

Finance Manager created vendor V001

System Admin disabled user USR009

Employee attempted unauthorized access to /admin/users
```

Do not log passwords, JWT tokens, or other secrets.

---

# 14. Unauthorized Page

Create a professional `403 Forbidden` page.

Example:

```text
Access Restricted

You don't have permission to access this module.

Your current role:
Employee

Required permission:
vendors.view

Return to Dashboard
```

---

# 15. User Experience

Each role should feel like it has its own application.

Do NOT simply hide a few buttons from one common dashboard.

Create genuinely different:

* Sidebar
* Dashboard KPIs
* Navigation
* Module visibility
* Data scope
* Actions
* Charts
* AI insights

while sharing common reusable components.

Use a professional financial SaaS design.

---

# 16. Security Requirements

Implement:

* JWT authentication
* Password hashing
* Token expiration
* Protected API routes
* Role-based authorization
* Permission-based authorization
* Resource ownership checks
* Organization-level isolation
* Backend authorization
* Frontend route guards
* Audit logging
* Secure logout
* No password storage in frontend
* No role selection during login
* No sensitive information in frontend local storage unless necessary
* Proper 401/403 handling

Never trust:

```text
role
user_id
organization_id
```

when supplied directly by the frontend.

Derive them from the authenticated JWT/user context wherever possible.

---

# 17. Required Folder Structure

Use a clean architecture.

Frontend example:

```text
src/
├── auth/
│   ├── AuthContext
│   ├── ProtectedRoute
│   ├── PermissionRoute
│   └── authService
│
├── layouts/
│   ├── EmployeeLayout
│   ├── FinanceLayout
│   ├── CFOLayout
│   └── AdminLayout
│
├── pages/
│   ├── employee/
│   ├── finance/
│   ├── cfo/
│   └── admin/
│
├── components/
├── services/
├── hooks/
├── utils/
└── routes/
```

Backend example:

```text
app/
├── models/
│   ├── user.py
│   ├── role.py
│   ├── permission.py
│   └── audit_log.py
│
├── schemas/
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── transactions.py
│   ├── invoices.py
│   ├── vendors.py
│   ├── budgets.py
│   ├── reports.py
│   └── admin.py
│
├── services/
│
├── core/
│   ├── security.py
│   ├── permissions.py
│   └── config.py
│
└── main.py
```

Adapt this structure to my existing FinSight codebase instead of unnecessarily replacing working code.

---

# 18. Seed Demo Users

Create development/demo accounts for testing each role.

Example:

```text
employee@finsight.demo
finance@finsight.demo
cfo@finsight.demo
admin@finsight.demo
```

Use secure development-only passwords and clearly mark them as demo accounts.

Do not expose these credentials in production.

---

# 19. Testing Requirements

Test all four roles.

### Employee

Verify:

```text
Login → Employee Dashboard
Employee → Own Transactions ✅
Employee → Own Expenses ✅
Employee → Vendors ❌
Employee → Admin ❌
Employee → Other user's transaction ❌
```

### Finance Manager

Verify:

```text
Login → Finance Dashboard
Transactions ✅
Invoices ✅
Vendors ✅
Approvals ✅
Fraud Detection ✅
Users ❌
System Settings ❌
```

### CFO

Verify:

```text
Login → CFO Dashboard
Financial Overview ✅
Invoices ✅
Vendors ✅
Risk ✅
Fraud Detection ✅
AI Assistant ✅
Executive Reports ✅
System Settings ❌
```

### System Admin

Verify:

```text
Login → Admin Dashboard
Users ✅
Roles ✅
Audit Logs ✅
System Settings ✅
Financial editing ❌ unless explicitly granted
```

Also test direct API requests using unauthorized JWT tokens and verify that the backend returns `403`.

---

# 20. Final Goal

The finished FinSight application must provide this experience:

```text
                         LOGIN
                           │
                           ↓
                     JWT AUTHENTICATION
                           │
                           ↓
                         RBAC
                           │
       ┌───────────────────┼───────────────────┐
       ↓                   ↓                   ↓
   EMPLOYEE          FINANCE MANAGER          CFO
       │                   │                   │
       ↓                   ↓                   ↓
Personal Finance      Operations          Executive
Dashboard             Dashboard           Dashboard
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                           +
                    SYSTEM ADMIN
                           │
                           ↓
                  Platform Management
```

The application should be **secure by default**, with authorization enforced at both frontend and backend levels.

Do not break existing FinSight modules.

First inspect the existing project structure, authentication system, models, routes, and frontend routing. Then integrate this RBAC architecture into the existing application.

After implementation, provide:

1. Files created
2. Files modified
3. Backend API changes
4. Frontend route changes
5. MongoDB schema changes
6. Permission matrix
7. Demo accounts
8. How to test each role
9. Any existing code that had to be changed or migrated
10. Any security issues or limitations that remain
