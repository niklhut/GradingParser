# Interactive Viewer

This project is a Python script that allows users to interactively view and grade rows in a data file. It supports both Excel (.xlsx) and CSV (.csv) files.

## File Format

The script expects the data file to have a header row with the following columns:

- `name_expected`: The expected name of the class or method for which the documentation is
- `documentation`: The JavaDoc documentation for the class or method
- `valid`: Whether the documentation is valid or not. This column will be overwritten by the script with `y` or `n` depending on the user's input. A row is considered graded if this column contains either `y` or `n`.

## Features

- Clear console output for easy reading
- Colorized output for better visibility
- Supports skipping already graded rows

## Usage

Run the script with the following command:

```bash
python src/main.py <path_to_file> --start <start_row> --end <end_row> --skip_graded
```

Replace `<path_to_file>` with the path to your Excel or CSV file, `<start_row>` and `<end_row>` with the range of rows you want to grade. If you don't want to skip already graded rows, you can omit the `--skip_graded` flag.

In the interactive viewer, you can use the following commands:

- `y`: Mark the current row as valid
- `n`: Mark the current row as invalid
- `s`: Skip the current row
- `b`: Go back to the previous row
- `q`: Quit the interactive viewer

Then press `Enter` to confirm your input.

The script will create a backup of the original file in the same directory as the original file, with the suffix `.original`. The script will then overwrite the original file with the graded rows.

Your progress will be saved into the initial file after every row. If you quit the interactive viewer, you can resume your progress by running the script again with the same arguments, using the `--skip_graded` flag to skip already graded rows.

To avoid corrupting the data file make sure to not use `Ctrl+C` to quit the interactive viewer, instead use the `q` command.

When working with big Excel files, the saving process can take a while. If you want to speed up the process, you can convert your Excel file to a CSV file and use that instead.

## Dependencies

Before running you might need to install the following dependencies with `pip`:

- `pandas`
- `openpyxl`
- `colorama`