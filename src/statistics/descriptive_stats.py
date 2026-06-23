import pandas as pd
from scipy.stats import skew, kurtosis

df = pd.read_csv("data/processed/master_dataset.csv")

numeric_cols = df.select_dtypes(include="number").columns

results = []

for col in numeric_cols:
    results.append({
        "Variable": col,
        "Mean": df[col].mean(),
        "Median": df[col].median(),
        "Std_Dev": df[col].std(),
        "Variance": df[col].var(),
        "Skewness": skew(df[col]),
        "Kurtosis": kurtosis(df[col])
    })

stats_df = pd.DataFrame(results)

stats_df.to_csv(
    "reports/statistical_results/descriptive_statistics.csv",
    index=False
)

print(stats_df)