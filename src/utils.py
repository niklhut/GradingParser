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

    while user_input.lower() not in ['y', 'n', 's', 'b', 'q', '']:
        # Keep waiting for a valid input
        print("Invalid input. " + get_input_options_description())
        user_input = input()

    return user_input
