"""
This script flush the file of the target CIRCUITPY1 drive 
With the current project code.

"""
import os
import subprocess
import sys

CURRENT_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
TARGET_CIRCUITPY_PATH = "/media/eloistree/CIRCUITPY1"

def run_with_sudo():
    """Check if running with sudo, if not, restart with sudo"""
    if os.geteuid() != 0:
        print("This script requires sudo privileges. Restarting with sudo...")
        subprocess.call(['sudo', sys.executable] + sys.argv)
        sys.exit()

def delete_all_files_and_folders(path):
    """Recursively delete all files and folders in the given path"""
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            os.rmdir(dir_path)

def delete_on_pico2w():
    """Delete all files and folders on the PICO2W CIRCUITPY drive"""
    delete_all_files_and_folders(TARGET_CIRCUITPY_PATH)

def copy_to_pico2w():
    """Copy all files and folders from the current project to the PICO2W CIRCUITPY drive"""
    for root, dirs, files in os.walk(CURRENT_PROJECT_PATH):
        relative_path = os.path.relpath(root, CURRENT_PROJECT_PATH)
        target_root = os.path.join(TARGET_CIRCUITPY_PATH, relative_path)
        os.makedirs(target_root, exist_ok=True)
        for file_name in files:
            source_file = os.path.join(root, file_name)
            target_file = os.path.join(target_root, file_name)
            with open(source_file, "rb") as src_file:
                with open(target_file, "wb") as tgt_file:
                    tgt_file.write(src_file.read())

if __name__ == "__main__":
    run_with_sudo()
    print("Deleting all files on PICO2W CIRCUITPY drive...")
    delete_on_pico2w()
    print("Copying project files to PICO2W CIRCUITPY drive...")
    copy_to_pico2w()
    print("Done.")