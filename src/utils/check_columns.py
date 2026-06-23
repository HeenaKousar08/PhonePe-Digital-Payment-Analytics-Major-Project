import pandas as pd

files = [
    "data/raw/aggregated_transaction.csv",
    "data/raw/map_transaction.csv",
    "data/raw/top_transaction_pincode.csv"
]

for file in files:
    print("\n" + "="*70)
    print("FILE:", file)
    print("="*70)

    df = pd.read_csv(file)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nShape:")
    print(df.shape)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nData Types:")
    print(df.dtypes)