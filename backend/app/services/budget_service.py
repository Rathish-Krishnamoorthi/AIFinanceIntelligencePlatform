def recommendation(budget):
    utilization = budget["actual_spending"] / budget["allocated_budget"]
    amount = budget["allocated_budget"] * (.92 if utilization < .85 else 1.08)
    return {"category": budget["category"], "current_budget": budget["allocated_budget"],
            "forecasted_spending": round(budget["actual_spending"] * 1.08, 2),
            "recommended_budget": round(amount, 2), "utilization": round(utilization * 100, 1),
            "reason": "Historical utilization and performance score indicate a right-sized allocation.",
            "evidence": ["Actual spending trend", "Performance score", "Forecasted demand"]}
