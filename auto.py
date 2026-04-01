import id
import dump
import build
import os
import upload
import ads
import store
import time
import title

GAMES = 781

def main(i):
    try:
        if not os.path.exists(f"crawler/{i}"):
            game_id = id.get_monitize(i)
            if not game_id:
                dump.dump_stack(i)
            else:
                print(f"Game #{i} had ads")
                return
        else:
            print(f"Game #{i} already crawled")
        if not os.path.exists(f"zip/{i}.zip"):
            build.main(i)
            print(f"Succesfully built game #{i}")
        else:
            print(f"Game #{i} already built")
        loggedin, session = upload.get_session()
        if loggedin:
            mid, gameid = upload.makegame(title.get_title(f"zip/{i}.zip"), i, session)
            if not title.get_title(f"zip/{i}.zip"):
                os.remove(f"zip/{i}.zip")
                raise(f"Failed to get title of game {i}")
            ads.wrap(i, gameid)
            upload.upload_zip(session, mid, gameid, i)
            print(f"Succesfully built and uploaded game #{i}")
        else:
            print("Not logged in")
    except Exception as e:
        print(f"Game {i} failed with exception: {e}")
        store.append(f"Game {i} failed with exception: {e}")
if __name__ == "__main__":
    for i in range(GAMES):
        if i > 22:
            main(i)