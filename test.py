import build
import package
import os

try:
    os.remove("zip/1.zip")
    os.remove("zip/index.html")
except:
    pass
build.main(1)
package.process_zip(1, "38hq4lnuk5njkl05w3i9txs5yuvzylcl")
import zipfile
from pathlib import Path

zip_path = Path("zip/1.zip")  # replace with your zip file name
extract_to = zip_path.parent      # same folder as the zip

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print("Extraction complete.")