import os
import requests
from markdownify import markdownify as md

CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://enqura.atlassian.net")
EMAIL          = os.environ.get("CONFLUENCE_EMAIL")
API_TOKEN      = os.environ.get("CONFLUENCE_API_TOKEN")
SPACE_KEY      = "EDP"
LABEL_PUBLIC   = "customer-visible"
LABEL_PRIVATE  = "customer-private"
DOCS_DIR       = "docs"
PRIVATE_DIR    = os.path.join(DOCS_DIR, "Private")

def get_pages_by_label(label):
    cql    = f'space = "{SPACE_KEY}" AND label = "{label}"'
    url    = f"{CONFLUENCE_URL}/wiki/rest/api/content/search"
    auth   = (EMAIL, API_TOKEN)
    params = {"cql": cql, "expand": "body.storage", "limit": 200}
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    return response.json()["results"]

def parse_title(title: str):
    if " - " in title:
        parts = title.split(" - ", 1)
        category = parts[0].strip()
        page     = parts[1].strip()
    else:
        category = "Genel"
        page     = title.strip()
    return category, page

def safe_name(name: str) -> str:
    return name.replace("/", "-").replace("\\", "-").strip()

def sync_pages(pages, base_dir, expected_files):
    os.makedirs(base_dir, exist_ok=True)
    for page in pages:
        category, page_name = parse_title(page["title"])
        category_dir = os.path.join(base_dir, safe_name(category))
        os.makedirs(category_dir, exist_ok=True)
        filename  = safe_name(page_name) + ".md"
        file_path = os.path.join(category_dir, filename)
        expected_files.add(file_path)
        html_content = page["body"]["storage"]["value"]
        markdown     = md(html_content, heading_style="ATX")
        content      = f"# {page['title']}\n\n{markdown}"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                if f.read() == content:
                    print(f"[ATLANDI] {file_path} — değişiklik yok")
                    continue
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[YAZILDI] {file_path}")

def sync():
    os.makedirs(DOCS_DIR, exist_ok=True)

    public_pages  = get_pages_by_label(LABEL_PUBLIC)
    private_pages = get_pages_by_label(LABEL_PRIVATE)
    print(f"Public: {len(public_pages)} sayfa, Private: {len(private_pages)} sayfa bulundu.")

    expected_files = set()
    sync_pages(public_pages, DOCS_DIR, expected_files)
    sync_pages(private_pages, PRIVATE_DIR, expected_files)

    # Stale dosyaları temizle
    existing_files = set()
    for root, dirs, files in os.walk(DOCS_DIR):
        dirs[:] = [d for d in dirs if d != "assets"]
        for f in files:
            if f.endswith(".md") and f != "index.md":
                existing_files.add(os.path.join(root, f))

    for stale in existing_files - expected_files:
        os.remove(stale)
        print(f"[SİLİNDİ] {stale}")
        parent = os.path.dirname(stale)
        if os.path.isdir(parent) and not os.listdir(parent):
            os.rmdir(parent)
            print(f"[KLASÖR SİLİNDİ] {parent}")

if __name__ == "__main__":
    sync()
