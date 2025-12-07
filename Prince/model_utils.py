import pandas as pd

def compute_rule_columns(df):
    """
    Compute rule-based columns for dropout risk with continuous weighting.
    Uses attendance, avg_score, and fee_weight.
    Returns df with 'rule_score' and 'rule_flag'.
    """

    
    def attendance_weight(att):
        """
        Continuous risk for attendance.
        90+% -> 0 risk, 40% -> 1 risk
        Linear scale in between
        """
        if att >= 90:
            return 0.0
        elif att <= 40:
            return 1.0
        else:
            return (90 - att) / 50  

    def score_weight(avg):
        """
        Continuous risk for average score.
        80+ -> 0 risk, 30 -> 1 risk
        Linear scale in between
        """
        if avg >= 80:
            return 0.0
        elif avg <= 30:
            return 1.0
        else:
            return (80 - avg) / 50 

    df["attendance_risk"] = df["attendance"].apply(attendance_weight)
    df["score_risk"] = df["avg_score"].apply(score_weight)
    df["fee_risk"] = df["fee_weight"] 

    
    df["rule_score"] = 0.4 * df["attendance_risk"] + 0.35 * df["score_risk"] + 0.25 * df["fee_risk"]

    df["rule_flag"] = (df["rule_score"] >= 0.6).astype(int)

    
    df.drop(columns=["attendance_risk", "score_risk", "fee_risk"], inplace=True)

    return df
