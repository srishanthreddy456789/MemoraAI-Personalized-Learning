import pandas as pd
import numpy as np
import os

np.random.seed(42)

N = 1000  # ← increase this anytime

topics = [
    "Neural Networks",
    "DBMS",
    "Operating Systems",
    "Machine Learning",
    "Data Structures"
]

data = []

for i in range(N):
    last_studied_days = np.random.randint(0, 15)
    quiz_score = np.round(np.random.uniform(0.3, 0.95), 2)
    revision_count = np.random.randint(0, 5)

    forgotten = int(
        (last_studied_days > 7 and quiz_score < 0.6) or
        (revision_count == 0 and quiz_score < 0.5)
    )

    data.append([
        i,
        np.random.choice(topics),
        last_studied_days,
        quiz_score,
        revision_count,
        forgotten
    ])

df = pd.DataFrame(
    data,
    columns=[
        "student_id",
        "topic",
        "last_studied_days",
        "quiz_score",
        "revision_count",
        "forgotten"
    ]
)

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/training_data.csv", index=False)

print("✅ Generated dataset with", len(df), "rows")