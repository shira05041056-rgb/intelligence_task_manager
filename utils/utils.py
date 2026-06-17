
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
    
def chek_rank(rank):
    ranks = ["Low", "Junior", "Junior", "Commander"]
    if rank not in ranks:
        return False
    return True

def chek_difficulty_and_importance(difficulty, importance):
    if 0 > difficulty and importance  < 11:
        return True
    return False
