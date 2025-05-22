import os
import sys

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'

def is_punctuation(char):
    return char in "。？！：；，、“”‘’（）《》【】[]{}.,!?;:\"'()<>"

def extract_chinese_line_by_line(content):
    lines = content.splitlines()
    chinese_lines = []
    
    for line in lines:
        if line.startswith("P:"):
            prefix = line[:2]
            chinese_part = ''.join([c for c in line[2:] if is_chinese(c) or is_punctuation(c)])
            chinese_lines.append(f"{prefix}{chinese_part}")
        elif line.startswith("I") or line.startswith("i"):
            # Ignore lines starting with I: or i:
            continue
        else:
            # If the line has no P:/I:/i: prefix, skip it or handle separately if needed
            continue

    return '\n'.join(chinese_lines)

def extract_english(content):
    lines = content.splitlines()
    english_lines = []
    
    for line in lines:
        if line.startswith("I") or line.startswith("i"):
            # Skip lines starting with I: or i:
            continue
        else:
            english_part = ''.join([c for c in line if not is_chinese(c)])
            english_lines.append(english_part)
    
    return '\n'.join(english_lines)

def process_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_content(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main(input_files):
    for file_path in input_files:
        if file_path.endswith('.txt'):
            content = process_txt(file_path)
            chinese_content = extract_chinese_line_by_line(content)
            english_content = extract_english(content)
            
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            chinese_file = f"{base_name}_chinese.txt"
            english_file = f"{base_name}_english.txt"
            
            save_content(chinese_content, chinese_file)
            save_content(english_content, english_file)
            print(f"Processed {file_path}: saved Chinese content to {chinese_file}, English content to {english_file}")

if __name__ == "__main__":
    input_files = sys.argv[1:]
    if not input_files:
        print("Please provide at least one .txt file as input.")
    else:
        main(input_files)
