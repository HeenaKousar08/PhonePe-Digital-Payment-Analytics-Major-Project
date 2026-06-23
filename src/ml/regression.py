import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

X = df[
    ["year","quarter","count"]
]

y = df["amount"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

model.fit(X_train,y_train)

pred = model.predict(X_test)

print("\nREGRESSION RESULTS")
print("R² =", round(
    r2_score(y_test,pred),4
))