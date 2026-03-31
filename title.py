import zipfile
import os
import tempfile
from bs4 import BeautifulSoup

def get_title(zip_path):
    """
    Extracts the first HTML file from a ZIP, reads its <title>, then cleans up.
    Returns the title string or None if not found.
    """
    title_text = None
    
    # Create a temporary directory for extraction
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
                
                # Walk through extracted files to find the first HTML file
                for root, _, files in os.walk(tmpdir):
                    for file in files:
                        if file.lower().endswith('.html') or file.lower().endswith('.htm'):
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            soup = BeautifulSoup(html_content, 'html.parser')
                            title_tag = soup.find('title')
                            if title_tag:
                                title_text = title_tag.get_text()
                            return title_text  # Return after first HTML file processed
        except (zipfile.BadZipFile, FileNotFoundError):
            print(f"Cannot process ZIP file: {zip_path}")
            return None
    return None