import json
import re

# Load your JSON file
with open("store.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Pattern to extract structured game data
pattern = re.compile(r"ZIP:\s*(\d+), NAME:\s*(.*?), ID:\s*(\d+), GAME:\s*(\S+)")

cleaned_data = []

for entry in data:
    match = pattern.match(entry)
    if match:
        zip_code, name, game_id, game_key = match.groups()
        cleaned_data.append({
            "icon": None,
            "zip": int(zip_code),
            "name": name.strip(),
            "id": int(game_id),
            "game": f"https://html5.gamemonetize.com/{game_key.strip()}/",
            "error": None
        })
    else:
        # Capture error entries
        cleaned_data.append({
            "icon": None,
            "zip": None,
            "name": None,
            "id": None,
            "game": None,
            "error": entry
        })

# Save the cleaned, structured data
with open("games_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

print("Conversion complete. Output saved to games_cleaned.json")