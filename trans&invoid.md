### Transaction Module

Build a complete financial transaction management module.

Features:

* Add, edit, view and filter transactions.
* Fields: transaction ID, date, type (income/expense), category, amount, currency, vendor, payment method, description and status.
* Automatically calculate totals and update dashboard metrics.
* Detect unusual transactions using the anomaly detection model.
* Generate a risk score with clear reasons.
* Support search, filtering, sorting and pagination.
* Store all transactions in MongoDB Atlas.
* Maintain audit logs for important actions.
* Enforce RBAC:

  * ADMIN: full access
  * FINANCE_MANAGER: create/update/view
  * ACCOUNTANT: create/update/view
  * AUDITOR: view only

### Invoice Module

Build an intelligent invoice processing and management module.

Workflow:

**Upload Invoice → OCR/Extraction → Validation → Duplicate Check → Anomaly Detection → Risk Score → Approval → Payment**

Features:

* Upload PDF/JPG/PNG invoices.
* Extract invoice number, vendor, date, due date, subtotal, tax, discount, total, currency and line items.
* Show extracted data for user verification/editing.
* Validate invoice calculations, dates, vendor and required fields.
* Detect duplicate invoices.
* Compare invoice amount with historical vendor transactions.
* Generate anomaly/risk score with explainable reasons.
* Assign status:
  `UPLOADED → PROCESSING → VALIDATED → PENDING_APPROVAL → APPROVED/REJECTED → PAID`
* Provide approval/rejection workflow.
* Store original invoice metadata, extracted data, validation results and risk assessment in MongoDB.
* Create audit logs for upload, modification, approval and rejection.
* Enforce RBAC:

  * ADMIN: full access
  * FINANCE_MANAGER: process, approve/reject
  * ACCOUNTANT: upload, process, submit for approval
  * AUDITOR: view and audit only

### Integration

When an invoice is approved, automatically create/update the related **Accounts Payable transaction**, update dashboard metrics and cash-flow projections, and notify the relevant users.

All AI/ML decisions must display **why the invoice or transaction was flagged**, rather than simply showing a score.
