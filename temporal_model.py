import pandas as pd
import os

folder = "Datasets"
results = []

for file in os.listdir(folder):
    if file.startswith("district_"):

        df = pd.read_csv(os.path.join(folder, file))

        df['Area'] = df['Latitude'].round(2).astype(str) + "_" + df['Longitude'].round(2).astype(str)
        df['Hour'] = pd.to_datetime(df['Date'], errors='coerce').dt.hour
        df = df.dropna(subset=['Hour'])

        df = df.sample(frac=1, random_state=42)
        split = int(0.7 * len(df))

        train = df[:split]
        test = df[split:]

        peak_hours = train['Hour'].value_counts().head(3).index
        train_filtered = train[train['Hour'].isin(peak_hours)]

        train_counts = train_filtered['Area'].value_counts()
        test_counts = test['Area'].value_counts()

        top_n = max(1, int(len(train_counts) * 0.2))

        pred = set(train_counts.head(top_n).index)
        actual = set(test_counts.head(top_n).index)

        acc = (len(pred & actual) / len(actual)) * 100 if len(actual) else 0
        results.append({"Dataset": file, "Temporal": round(acc, 2)})

pd.DataFrame(results).to_csv("temporal_results.csv", index=False)