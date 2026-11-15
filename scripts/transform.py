
import pandas as pd

def transform_weather(df):

    df["time"] = pd.to_datetime(df["time"])

    
    print("Missing values:")
    print(df.isnull().sum())

    
    print("Duplicates:",
          df.duplicated(subset=["time", "city"]).sum())

    
    print("\nDataFrame information:")
    df.info()

    return df
