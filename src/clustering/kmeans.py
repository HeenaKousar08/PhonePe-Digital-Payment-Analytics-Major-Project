import pandas as pd

from sklearn.cluster import KMeans

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

state_data = (
    df.groupby("state")
    [["count","amount"]]
    .sum()
)

model = KMeans(
    n_clusters=3,
    random_state=42
)

state_data["cluster"] = (
    model.fit_predict(state_data)
)

print(
    state_data.head()
)

state_data.to_csv(
    "reports/model_results/state_clusters.csv"
)