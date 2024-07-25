import os
import re
import argparse

def rename_files_in_directory(directory):
    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Create the new filename by adding dashes between words
            new_filename = re.sub(r'([a-z])([A-Z])', r'\1-\2', filename)
            new_filename = re.sub(r'(\d+)([a-zA-Z])', r'\1-\2', new_filename)
            new_filename = re.sub(r'([a-zA-Z])(\d+)', r'\1-\2', new_filename)

            # Rename the file
            old_file_path = os.path.join(root, filename)
            new_file_path = os.path.join(root, new_filename)
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {old_file_path} -> {new_file_path}')

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Rename files in a directory and its subdirectories by adding dashes between words.')
    parser.add_argument('directory', type=str, help='The path to the directory containing the files to rename')

    # Parse the arguments
    args = parser.parse_args()

    # Run the function with the provided directory
    rename_files_in_directory(args.directory)

