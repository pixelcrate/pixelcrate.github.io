import requests
import login
import re
import os
import store

BASE = "https://gamemonetize.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

# ---------- HELPERS ----------

def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def build_payload(name):
    full_name = f"PixelVault {name}"
    nameid = slugify(full_name)

    payload = {
        "name": full_name,
        "nameid": nameid,
        "width": "800",
        "height": "600",
        "desc": f"Play {full_name}, a fast-paced browser game with simple controls and fun gameplay.",
        "submit": ""
    }

    # default categories/tags (edit if needed)
    categories = ["1", "2"]
    tags = ["375", "885"]

    # array-style fields
    data = []
    for k, v in payload.items():
        data.append((k, v))

    for c in categories:
        data.append(("category[]", c))

    for t in tags:
        data.append(("tags[]", t))

    return data


# ---------- CORE FLOW ----------

def create_game(session, name):
    full_name = f"{name}-PixelVault"
    nameid = slugify(full_name)

    resp = session.post(
        f"{BASE}/account/gameadd.php",
        data={
            "name": full_name,
            "nameid": nameid,
            "submit": ""
        },
        allow_redirects=True
    )

    match = re.search(r'id=(\d+)', resp.url)
    if not match:
        raise Exception("Failed to get game id")

    return match.group(1)


def get_gameid(session, game_id):
    resp = session.get(f"{BASE}/account/editgame.php?id={game_id}")

    match = re.search(
        r'upload\.php\?gameid=([a-z0-9]+)&id=(\d+)',
        resp.text
    )

    if not match:
        raise Exception("Failed to get gameid")

    return match.group(1)


def upload_zip(session, game_id, gameid, zip_num):
    path = f"zip/{zip_num}.zip"

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "rb") as f:
        resp = session.post(
            f"{BASE}/account/upload.php",
            params={
                "gameid": gameid,
                "id": game_id
            },
            files={
                "file": (f"{zip_num}.zip", f, "application/zip")
            }
        )

    print("Upload:", resp.status_code)


def submit_metadata(session, game_id, name):
    payload = build_payload(name)

    resp = session.post(
        f"{BASE}/account/editgame.php",
        params={"id": game_id},
        data=payload
    )

    print("Metadata:", resp.status_code)


def workflow(name, zip_num, session):
    # Step 1: create game
    game_id = create_game(session, name)
    print("id:", game_id)

    # Step 2: get gameid
    gameid = get_gameid(session, game_id)
    print("gameid:", gameid)

    # Step 3: upload zip
    upload_zip(session, game_id, gameid, zip_num)

    # Step 4: submit metadata
    submit_metadata(session, game_id, name)

    store.append(f"ZIP: {zip_num}, NAME: {name}, ID: {game_id}, GAME: {gameid}")

    print("Done.")

def get_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    session.cookies.update(login.cookie)

    resp = session.get("https://gamemonetize.com/account")
    return ("login" not in resp.text.lower(), session)

# ---------- MAIN ----------

if __name__ == "__main__":
    resp, session = get_session()
    print("Logged in?", resp)

    name = input("Game name: ")
    zip_num = input("Zip number (zip/{num}.zip): ")
    workflow(name, zip_num, session)