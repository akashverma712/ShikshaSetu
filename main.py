import io
import pandas as pd
import joblib
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from model_utils import compute_rule_columns

app = FastAPI(title="Dropout Prediction System - SIH")


ml_model = joblib.load("dropout_model.pkl")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def compute_fee_weight(months_unpaid):
    if months_unpaid >= 3:
        return 1.0
    elif months_unpaid == 2:
        return 0.7
    elif months_unpaid == 1:
        return 0.4
    else:
        return 0.0


def get_zone(final_score):
    """
    Zone thresholds updated for smoother continuous rule_score.
    """
    if final_score >= 0.55:
        return "Red Zone"
    elif final_score >= 0.30:
        return "Yellow Zone"
    else:
        return "Green Zone"

@app.post("/predict/batch")
async def batch_predict(
    attendance_csv: UploadFile = File(...),
    exam_csv: UploadFile = File(...),
    fees_csv: UploadFile = File(...)
):
    try:
        df_att = pd.read_csv(io.BytesIO(await attendance_csv.read()))
        df_exam = pd.read_csv(io.BytesIO(await exam_csv.read()))
        df_fees = pd.read_csv(io.BytesIO(await fees_csv.read()))


        df_fees["fee_weight"] = df_fees["outstanding_months"].apply(compute_fee_weight)


        df = df_att.merge(df_exam, on="student_id", how="left")
        df = df.merge(df_fees, on="student_id", how="left")


        if "avg_score" not in df.columns:
            df["avg_score"] = df[["test1", "test2", "test3"]].mean(axis=1)

        df = compute_rule_columns(df)

        ml_features = ["attendance", "avg_score", "fee_weight", "rule_score"]
        df["ml_pred"] = ml_model.predict_proba(df[ml_features].fillna(0))[:, 1]
        df["final_score"] = (df["ml_pred"] + df["rule_score"]) / 2


        df["risk_zone"] = df["final_score"].apply(get_zone)

    
        return {
            "total_records": len(df),
            "preview": df.head(10).to_dict(orient="records"),
            "full_data": df.to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
