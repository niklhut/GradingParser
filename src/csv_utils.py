import pandas as pd

def save_dataframe(df, csv_file_path):
    df.to_csv(csv_file_path, sep=';', index=False, lineterminator='\r')