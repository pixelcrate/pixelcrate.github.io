import os
import shutil
import zipfile
import re

def is_obfuscated_script(line):
    line = line.strip()

    # if not line.startswith("<script"):
    #     return False

    # Heuristics for obfuscation / anti-tampering
    patterns = [
        r"<script",
        r"_0x[a-fA-F0-9]+",        # hex-like variable names (_0x123abc)
        r"while\s*\(\s*!!\[\]\s*\)", # while(!![]) infinite loops
        r"function\s*\(_0x",       # obfuscated function params
        r"parseInt\(",             # heavy parseInt usage in obfuscation
        r"Math\.(floor|ceil|trunc)", # math noise common in obfuscation
        r"\[\s*['\"]",             # weird array string access
    ]

    score = sum(bool(re.search(p, line)) for p in patterns)

    # Require multiple signals to avoid false positives
    return score >= 3


def clean_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for id, line in enumerate(lines):
        if is_obfuscated_script(line):
            lines.pop(id)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def zip(html_file_path, game_id):
    # Ensure the zip directory exists
    os.makedirs("zip", exist_ok=True)

    # Define the zip file path
    zip_path = f"zip/{game_id}.zip"

    # Add the HTML file to the zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # The second argument is the name inside the zip
        zipf.write(html_file_path, "index.html")

def main(id):
    directory = f"crawler/{id}/cdn.jsdelivr.net/gh/%67%6e%2d%6d%61%74%68/html@main"
    file = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))][0]
    clean_html(os.path.join(directory, file))
    zip(os.path.join(directory, file), id)

if __name__ == "__main__":
    main(input("Game ID? "))