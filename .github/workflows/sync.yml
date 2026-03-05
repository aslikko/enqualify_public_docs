name: Confluence to GitHub Sync

on:
  schedule:
    - cron: '0 * * * *' # Her saat başı otomatik çalışır
  workflow_dispatch: # İstediğimiz an manuel çalıştırmak için buton ekler

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: pip install requests markdownify

      - name: Run Sync Script
        env:
          CONFLUENCE_URL: ${{ secrets.CONFLUENCE_URL }}
          CONFLUENCE_EMAIL: ${{ secrets.CONFLUENCE_EMAIL }}
          CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
        run: python sync_docs.py

      - name: Commit and Push
        run: |
          git config --global user.name "DocSyncBot"
          git config --global user.email "bot@github.com"
          git add docs/
          git commit -m "Automated doc update: $(date)" || exit 0
          git push
