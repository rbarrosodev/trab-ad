from datetime import datetime
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import json
import pandas as pd
import warnings


# Load JSON data
throughputs_data = json.load(open("data/throughputs_normalized.json"))

# Prepare data for analysis
timestamps = [datetime.fromtimestamp(data["ts"]) for data in throughputs_data]
values = [data["val"] for data in throughputs_data]

# Create a DataFrame from the data
df = pd.DataFrame(values, index=timestamps)
df.columns = ["val"]

# Resample data to daily frequency and handle missing values
daily = df.resample("d").sum()

# Calculate the median value for data normalization
mediana = daily.median()["val"]

# Replace values close to zero with the median (for normalization)
daily["val"] = daily["val"].apply(lambda x: mediana if 0.2 > x > -0.2 else x)

# Ensure the 'val' column is of a compatible dtype
daily["val"] = daily["val"].astype(float)

# ETS Decomposition (Exponential Smoothing)
result_add = seasonal_decompose(daily["val"], model="additive", extrapolate_trend="freq")
result_mul = seasonal_decompose(daily["val"], model="multiplicative", extrapolate_trend="freq")

# Plot additive decomposition
plt.rcParams.update({"figure.figsize": (15, 10)})
result_add.plot().suptitle("Aditivo", x=0.2, fontweight="bold")
plt.show()

# Plot multiplicative decomposition
result_mul.plot().suptitle("Multiplicativo", x=0.2, fontweight="bold")
plt.show()

# Plot ACF (Auto-Correlation Function)
fig, ax = plt.subplots(figsize=(10, 5))
plot_acf(df["val"], ax=ax)
ax.set_ylim(-1.1, 1.1)  # Set y-axis limit for ACF
plt.title("Autocorrelation Function (ACF)")
plt.show()
plt.close()

# Plot PACF (Partial Auto-Correlation Function)
fig, ax = plt.subplots(figsize=(10, 5))
plot_pacf(df["val"], ax=ax)
ax.set_ylim(-1.1, 1.1)  # Set y-axis limit for PACF
plt.title("Partial Autocorrelation Function (PACF)")
plt.show()
plt.close()

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Automatically select ARIMA model parameters using stepwise search
stepwise_fit = auto_arima(
    daily["val"],
    start_p=1,
    start_q=1,
    max_p=1,
    max_q=1,
    m=12,
    start_P=0,
    seasonal=True,
    d=None,
    D=1,
    trace=True,
    error_action="ignore",
    suppress_warnings=True,
    stepwise=True
)

# Print summary of the best fitting ARIMA model found
stepwise_fit.summary()

# Split data into training and testing sets
train = daily.iloc[:len(daily) - 12]
test = daily.iloc[len(daily) - 12:]

# Fit SARIMA model to training data (using manually chosen parameters), Best forecast uses order (1, 0, 1) and seasonal_order (0, 1, 1, 12)
model = SARIMAX(
    train["val"],
    order=(1, 0, 1),
    seasonal_order=(0, 1, 1, 12)
)

# Fit the model and print summary
result = model.fit()
result.summary()

# Make predictions on the test set and plot against actual values
start = len(train)
end = len(train) + len(test) - 1
predictions = result.predict(start, end, typ="levels").rename("Predictions")

test["val"].plot(legend=True)
predictions.plot(legend=True)
plt.show()

# Forecast future values using SARIMA model
model = SARIMAX(
    daily["val"],
    order=(1, 0, 1),
    seasonal_order=(0, 1, 1, 12)
)

# Fit the model to the entire dataset
result = model.fit()

# Generate forecast for the next 12 periods and plot
forecast = result.predict(
    start=len(daily),
    end=(len(daily) - 1) + 12,
    typ="levels",
).rename("Forecast")

daily["val"].plot(figsize=(12, 5), legend=True)
forecast.plot(legend=True)
plt.show()