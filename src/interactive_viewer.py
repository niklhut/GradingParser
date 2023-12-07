import pandas as pd
import os
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from user_interface import get_input_options_description
from utils import save_dataframe

def display_row_info(df, idx, graded_count, skipped_count, total_elements):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

    name_expected = df.at[idx, "name_expected"]
    documentation = df.at[idx, "documentation"]
    valid_status = df.at[idx, "valid"]

    # Display the count and total number of elements to grade before the valid row
    print(f"{Fore.CYAN}Graded rows:{Style.RESET_ALL} {graded_count}/{total_elements} (Skipped: {skipped_count})")
    if valid_status == 'y' or valid_status == 'n':
        print(f"{Fore.CYAN}Valid:{Style.RESET_ALL} {Fore.GREEN if valid_status == 'y' else Fore.RED}{valid_status}{Style.RESET_ALL}")
    else:
        print("Not yet graded")

    # Colorize the output for name_expected and documentation
    print(f"{Fore.CYAN}Name Expected:{Style.RESET_ALL} {name_expected}")
    print(f"{Fore.CYAN}Documentation:{Style.RESET_ALL}\n{Fore.GREEN}{documentation}{Style.RESET_ALL}")

def display_selected_columns(args):
    try:
        if args.file_path.endswith('.xlsx'):
            df = pd.read_excel(args.file_path, header=0)
        elif args.file_path.endswith('.csv'):
            df = pd.read_csv(args.file_path, header=0, sep=';', lineterminator='\r')
        else:
            print("Error: File format not supported.")
            return
    except FileNotFoundError:
        print(f"Error: File '{args.file_path}' not found.")
        return
    except pd.errors.EmptyDataError:
        print("Table file is empty.")
        return
    except pd.errors.ParserError as e:
        print(f"Error parsing Table: {e}")
        return

    # Validate start_row and end_row
    if args.start < 1 or (args.end and args.end >= len(df) + 2):
        print("Invalid start_row or end_row.")
        return

    # Convert to 0-based index
    start_row = max(args.start - 2, 0)
    # And set end_row to the last row if it is not specified
    end_row = min(args.end - 1, len(df)) if args.end else len(df)

    # Skip graded
    skip_graded = args.skip_graded

    # Counter for graded and skipped x rows
    graded_count = 0
    skipped_count = 0

    # List to keep track of skipped and graded rows
    skipped_rows = []

    # Count and total number of elements to grade before the valid row
    total_elements = end_row - start_row

    idx_list = list(df.iloc[start_row:end_row].index)
    current_idx = 0

    with ThreadPoolExecutor() as executor:
        while current_idx < len(idx_list):
            idx = idx_list[current_idx]

            if skip_graded and (df.at[idx, 'valid'] == 'y' or df.at[idx, 'valid'] == 'n'):
                # Skip already graded rows
                graded_count += 1
                current_idx += 1
                continue

            display_row_info(df, idx, graded_count, skipped_count, total_elements)

            print("\n" + get_input_options_description())

            # Wait for user input
            user_input = input()

            while user_input.lower() not in ['y', 'n', 's', 'b', 'q', '']:
                # Keep waiting for a valid input
                print("Invalid input. Please press 'Y', 'N', 'S', 'B', 'Q', or 'Enter'.")
                user_input = input()

            if user_input.lower() == 'q':
                print("Saving and quitting...")
                # Save the modified DataFrame back to the CSV file
                executor.submit(save_dataframe, df.copy(), args.file_path)
                return
            elif user_input.lower() == 's':
                skipped_rows.append(True)
                skipped_count += 1
                print("Skipping row...")
            elif user_input.lower() == 'b':
                # Go back to the previous row
                if current_idx > 0:
                    current_idx -= 1
                    if skipped_rows[idx - 1] == False:
                        graded_count -= 1
                    else:
                        skipped_count -= 1
                    skipped_rows.pop()
                continue

            # Update DataFrame based on user input
            if user_input.lower() == 'y':
                skipped_rows.append(False)
                graded_count += 1
                df.at[idx, 'valid'] = 'y'
            elif user_input.lower() == 'n':
                skipped_rows.append(False)
                graded_count += 1
                df.at[idx, 'valid'] = 'n'
            
            # Save the modified DataFrame back to the CSV file
            executor.submit(save_dataframe, df.copy(), args.file_path)

            current_idx += 1

    # Save the modified DataFrame back to the CSV file
    save_dataframe(df, args.file_path)

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    # Display the counter at the top
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Graded rows:{Style.RESET_ALL} {graded_count}/{total_elements} (Skipped: {skipped_count})")
