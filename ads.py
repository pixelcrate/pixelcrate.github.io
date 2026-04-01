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
            width: 100%;
            background: #000;
        }}
        iframe {{
            border: none;
        }}
    </style>
</head>
<body>

<script>
window.SDK_OPTIONS = {{
    gameId: "{game_id}",
    onEvent: function(a) {{
        switch (a.name) {{
            case "SDK_GAME_START":
                // Load game.html in same-origin iframe
                if (!document.getElementById("game-iframe")) {{
                    const iframe = document.createElement("iframe");
                    iframe.id = "game-iframe";
                    iframe.src = "game.html";
                    iframe.style.position = "absolute";
                    iframe.style.top = "0";
                    iframe.style.left = "0";
                    iframe.style.width = "100%";
                    iframe.style.height = "100%";
                    document.body.appendChild(iframe);
                }}
                break;
            case "SDK_READY":
                console.log("SDK_READY");
                break;
            default:
                console.log("SDK event:", a.name);
        }}
    }}
}};

// Load SDK
(function(a,b,c){{
    var d = a.getElementsByTagName(b)[0];
    if(!a.getElementById(c)){{
        var s = a.createElement(b);
        s.id = c;
        s.src = "https://api.gamemonetize.com/sdk.js";
        d.parentNode.insertBefore(s,d);
    }}
}})(document,"script","gamemonetize-sdk");

window.onload = function() {{
    if(typeof sdk !== "undefined") {{
        sdk.showBanner(); // SDK handles ads
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

    print(f"Wrapped {zip_path} with SDK-controlled iframe game load.")


# Example usage
if __name__ == "__main__":
    wrap(input('Zip ID? '), input('Game ID? '))