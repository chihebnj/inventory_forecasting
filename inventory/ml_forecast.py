import pandas as pd
from sklearn.linear_model import LinearRegression
from .models import SalesHistory, Forecast

def train_and_forecast(product_id):
    # Fetch historical data
    data = SalesHistory.objects.filter(product_id=product_id).values('timestamp', 'quantity_sold')
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df = df.resample('D').sum()  # Daily aggregation

    # Simple linear regression (replace with ARIMA or LSTM for better accuracy)
    model = LinearRegression()
    X = df.index.dayofyear.values.reshape(-1, 1)  # Feature: day of year
    y = df['quantity_sold']
    model.fit(X, y)

    # Predict next 7 days
    future_days = [df.index[-1] + pd.Timedelta(days=i) for i in range(1, 8)]
    predictions = model.predict([[d.dayofyear] for d in future_days])

    # Save forecasts
    for i, pred in enumerate(predictions):
        Forecast.objects.create(
            product_id=product_id,
            predicted_demand=pred,
            forecast_date=future_days[i].date(),
            confidence=0.8  # Placeholder
        )