import argparse
from interactive_viewer import display_selected_columns

def main():
    parser = argparse.ArgumentParser(description="Table Viewer with Interaction")
    parser.add_argument("file_path", help="Path to the CSV or Excel file")
    parser.add_argument("--start", type=int, default=1, help="Start row index (default: 1)")
    parser.add_argument("--end", type=int, help="End row index (default: end of file)")
    parser.add_argument("--skip-graded", action="store_true", help="Skip already graded rows (default: False)")

    args = parser.parse_args()
    display_selected_columns(args)

if __name__ == "__main__":
    main()