import build
import ads
import os

try:
    os.remove("zip/5.zip")
    os.remove("zip/index.html")
    os.remove("zip/game.html")
except:
    pass
build.main(5)
ads.wrap(5, "99oz3b678714l1sru7lucqnokxcdhbvn")
import zipfile
from pathlib import Path

zip_path = Path("zip/5.zip")  # replace with your zip file name
extract_to = zip_path.parent      # same folder as the zip

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print("Extraction complete.")