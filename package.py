import os
import zipfile
import shutil
from pathlib import Path

AUDIO_WRAPPER = """
<script>
// --- AUDIO MUTE SYSTEM ---
function muteGameAudio() {
    document.querySelectorAll('audio,video').forEach(el => el.pause());
    console.log('Game audio muted');
}

function unmuteGameAudio() {
    document.querySelectorAll('audio,video').forEach(el => el.play().catch(() => {}));
    console.log('Game audio unmuted');
}

// --- SDK INTEGRATION ---
window.SDK_OPTIONS = {
    gameId: "your_game_id_here",
    onEvent: function(event) {
        switch(event.name) {
            case "SDK_GAME_PAUSE":
                muteGameAudio();
                break;
            case "SDK_GAME_START":
                unmuteGameAudio();
                break;
            case "SDK_READY":
                if(typeof sdk !== 'undefined' && sdk.showBanner !== 'undefined'){
                    sdk.showBanner(); // auto-show ad on load
                }
                break;
        }
    }
};

// Inject SDK
(function(d, t, id){
    var s = d.getElementsByTagName(t)[0];
    if(!d.getElementById(id)){
        var js = d.createElement(t);
        js.id = id;
        js.src = "https://api.gamemonetize.com/sdk.js";
        s.parentNode.insertBefore(js, s);
    }
})(document,"script","gamemonetize-sdk");

// Auto-mute immediately until ad finishes
window.addEventListener('load', () => {
    muteGameAudio();
});
</script>
"""

def process_zip(num: int, game_id: str):
    """
    Process zip/{num}.zip:
    - Unzip
    - Inject audio mute + SDK wrapper into index.html
    - Delete old ZIP
    - Rezip to the same path
    """
    zip_path = Path(f"zip/{num}.zip")
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    temp_dir = Path(f"temp_{num}")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    # Unzip
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(temp_dir)

    # Find index.html
    index_file = None
    for root, dirs, files in os.walk(temp_dir):
        if 'index.html' in files:
            index_file = Path(root) / 'index.html'
            break

    if not index_file:
        shutil.rmtree(temp_dir)
        raise FileNotFoundError("index.html not found in the ZIP")

    html_text = index_file.read_text(encoding='utf-8')

    # Replace placeholder gameId
    wrapper_code = AUDIO_WRAPPER.replace("your_game_id_here", game_id)

    # Inject before </head>
    if "</head>" in html_text:
        html_text = html_text.replace("</head>", wrapper_code + "\n</head>")
    else:
        html_text = wrapper_code + "\n" + html_text

    # Write back
    index_file.write_text(html_text, encoding='utf-8')

    # Delete old ZIP
    zip_path.unlink()

    # Rezip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                zf.write(file_path, arcname=file_path.relative_to(temp_dir))

    # Clean up temp folder
    shutil.rmtree(temp_dir)

    print(f"Processed ZIP {zip_path} successfully. Audio mute + SDK wrapper injected.")

# Example usage:
# process_zip(1, "my_game_id_123")