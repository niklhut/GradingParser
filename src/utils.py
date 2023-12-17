import pandas as pd 
from pathlib import Path
import shutil
from user_interface import get_input_options_description

def save_dataframe(df, file_path):

    # Save the modified DataFrame back to the CSV file
    if file_path.endswith('.xlsx'):
        df.to_excel(file_path, index=False)
    elif file_path.endswith('.csv'):
        df.to_csv(file_path, sep=';', index=False, lineterminator='\r')
    else:
        print("Error: File format not supported.")
        return
    
def get_user_input():
    user_input = input()

    while user_input.lower() not in ['y', 'n', 's', 'b', 'q']:
        # Keep waiting for a valid input
        print("Invalid input. " + get_input_options_description())
        user_input = input()

    return user_input

def check_file_exists(file_path):
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: File '{file_path}' not found.")
        quit()

def read_file(file_path):
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, header=0)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, header=0, sep=';', lineterminator='\r')
        else:
            print("Error: File format not supported.")
            quit()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        quit()
    except pd.errors.EmptyDataError:
        print("Table file is empty.")
        quit()
    except pd.errors.ParserError as e:
        print(f"Error parsing Table: {e}")
        quit()

    return df

def create_backup_of_original_file(file_path):
    # Create a backup of the original file
    path = Path(file_path)
    shutil.copyfile(file_path, path.stem + '.original' + path.suffix)
