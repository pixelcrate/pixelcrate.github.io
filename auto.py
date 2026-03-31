import id
import dump
import build
import os
import upload
import title

GAMES = 781

loggedin, session = upload.get_session()

for i in range(GAMES):
    if not os.path.exists(f"crawler/{i}"):
        game_id = id.get_monitize(i)
        if not game_id:
            dump.dump_stack(i)
        else:
            print(f"Game #{i} had ads")
            continue
    if not os.path.exists(f"zip/{i}.zip"):
        build.main(i)
        if not loggedin:
            print(f"Succesfully built game #{i}")
    else:
        if not loggedin:
            print(f"Game #{i} already built")
    if loggedin:
        if i > 1:
            upload.workflow(title.get_title(f"zip/{i}.zip"), i, session)
            print(f"Succesfully built and uploaded game #{i}")
