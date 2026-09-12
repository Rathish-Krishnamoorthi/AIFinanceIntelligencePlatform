ALLOWED_ROLES = {"ADMIN", "FINANCE_MANAGER", "ACCOUNTANT", "AUDITOR"}


def normalize_role(role: str) -> str:
    return role if role in ALLOWED_ROLES else "ACCOUNTANT"
