import pandas as pd
from scipy.stats import f_oneway

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

top_states = (
    df.groupby("state")["amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

groups = []

for state in top_states:
    groups.append(
        df[df["state"] == state]["amount"]
    )

f_stat, p_value = f_oneway(*groups)

print("\nANOVA TEST")
print("F Statistic =", round(f_stat,4))
print("P Value =", p_value)

if p_value < 0.05:
    print("Significant difference exists.")
else:
    print("No significant difference.")