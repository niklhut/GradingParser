import pandas as pd

def save_dataframe(df, file_path):
    if file_path.endswith('.xlsx'):
        df.to_excel(file_path, index=False)
    elif file_path.endswith('.csv'):
        df.to_csv(file_path, sep=';', index=False, lineterminator='\r')
    else:
        print("Error: File format not supported.")
        return