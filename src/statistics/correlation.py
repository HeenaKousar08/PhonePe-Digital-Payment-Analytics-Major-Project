import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/master_dataset.csv")

numeric_df = df.select_dtypes(include="number")

corr = numeric_df.corr(method="pearson")

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap="coolwarm")

plt.title("Correlation Matrix")

plt.savefig(
    "reports/charts/correlation_heatmap.png",
    bbox_inches="tight"
)

plt.show()