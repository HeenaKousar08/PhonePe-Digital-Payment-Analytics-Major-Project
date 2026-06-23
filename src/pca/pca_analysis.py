import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

features = df[
    ["year","quarter","count","amount"]
]

scaled = StandardScaler().fit_transform(
    features
)

pca = PCA()

pca.fit(scaled)

print("\nExplained Variance Ratio")

for i,v in enumerate(
    pca.explained_variance_ratio_
):
    print(
        f"PC{i+1}: {round(v*100,2)}%"
    )