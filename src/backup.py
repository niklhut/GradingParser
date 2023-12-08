from pathlib import Path
import shutil

def create_backup_of_original_file(file_path):
    # Create a backup of the original file
    path = Path(file_path)
    shutil.copyfile(file_path, path.stem + '.original' + path.suffix)