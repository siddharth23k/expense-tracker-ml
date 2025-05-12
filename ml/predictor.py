from prophet import Prophet
from datetime import datetime, time
import pandas as pd

def predictor(periods, df):
    model = Prophet()
    df['date'] = pd.to_datetime(df['date'])
    modif_df = df[['date','expense']].copy()
    modif_df['year_month'] = modif_df['date'].dt.to_period('M')

    modif_df_grouped = modif_df.groupby('year_month')['expense'].sum().reset_index()
    modif_df_grouped['year_month'] = modif_df_grouped['year_month'].dt.to_timestamp()
    modif_df_grouped.columns = ['ds','y']
    model.fit(modif_df_grouped)

    future = model.make_future_dataframe(periods=3, freq='M')
    forecast = model.predict(future)
    forecast['ds'] = forecast['ds'].dt.to_period('M').astype(str)
    forecast = forecast.rename(columns={'ds': 'Month', 'yhat': 'Expense prediction'})
    return forecast[['Month', 'Expense prediction']].tail(3)