import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv(
    "data/raw/aggregated_transaction.csv"
)

yearly = (
    df.groupby("year")["amount"]
    .sum()
)

model = ARIMA(
    yearly,
    order=(1,1,1)
)

model_fit = model.fit()

forecast = model_fit.forecast(
    steps=5
)

print("\nForecasted Amounts")

for year,value in zip(
    range(yearly.index.max()+1,
          yearly.index.max()+6),
    forecast
):
    print(year, round(value,2))

plt.figure(figsize=(10,5))

plt.plot(
    yearly.index,
    yearly.values,
    label="Historical"
)

future_years = range(
    yearly.index.max()+1,
    yearly.index.max()+6
)

plt.plot(
    future_years,
    forecast,
    marker="o",
    label="Forecast"
)

plt.legend()

plt.title(
    "PhonePe Transaction Forecast"
)

plt.savefig(
    "reports/charts/arima_forecast.png"
)

plt.show()