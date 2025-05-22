import os
import subprocess

# Directory containing the filtered files
filtered_dir = './filtered'

# Iterate through all files in the filtered directory
for file_name in os.listdir(filtered_dir):
    # Check if the file is a .txt file and contains 'english' in its name
    if file_name.endswith('.txt') and 'english' in file_name:
        file_path = os.path.join(filtered_dir, file_name)
        # Run frequency.py with the file as an argument
        subprocess.run(['python', 'frequency.py', file_path])