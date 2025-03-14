import pandas as pd
import os

def load_and_clean_data(dummy_npi_data):
    if not os.path.exists(dummy_npi_data):
        raise FileNotFoundError(f"Dataset not found: {dummy_npi_data}")
    
    df = pd.read_csv(dummy_npi_data)
    df['Login Time'] = pd.to_datetime(df['Login Time'], errors='coerce')
    df['Logout Time'] = pd.to_datetime(df['Logout Time'], errors='coerce')
    df.dropna(inplace=True)
    df['Session Duration'] = (df['Logout Time'] - df['Login Time']).dt.total_seconds() / 60
    return df
