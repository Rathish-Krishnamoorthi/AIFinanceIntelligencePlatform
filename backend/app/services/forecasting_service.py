def forecast_points(horizon=90):
    return [{"date": f"Day {i}", "predicted_cash_balance": round(880000 + i * 2500, 2),
             "lower": round(830000 + i * 1800, 2), "upper": round(930000 + i * 3200, 2)}
            for i in range(1, horizon + 1)]
