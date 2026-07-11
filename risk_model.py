import pandas as pd
import os

folder = "Datasets"
results = []

for file in os.listdir(folder):
    if file.startswith("district_"):

        df = pd.read_csv(os.path.join(folder, file))

        df['Area'] = df['Latitude'].round(2).astype(str) + "_" + df['Longitude'].round(2).astype(str)

        df = df.sample(frac=1, random_state=42)
        split = int(0.7 * len(df))

        train = df[:split]
        test = df[split:]

        train_counts = train['Area'].value_counts()
        test_counts = test['Area'].value_counts()

        risk = train_counts * 1.2
        pred = set(risk.sort_values(ascending=False).head(int(len(risk)*0.2)).index)

        actual = set(test_counts.head(int(len(test_counts)*0.2)).index)

        acc = (len(pred & actual) / len(actual)) * 100 if len(actual) else 0
        results.append({"Dataset": file, "Risk": round(acc, 2)})

pd.DataFrame(results).to_csv("risk_results.csv", index=False)