from enum import Enum


class UserRole(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    CFO = "CFO"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    # Legacy values are retained so existing accounts continue to authenticate.
    ADMIN = "ADMIN"
    FINANCE_MANAGER = "FINANCE_MANAGER"
    ACCOUNTANT = "ACCOUNTANT"
    AUDITOR = "AUDITOR"


class Permission(str, Enum):
    DASHBOARD_VIEW = "DASHBOARD_VIEW"
    TRANSACTION_VIEW = "TRANSACTION_VIEW"
    TRANSACTION_CREATE = "TRANSACTION_CREATE"
    TRANSACTION_UPDATE = "TRANSACTION_UPDATE"
    TRANSACTION_DELETE = "TRANSACTION_DELETE"
    INVOICE_VIEW = "INVOICE_VIEW"
    INVOICE_UPLOAD = "INVOICE_UPLOAD"
    INVOICE_PROCESS = "INVOICE_PROCESS"
    INVOICE_UPDATE = "INVOICE_UPDATE"
    INVOICE_APPROVE = "INVOICE_APPROVE"
    INVOICE_REJECT = "INVOICE_REJECT"
    INVOICE_PAYMENT = "INVOICE_PAYMENT"
    VENDOR_VIEW = "VENDOR_VIEW"
    VENDOR_CREATE = "VENDOR_CREATE"
    VENDOR_UPDATE = "VENDOR_UPDATE"
    VENDOR_DELETE = "VENDOR_DELETE"
    ANOMALY_VIEW = "ANOMALY_VIEW"
    ANOMALY_ANALYZE = "ANOMALY_ANALYZE"
    FORECAST_VIEW = "FORECAST_VIEW"
    FORECAST_GENERATE = "FORECAST_GENERATE"
    BUDGET_VIEW = "BUDGET_VIEW"
    BUDGET_CREATE = "BUDGET_CREATE"
    BUDGET_UPDATE = "BUDGET_UPDATE"
    BUDGET_APPROVE = "BUDGET_APPROVE"
    RISK_VIEW = "RISK_VIEW"
    ASSISTANT_USE = "ASSISTANT_USE"
    ASSISTANT_EXECUTE_ACTION = "ASSISTANT_EXECUTE_ACTION"
    APPROVAL_VIEW = "APPROVAL_VIEW"
    APPROVAL_APPROVE = "APPROVAL_APPROVE"
    APPROVAL_REJECT = "APPROVAL_REJECT"
    NOTIFICATION_VIEW = "NOTIFICATION_VIEW"
    AUDIT_VIEW = "AUDIT_VIEW"
    USER_VIEW = "USER_VIEW"
    USER_CREATE = "USER_CREATE"
    USER_UPDATE = "USER_UPDATE"
    USER_DELETE = "USER_DELETE"
    USER_ROLE_UPDATE = "USER_ROLE_UPDATE"
    SYSTEM_SETTINGS_VIEW = "SYSTEM_SETTINGS_VIEW"
    SYSTEM_SETTINGS_UPDATE = "SYSTEM_SETTINGS_UPDATE"


def _permissions(*names: Permission) -> set[str]:
    return {item.value for item in names}


ROLE_PERMISSIONS: dict[UserRole, set[str]] = {
    UserRole.SYSTEM_ADMIN: _permissions(
        Permission.DASHBOARD_VIEW, Permission.USER_VIEW, Permission.USER_CREATE,
        Permission.USER_UPDATE, Permission.USER_DELETE, Permission.USER_ROLE_UPDATE,
        Permission.AUDIT_VIEW, Permission.SYSTEM_SETTINGS_VIEW, Permission.SYSTEM_SETTINGS_UPDATE,
    ),
    UserRole.ADMIN: _permissions(
        Permission.DASHBOARD_VIEW, Permission.USER_VIEW, Permission.USER_CREATE,
        Permission.USER_UPDATE, Permission.USER_DELETE, Permission.USER_ROLE_UPDATE,
        Permission.AUDIT_VIEW, Permission.SYSTEM_SETTINGS_VIEW, Permission.SYSTEM_SETTINGS_UPDATE,
    ),
    UserRole.FINANCE_MANAGER: _permissions(
        Permission.DASHBOARD_VIEW, Permission.TRANSACTION_VIEW, Permission.TRANSACTION_CREATE,
        Permission.TRANSACTION_UPDATE, Permission.INVOICE_VIEW, Permission.INVOICE_UPLOAD,
        Permission.INVOICE_PROCESS, Permission.INVOICE_UPDATE, Permission.INVOICE_APPROVE,
        Permission.INVOICE_REJECT, Permission.INVOICE_PAYMENT, Permission.VENDOR_VIEW, Permission.VENDOR_CREATE,
        Permission.VENDOR_UPDATE, Permission.ANOMALY_VIEW, Permission.ANOMALY_ANALYZE,
        Permission.FORECAST_VIEW, Permission.FORECAST_GENERATE, Permission.BUDGET_VIEW,
        Permission.BUDGET_CREATE, Permission.BUDGET_UPDATE, Permission.BUDGET_APPROVE,
        Permission.RISK_VIEW, Permission.ASSISTANT_USE, Permission.APPROVAL_VIEW,
        Permission.APPROVAL_APPROVE, Permission.APPROVAL_REJECT, Permission.NOTIFICATION_VIEW,
        Permission.AUDIT_VIEW, Permission.USER_VIEW,
    ),
    UserRole.EMPLOYEE: _permissions(
        Permission.DASHBOARD_VIEW, Permission.TRANSACTION_VIEW, Permission.TRANSACTION_CREATE,
        Permission.TRANSACTION_UPDATE, Permission.ANOMALY_VIEW, Permission.FORECAST_VIEW,
        Permission.BUDGET_VIEW, Permission.ASSISTANT_USE, Permission.NOTIFICATION_VIEW,
    ),
    UserRole.ACCOUNTANT: _permissions(
        Permission.DASHBOARD_VIEW, Permission.TRANSACTION_VIEW, Permission.TRANSACTION_CREATE,
        Permission.TRANSACTION_UPDATE, Permission.INVOICE_VIEW, Permission.INVOICE_UPLOAD,
        Permission.INVOICE_PROCESS, Permission.ANOMALY_VIEW, Permission.FORECAST_VIEW,
        Permission.BUDGET_VIEW, Permission.ASSISTANT_USE, Permission.NOTIFICATION_VIEW,
    ),
    UserRole.CFO: _permissions(
        Permission.DASHBOARD_VIEW, Permission.TRANSACTION_VIEW, Permission.INVOICE_VIEW,
        Permission.INVOICE_APPROVE, Permission.INVOICE_REJECT,
        Permission.VENDOR_VIEW, Permission.ANOMALY_VIEW, Permission.FORECAST_VIEW,
        Permission.BUDGET_VIEW, Permission.RISK_VIEW, Permission.ASSISTANT_USE,
        Permission.APPROVAL_VIEW, Permission.NOTIFICATION_VIEW, Permission.AUDIT_VIEW,
    ),
    UserRole.AUDITOR: _permissions(
        Permission.DASHBOARD_VIEW, Permission.TRANSACTION_VIEW, Permission.INVOICE_VIEW,
        Permission.VENDOR_VIEW, Permission.ANOMALY_VIEW, Permission.FORECAST_VIEW,
        Permission.BUDGET_VIEW, Permission.RISK_VIEW, Permission.ASSISTANT_USE,
        Permission.APPROVAL_VIEW, Permission.NOTIFICATION_VIEW, Permission.AUDIT_VIEW,
    ),
}


ROLE_ALIASES = {
    "ACCOUNTANT": UserRole.EMPLOYEE,
    "AUDITOR": UserRole.CFO,
    "ADMIN": UserRole.SYSTEM_ADMIN,
}


def canonical_role(role: str | UserRole) -> UserRole | None:
    if isinstance(role, UserRole):
        return role
    if role in ROLE_ALIASES:
        return ROLE_ALIASES[role]
    try:
        return UserRole(role)
    except ValueError:
        return None


def permissions_for_role(role: str | UserRole) -> set[str]:
    canonical = canonical_role(role)
    return ROLE_PERMISSIONS.get(canonical, set()) if canonical else set()
