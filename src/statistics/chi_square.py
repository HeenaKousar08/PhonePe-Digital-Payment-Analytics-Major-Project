import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

table = pd.crosstab(
    df["state"],
    df["category"]
)

chi2, p, dof, expected = chi2_contingency(table)

print("\nCHI SQUARE TEST")
print("Chi2 =", chi2)
print("P Value =", p)
print("DOF =", dof)