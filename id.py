from playwright.sync_api import sync_playwright
import re
import threading
from concurrent.futures import ThreadPoolExecutor

print_lock = threading.Lock()

def get_monitize(i):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            game_id = None

            def handle_request(request):
                nonlocal game_id
                url = request.url
                if "gamemonetize.com/account/event.php" in url:
                    match = re.search(r"game_id=([^&]+)", url)
                    if match:
                        game_id = match.group(1)

            page.on("request", handle_request)

            page.goto(f"https://lapatic.github.io/PixelVault/?id={i}")
            page.wait_for_timeout(5000)

            browser.close()

            return game_id

    except Exception as e:
        with print_lock:
            print(f"\nGame #{i} ERROR: {e}")

if __name__ == "__main__":
    MAX_WORKERS = 5

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(get_monitize, range(781))