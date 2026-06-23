import pandas as pd
from scipy.stats import ttest_ind

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

state_totals = (
    df.groupby("state")["amount"]
    .sum()
    .sort_values()
)

bottom_states = state_totals.head(10).index
top_states = state_totals.tail(10).index

group1 = df[df["state"].isin(top_states)]["amount"]
group2 = df[df["state"].isin(bottom_states)]["amount"]

t_stat, p_value = ttest_ind(
    group1,
    group2
)

print("T Statistic =", t_stat)
print("P Value =", p_value)