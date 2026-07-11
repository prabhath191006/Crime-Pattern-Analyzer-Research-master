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

        threshold = train_counts.mean() * 1.5
        pred = set(train_counts[train_counts > threshold].index)

        top_n = max(1, int(len(test_counts) * 0.2))
        actual = set(test_counts.head(top_n).index)

        acc = (len(pred & actual) / len(actual)) * 100 if len(actual) else 0
        results.append({"Dataset": file, "Rule": round(acc, 2)})

pd.DataFrame(results).to_csv("rule_results.csv", index=False)