import os
import requests
from markdownify import markdownify as md

# ── Yapılandırma ────────────────────────────────────────────────
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://enqura.atlassian.net")
EMAIL          = os.environ.get("CONFLUENCE_EMAIL")
API_TOKEN      = os.environ.get("CONFLUENCE_API_TOKEN")
SPACE_KEY      = "EDP"
LABEL          = "customer-visible"
DOCS_DIR       = "docs"
# ────────────────────────────────────────────────────────────────


def get_pages_by_label():
    """Confluence'taki etiketli sayfaları çeker."""
    cql    = f'space = "{SPACE_KEY}" AND label = "{LABEL}"'
    url    = f"{CONFLUENCE_URL}/wiki/rest/api/content/search"
    auth   = (EMAIL, API_TOKEN)
    params = {"cql": cql, "expand": "body.storage", "limit": 200}
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    return response.json()["results"]


def parse_title(title: str):
    """
    'Android - Başlarken' → ('Android', 'Başlarken')
    'iOS - Core Modülü'   → ('iOS', 'Core Modülü')
    'Genel Bilgiler'      → ('Genel', 'Genel Bilgiler')  ← prefix yoksa
    """
    if " - " in title:
        parts = title.split(" - ", 1)
        category = parts[0].strip()
        page     = parts[1].strip()
    else:
        category = "Genel"
        page     = title.strip()
    return category, page


def safe_name(name: str) -> str:
    """Dosya/klasör adı için güvenli hale getirir."""
    return name.replace("/", "-").replace("\\", "-").strip()


def sync():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # 1. Confluence'tan güncel sayfa listesini al
    pages = get_pages_by_label()
    print(f"Confluence'ta {len(pages)} sayfa bulundu.")

    # 2. Beklenen dosya yollarını hesapla
    expected_files = set()
    for page in pages:
        category, page_name = parse_title(page["title"])
        category_dir = os.path.join(DOCS_DIR, safe_name(category))
        filename     = safe_name(page_name) + ".md"
        expected_files.add(os.path.join(category_dir, filename))

    # 3. Mevcut .md dosyalarını tara (assets/ ve index.md hariç)
    existing_files = set()
    for root, dirs, files in os.walk(DOCS_DIR):
        # assets klasörünü atla
        dirs[:] = [d for d in dirs if d != "assets"]
        for f in files:
            if f.endswith(".md") and f != "index.md":
                existing_files.add(os.path.join(root, f))

    # 4. Confluence'tan silinmiş dosyaları temizle
    stale_files = existing_files - expected_files
    for stale in stale_files:
        os.remove(stale)
        print(f"[SİLİNDİ] {stale}")
        # Klasör boşaldıysa onu da sil
        parent = os.path.dirname(stale)
        if os.path.isdir(parent) and not os.listdir(parent):
            os.rmdir(parent)
            print(f"[KLASÖR SİLİNDİ] {parent}")

    # 5. Güncel sayfaları yaz / güncelle
    for page in pages:
        title        = page["title"]
        category, page_name = parse_title(title)
        category_dir = os.path.join(DOCS_DIR, safe_name(category))
        os.makedirs(category_dir, exist_ok=True)

        filename  = safe_name(page_name) + ".md"
        file_path = os.path.join(category_dir, filename)

        html_content = page["body"]["storage"]["value"]
        markdown     = md(html_content, heading_style="ATX")
        content      = f"# {title}\n\n{markdown}"

        # Değişiklik yoksa atla
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                if f.read() == content:
                    print(f"[ATLANDI] {file_path} — değişiklik yok")
                    continue

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[YAZILDI] {file_path}")


if __name__ == "__main__":
    sync()
