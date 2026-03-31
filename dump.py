import os
import time
import threading
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

# ===================== CONFIG =====================
BASE_OUTPUT_DIR = "crawler"

HEADLESS = True
WAIT_TIME_MS = 8000
REQUEST_DELAY = 0  # delay between runs (seconds)

SAVE_TYPES = ["javascript", "json", "html", "text"]
# =================================================

os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

lock = threading.Lock()


def dump_stack(id):
    base_dir = os.path.join(BASE_OUTPUT_DIR, str(id))
    os.makedirs(base_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context()
        page = context.new_page()

        # ---- SAVE RESPONSES ----
        def save_response(response):
            url = response.url

            try:
                parsed = urlparse(url)

                if not parsed.path or url.startswith("data:"):
                    return

                content_type = response.headers.get("content-type", "")
                if not any(x in content_type for x in SAVE_TYPES):
                    return

                body = response.body()

                # ---- LOCAL SAVE ----
                path = parsed.path.lstrip("/")
                if path.endswith("/") or path == "":
                    path += "index.html"

                local_path = os.path.join(base_dir, parsed.netloc, path)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                with open(local_path, "wb") as f:
                    f.write(body)

            except Exception as e:
                # with lock:
                #     print(f"[{id}] Error saving {url}: {e}")
                pass

        # ---- TRACK GAMEMONETIZE ----
        def track_requests(request):
            if "gamemonetize.com" in request.url:
                with lock:
                    print(f"\n[{id}] GM CALL: {request.url}")

        page.on("response", save_response)
        page.on("request", track_requests)

        # ---- LOAD PAGE ----
        page.goto(f"https://lapatic.github.io/PixelVault/?id={id}")
        page.wait_for_timeout(WAIT_TIME_MS)

        browser.close()

    if REQUEST_DELAY:
        time.sleep(REQUEST_DELAY)


# ===================== EXAMPLE =====================
if __name__ == "__main__":
    dump_stack(input("Game ID? "))