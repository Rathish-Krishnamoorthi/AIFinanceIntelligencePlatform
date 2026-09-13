ALLOWED_ROLES = {"SYSTEM_ADMIN", "FINANCE_MANAGER", "EMPLOYEE", "CFO",
                 "ADMIN", "ACCOUNTANT", "AUDITOR"}
ELEVATED_ROLES = {"SYSTEM_ADMIN", "ADMIN", "FINANCE_MANAGER"}


def normalize_role(role: str) -> str:
    return role if role in ALLOWED_ROLES else "EMPLOYEE"
