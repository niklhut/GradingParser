import argparse
from interactive_viewer import InteractiveViewer
from utils import *

def main():
    parser = argparse.ArgumentParser(description="Table Viewer with Interaction")
    parser.add_argument("file_path", help="Path to the CSV or Excel file")
    parser.add_argument("--start", type=int, default=1, help="Start row index (default: 1)")
    parser.add_argument("--end", type=int, help="End row index (default: end of file)")
    parser.add_argument("--skip-graded", action="store_true", help="Skip already graded rows (default: False)")

    args = parser.parse_args()
    check_file_exists(args.file_path)
    create_backup_of_original_file(args.file_path)
    viewer = InteractiveViewer(args.file_path, args.start, args.end, args.skip_graded)
    viewer.display_selected_columns()

if __name__ == "__main__":
    main()