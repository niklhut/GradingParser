import os
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from user_interface import get_input_options_description
from utils import *
from enum import Enum

class InteractiveViewer:

    class HandleUserInputResult(Enum):
        QUIT = 1
        SKIP = 2
        BACK = 3
        CONTINUE = 4

    def __init__(self, file_path, start_row, end_row, skip_graded):
        self.file_path = file_path
        path = Path(file_path)
        self.csv_file_path = path.stem + '.tmp.csv'
        self.start_row = start_row
        self.end_row = end_row
        self.skip_graded = skip_graded

        # Flag to save how many times the user went back
        self.back_flag = 0

        # List to keep track of skipped and graded rows
        self.skipped_rows = []

        # Counter for graded and skipped x rows
        self.graded_count = 0
        self.skipped_count = 0

        # Read the file
        self.df = read_file(file_path)

        # Validate start_row and end_row
        self.validate_start_and_end_row()

        # Convert to 0-based index
        self.start_row = max(self.start_row - 2, 0)
        # And set end_row to the last row if it is not specified
        self.end_row = min(self.end_row - 1, len(self.df)) if self.end_row else len(self.df)

        # Set total number of elements to grade
        self.total_elements = self.end_row - self.start_row

    def validate_start_and_end_row(self):
        # Validate start_row and end_row
        if self.start_row < 1 or (self.end_row and self.end_row >= len(self.df) + 2):
            print("Invalid start_row or end_row.")
            quit()

        if self.end_row and self.end_row < self.start_row:
            print("end_row must be greater than start_row.")
            quit()

    def should_skip_row(self, idx):
        if self.back_flag == 0 and self.skip_graded and (self.df.at[idx, 'valid'] == 'y' or self.df.at[idx, 'valid'] == 'n'):
            # Skip already graded rows
            self.skipped_rows.append(False)
            self.graded_count += 1
            return True
        return False

    def display_selected_columns(self):
        idx_list = list(self.df.iloc[self.start_row:self.end_row].index)
        self.current_idx = 0

        with ThreadPoolExecutor() as executor:
            while self.current_idx < len(idx_list):
                idx = idx_list[self.current_idx]

                if self.should_skip_row(idx):
                    self.current_idx += 1
                    continue

                self.display_row_info(idx)

                print("\n" + get_input_options_description())

                # Get user input
                user_input = get_user_input()
                res = self.handle_user_input(user_input, idx)

                if res == InteractiveViewer.HandleUserInputResult.QUIT:
                    break
                elif res == InteractiveViewer.HandleUserInputResult.BACK:
                    continue

                self.back_flag = max(self.back_flag - 1, 0)

                # Save the modified DataFrame back to the CSV file
                executor.submit(save_dataframe, self.df.copy(), self.csv_file_path)

                self.current_idx += 1

        # Save the modified DataFrame
        self.save_and_finish()

    def handle_user_input(self, user_input, idx):
        if user_input.lower() == 'q':
            print("Saving and quitting...")
            return InteractiveViewer.HandleUserInputResult.QUIT
        elif user_input.lower() == 's':
            if self.df.at[idx, 'valid'] == 'y' or self.df.at[idx, 'valid'] == 'n':
                self.skipped_rows.append(False)
                self.graded_count += 1
            else:
                self.skipped_rows.append(True)
                self.skipped_count += 1
            print("Skipping row...")
            return InteractiveViewer.HandleUserInputResult.SKIP
        elif user_input.lower() == 'b':
            # Go back to the previous row
            if self.current_idx > 0:
                self.back_flag += 1 # add two since we already subtracted one
                self.current_idx -= 1
                if self.skipped_rows[self.current_idx] == False:
                    self.graded_count -= 1
                else:
                    self.skipped_count -= 1
                self.skipped_rows.pop()
            return InteractiveViewer.HandleUserInputResult.BACK

        # Update DataFrame based on user input
        if user_input.lower() == 'y' or user_input.lower() == '1':
            self.skipped_rows.append(False)
            self.graded_count += 1
            self.df.at[idx, 'valid'] = '1'
        elif user_input.lower() == 'n' or user_input.lower() == '0':
            self.skipped_rows.append(False)
            self.graded_count += 1
            self.df.at[idx, 'valid'] = '0'
        return InteractiveViewer.HandleUserInputResult.CONTINUE

    def save_and_finish(self):
        # Save the modified DataFrame
        save_dataframe(self.df.copy(), self.file_path)

        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        # Display the counter at the top
        print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Graded rows:{Style.RESET_ALL} {self.graded_count}/{self.total_elements} (Skipped: {self.skipped_count})")


    def display_row_info(self, idx):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

        name_expected = self.df.at[idx, "name_expected"]
        documentation = self.df.at[idx, "documentation"]
        valid_status = self.df.at[idx, "valid"]

        # Display the count and total number of elements to grade before the valid row
        print(f"{Fore.CYAN}Graded rows:{Style.RESET_ALL} {self.graded_count}/{self.total_elements} (Skipped: {self.skipped_count})")
        if valid_status == '1' or valid_status == '0':
            print(f"{Fore.CYAN}Valid:{Style.RESET_ALL} {Fore.GREEN if valid_status == 'y' else Fore.RED}{valid_status}{Style.RESET_ALL}")
        else:
            print("Not yet graded")

        # Colorize the output for name_expected and documentation
        print(f"{Fore.CYAN}Name Expected:{Style.RESET_ALL} {name_expected}")
        print(f"{Fore.CYAN}Documentation:{Style.RESET_ALL}\n{Fore.GREEN}{documentation}{Style.RESET_ALL}")

