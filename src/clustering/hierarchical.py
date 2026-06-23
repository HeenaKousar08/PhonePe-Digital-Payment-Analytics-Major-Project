import pandas as pd
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

state_data = (
    df.groupby("state")
    [["count","amount"]]
    .sum()
)

linked = linkage(
    state_data,
    method="ward"
)

plt.figure(figsize=(12,8))

dendrogram(
    linked,
    labels=state_data.index,
    leaf_rotation=90
)

plt.title(
    "Hierarchical Clustering"
)

plt.tight_layout()

plt.savefig(
    "reports/charts/hierarchical_clustering.png"
)

plt.show()