import os
import subprocess

# Directory containing the .txt files
directory = 'P'

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        # Run filterLanguage.py for each .txt file
        subprocess.run(['python', 'filterLanguage.py', filepath])