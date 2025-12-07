import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle


attendance_df = pd.read_csv("attendance.csv")
fee_df = pd.read_csv("fee_status.csv")
marks_df = pd.read_csv("marks.csv")  


data = attendance_df.merge(fee_df, on="student_id").merge(marks_df, on="student_id")


data['score_drop'] = data['last_score'] - data['current_score']
data['fee_pending'] = data['fee_status'].apply(lambda x: 1 if str(x).lower() == 'pending' else 0)
data['num_failed'] = data['num_failed'].fillna(0)

X = data[['attendance', 'score_drop', 'fee_pending', 'num_failed']]
y = data['is_dropout']   

model = RandomForestClassifier()
model.fit(X, y)


with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully using THREE CSV files!")
