import os
from pathlib import Path

def wrap_html(file_path: str):
    original = Path(file_path)

    if not original.exists() or original.suffix.lower() != ".html":
        raise ValueError("Input must be an existing .html file")

    game_file = original.with_name("game.html")
    index_file = original.with_name("index.html")

    # Rename original → game.html
    os.rename(original, game_file)

    wrapper_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Game Wrapper</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            background: #000;
        }
        #ad-container {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: black;
        }
        #game-container {
            width: 100%;
            height: 100%;
            display: none;
        }
        iframe, video {
            width: 100%;
            height: 100%;
            border: none;
            object-fit: cover;
        }
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
window.SDK_OPTIONS = {
   gameId: "your_game_id_here",
   onEvent: function (a) {
      switch (a.name) {
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
      }
   }
};

(function (a, b, c) {
   var d = a.getElementsByTagName(b)[0];
   a.getElementById(c) || (a = a.createElement(b), a.id = c, a.src = "https://api.gamemonetize.com/sdk.js", d.parentNode.insertBefore(a, d))
})(document, "script", "gamemonetize-sdk");

function resumeGame() {
    document.getElementById("ad-container").style.display = "none";
    document.getElementById("game-frame").src = "game.html";
    document.getElementById("game-container").style.display = "block";
}
</script>

</body>
</html>
"""

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(wrapper_html)

    print(f"Created {index_file} and moved original to {game_file}")


# Example usage:
wrap_html("zip/game.html")