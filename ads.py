import os
import zipfile
from pathlib import Path
import shutil

def wrap_game_zip(num: int, game_id: str):
    zip_path = Path(f"zip/{num}.zip")
    if not zip_path.exists():
        raise FileNotFoundError(f"{zip_path} does not exist")

    # Temporary extraction folder
    temp_dir = Path(f"temp_{num}")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    # Extract ZIP
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    original_html = temp_dir / "index.html"
    if not original_html.exists():
        raise FileNotFoundError("index.html not found in the ZIP")

    game_html = temp_dir / "game.html"
    index_html = temp_dir / "index.html"  # wrapper will overwrite this

    # Rename original index.html → game.html
    original_html.rename(game_html)

    # Create wrapper index.html
    wrapper_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Game Wrapper</title>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            height: 100%;
            background: #000;
        }}
        #ad-container {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: black;
        }}
        #game-container {{
            width: 100%;
            height: 100%;
            display: none;
        }}
        iframe, video {{
            width: 100%;
            height: 100%;
            border: none;
            object-fit: cover;
        }}
    </style>
</head>
<body>

<div id="ad-container">
    <video id="ad-video" autoplay muted playsinline>
        <source src="ad.mp4" type="video/mp4">
    </video>
</div>

<div id="game-container">
    <iframe id="game-frame" src=""></iframe>
</div>

<script type="text/javascript">
window.SDK_OPTIONS = {{
   gameId: "{game_id}",
   onEvent: function (a) {{
      switch (a.name) {{
         case "SDK_GAME_START":
            resumeGame();
            break;
         case "SDK_GAME_PAUSE":
            console.log("SDK_GAME_PAUSE");
            break;
         case "SDK_READY":
            console.log("SDK_READY");
            break;
         default:
            console.log("SDK event:", a.name);
            break;
      }}
   }}
}};

(function (a, b, c) {{
   var d = a.getElementsByTagName(b)[0];
   a.getElementById(c) || (a = a.createElement(b), a.id = c, a.src = "https://api.gamemonetize.com/sdk.js", d.parentNode.insertBefore(a, d))
}})(document, "script", "gamemonetize-sdk");

function resumeGame() {{
    document.getElementById("ad-container").style.display = "none";
    document.getElementById("game-frame").src = "game.html";
    document.getElementById("game-container").style.display = "block";
}}
</script>

</body>
</html>
"""

    # Write wrapper index.html
    index_html.write_text(wrapper_html, encoding="utf-8")

    # Create a new ZIP with the same name, containing index.html and game.html
    new_zip_path = zip_path
    with zipfile.ZipFile(new_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(index_html, "index.html")
        zipf.write(game_html, "game.html")

    # Cleanup temporary folder
    shutil.rmtree(temp_dir)

    print(f"Wrapped {zip_path} with SDK and recreated index.html/game.html in ZIP.")


# Example usage:
