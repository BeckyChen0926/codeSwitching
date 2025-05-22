import re
from collections import Counter
import csv
import sys
import os

def clean_text(text):
    # Replace Chinese punctuation with spaces
    text = re.sub(r'[，。？！：；、“”‘’（）《》【】]', ' ', text)

    # Lowercase everything
    text = text.lower()

    # Extract only English words (removes numbers, special chars)
    words = re.findall(r'\b[a-z]+\b', text)

    return words

# Read sample text from terminal input (can take multiple files)

if len(sys.argv) < 2:
    print("Usage: python frequencyTest.py <file1> <file2> ...")
    sys.exit(1)

sample = ""
for file_path in sys.argv[1:]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sample += file.read() + " "
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

words = clean_text(sample)
word_frequencies = Counter(words)

# Read existing CSV if it exists
try:
    with open('word_frequencies.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        existing_data = list(reader)
        headers = existing_data[0]
        data = {row[0]: {headers[i]: int(row[i]) for i in range(1, len(headers))} for row in existing_data[1:]}
except FileNotFoundError:
    headers = ['PID']
    data = {}

# Update data with current PID and word frequencies
# Extract PID from the first file name (assuming PID is the number in the file name)
PID = None
for file_path in sys.argv[1:]:
    file_name = os.path.basename(file_path)
    match = re.search(r'\d+', file_name)
    if match:
        PID = match.group(0)
        break

if not PID:
    print("Error: Could not extract PID from file names.")
    sys.exit(1)

if PID not in data:
    data[PID] = {word: 0 for word in headers[1:]}  # Initialize with existing words

for word, freq in word_frequencies.items():
    if word not in headers:
        headers.append(word)
        for pid in data:
            data[pid][word] = 0
    if word not in data[PID]:
        data[PID][word] = 0
    data[PID][word] += freq

# Write updated data back to CSV
with open('word_frequencies.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for pid, word_freqs in data.items():
        row = [pid] + [word_freqs.get(word, 0) for word in headers[1:]]
        writer.writerow(row)

print("Cumulative word frequencies saved to word_frequencies.csv")


