from pydantic import BaseModel, Field


class BudgetCreate(BaseModel):
    category: str
    allocated_budget: float = Field(gt=0)
    actual_spending: float = Field(ge=0)
    business_priority: int = Field(ge=0, le=100)
    performance_score: int = Field(ge=0, le=100)
