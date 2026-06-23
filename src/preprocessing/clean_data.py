import pandas as pd
import os

# Paths
RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

# Load datasets
agg_txn = pd.read_csv(f"{RAW_PATH}/aggregated_transaction.csv")
map_txn = pd.read_csv(f"{RAW_PATH}/map_transaction.csv")
top_txn = pd.read_csv(f"{RAW_PATH}/top_transaction_pincode.csv")

print("Aggregated Transaction Shape:", agg_txn.shape)
print("Map Transaction Shape:", map_txn.shape)
print("Top Transaction Shape:", top_txn.shape)

# Clean column names
for df in [agg_txn, map_txn, top_txn]:
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
    )

# Remove duplicates
agg_txn.drop_duplicates(inplace=True)
map_txn.drop_duplicates(inplace=True)
top_txn.drop_duplicates(inplace=True)

# Fill missing values
agg_txn.fillna(0, inplace=True)
map_txn.fillna(0, inplace=True)
top_txn.fillna(0, inplace=True)

# Save cleaned files
agg_txn.to_csv(f"{PROCESSED_PATH}/aggregated_transaction_clean.csv", index=False)
map_txn.to_csv(f"{PROCESSED_PATH}/map_transaction_clean.csv", index=False)
top_txn.to_csv(f"{PROCESSED_PATH}/top_transaction_clean.csv", index=False)

# Create master dataset
master_df = pd.concat(
    [agg_txn, map_txn, top_txn],
    ignore_index=True,
    sort=False
)

master_df.to_csv(
    f"{PROCESSED_PATH}/master_dataset.csv",
    index=False
)

print("\nMaster Dataset Created Successfully")
print(master_df.shape)