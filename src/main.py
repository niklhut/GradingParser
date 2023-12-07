import argparse
from csv_interactive_viewer import display_selected_columns

def main():
    parser = argparse.ArgumentParser(description="CSV Viewer with Interaction")
    parser.add_argument("csv_file_path", help="Path to the CSV file")
    parser.add_argument("--start", type=int, default=1, help="Start row index (default: 1)")
    parser.add_argument("--end", type=int, help="End row index")

    args = parser.parse_args()
    display_selected_columns(args)

if __name__ == "__main__":
    main()