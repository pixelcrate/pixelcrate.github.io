import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_HTML = "https://cdn.jsdelivr.net/gh/gn-math/html@main/"
ZONES_JSON = "https://cdn.jsdelivr.net/gh/gn-math/assets@main/zones.json"

SAVE_DIR = "games"
ASSET_DIR = os.path.join(SAVE_DIR, "assets")

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(ASSET_DIR, exist_ok=True)

session = requests.Session()


def download_file(url):
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        return r.content
    except:
        return None


def save_asset(url):
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")

    local_path = os.path.join(ASSET_DIR, path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not os.path.exists(local_path):
        data = download_file(url)
        if data:
            with open(local_path, "wb") as f:
                f.write(data)

    return os.path.relpath(local_path, SAVE_DIR)


def clean_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    # 🔽 Download assets and rewrite paths
    for tag in soup.find_all(["script", "link", "img"]):
        attr = "src" if tag.name in ["script", "img"] else "href"

        if tag.has_attr(attr):
            full_url = urljoin(base_url, tag[attr])

            if full_url.startswith("http"):
                local_path = save_asset(full_url)
                if local_path:
                    tag[attr] = local_path

    return str(soup)


# 🔽 Load zones.json
zones = session.get(ZONES_JSON).json()

for zone in zones:
    try:
        game_id = zone["id"]
        url_template = zone["url"]

        # Replace placeholders
        game_url = url_template.replace("{HTML_URL}", BASE_HTML)

        if not game_url.startswith("http"):
            game_url = urljoin(BASE_HTML, game_url)

        print(f"Downloading game {game_id}...")

        html = session.get(game_url).text
        cleaned = clean_html(html, game_url)

        # Save cleaned HTML
        output_path = os.path.join(SAVE_DIR, f"{game_id}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

    except Exception as e:
        print(f"Error on game {zone.get('id')}: {e}")

print("Done.")