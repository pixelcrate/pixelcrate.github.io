import zipfile
from pathlib import Path
import shutil

def wrap(num: int, game_id: str):
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
    index_html = temp_dir / "index.html"

    # Rename original index.html → game.html
    original_html.rename(game_html)

    # Wrapper HTML
    wrapper_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pixel Crate</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        video {{
            width: 100%;
            height: 100%;
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

<script>
let gameStarted = false;

function openGame() {{
    if (gameStarted) return;
    gameStarted = true;

    // Open in new tab
    const win = window.open("game.html", "_blank");

    // Attempt fullscreen (only works if browser allows)
    if (win) {{
        try {{
            win.focus();
        }} catch (e) {{}}
    }}
}}

window.SDK_OPTIONS = {{
   gameId: "{game_id}",
   onEvent: function (a) {{
      switch (a.name) {{
         case "SDK_GAME_START":
            openGame();
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
   if (!a.getElementById(c)) {{
       var s = a.createElement(b);
       s.id = c;
       s.src = "https://api.gamemonetize.com/sdk.js";
       d.parentNode.insertBefore(s, d);
   }}
}})(document, "script", "gamemonetize-sdk");

window.onload = function() {{
    const video = document.getElementById("ad-video");

    // Fallback if SDK doesn't trigger
    video.onended = openGame;

    // Optional: safety timeout (uncomment if needed)
    // setTimeout(openGame, 8000);

    if (typeof sdk !== "undefined") {{
        sdk.showBanner();
    }}
}};
</script>

</body>
</html>
"""

    # Write wrapper
    index_html.write_text(wrapper_html, encoding="utf-8")

    # Rebuild ZIP (only two files needed)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(index_html, "index.html")
        zipf.write(game_html, "game.html")

    # Cleanup
    shutil.rmtree(temp_dir)

    print(f"Wrapped {zip_path} with ad + new-tab game launch.")


# Example usage
if __name__ == "__main__":
    wrap(input('Zip ID? '), input('Game ID? '))