import json
import os

file_path = "store.json"

def append(string):
    """
    Appends a string to a JSON file containing a list.
    Creates the file if it doesn't exist.
    """
    data = []

    # Load existing JSON if it exists
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON file does not contain a list.")
            except json.JSONDecodeError:
                data = []

    # Append the string
    data.append(string)

    # Write back to JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)