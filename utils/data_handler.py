'''load_data will load the data as a dataframe to a variable 'data'
add_expense will add the expense details given as input to the dataframe'''
from datetime import datetime, time
import pandas as pd

Data_path = 'data/expenses.csv'

def load_data():
    try:
        return pd.read_csv(Data_path, parse_dates=['date'])
    except:
        return pd.DataFrame(columns=['date', 'expense', 'category', 'description'], )
    
def save_data(df):
    df.to_csv(Data_path, index = False)

def add_expense(date, expense, category, description):
    df = load_data()
    if isinstance(date, datetime):
        set_date = date
    else:
        set_date = datetime.combine(date, time(0, 0))
    
    new_row = {
        "date": set_date,
        "expense": expense, 
        "category": category,
        "description": description,
    }

    df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
    save_data(df)