
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from model_utils import compute_rule_columns


def compute_fee_weight(months_unpaid):
    """Assign numeric weight based on overdue duration."""
    if months_unpaid >= 3:
        return 1.0
    elif months_unpaid == 2:
        return 0.7
    elif months_unpaid == 1:
        return 0.4
    else:
        return 0.0


def load_merge(att_path, scores_path, fees_path):
    att = pd.read_csv(att_path)
    scores = pd.read_csv(scores_path)
    fees = pd.read_csv(fees_path)

    
    fees["fee_weight"] = fees["outstanding_months"].apply(compute_fee_weight)

    df = att.merge(scores, on="student_id").merge(fees, on="student_id")
    
    
    if "avg_score" not in df.columns:
        df["avg_score"] = df[["test1","test2","test3"]].mean(axis=1)
    return df


def create_labels(df):
    df = compute_rule_columns(df)
    df["dropout_label"] = ((df["rule_score"] >= 0.6) | (df["rule_flag"] == 1)).astype(int)
    return df


def train_and_save(df, model_path="dropout_model.pkl"):
    features = ["attendance", "avg_score", "fee_weight", "rule_score"]
    X = df[features].fillna(0)
    y = df["dropout_label"]

    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.25, random_state=42
    )

    
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)
    calib = CalibratedClassifierCV(rf, cv=5, method="sigmoid")
    calib.fit(X_train, y_train)

    
    preds = calib.predict(X_test)
    print(classification_report(y_test, preds))

   
    joblib.dump(calib, model_path)
    print("Saved model to", model_path)


if __name__ == "__main__":
    df = load_merge("attendance.csv", "scores.csv", "fees.csv")
    df = create_labels(df)
    train_and_save(df)
