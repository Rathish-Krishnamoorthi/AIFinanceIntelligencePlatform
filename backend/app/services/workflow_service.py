def approval_status(status: str) -> bool:
    return status in {"APPROVED", "REJECTED"}
