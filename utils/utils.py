
def risk_level_chek(difficulty, importance):
    res = difficulty * 2 + importance
    if 0 < res <= 9:
        return "LOW"
    elif 10 <= res <= 17:
        return "MEDIUM"
    elif 18 <= res <= 24:
        return "HIGH"
    else:
        return "CRITICAL"
