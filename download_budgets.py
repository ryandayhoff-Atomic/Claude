#!/usr/bin/env python3
"""Download all 2026 budgets from Google Sheets as Excel files."""

import os
import re
import urllib.request
import urllib.error
import time

BUDGETS = [
    ("Battlefield", None),
    ("Park Forest", None),
    ("Emerald", None),
    ("Hobbs", None),
    ("Old Foundry", None),
    ("Mt Joy", None),
    ("Telford", None),
    ("Apex - Verona, Ocean City", None),
    ("Storage Solutions", None),
    ("247 & Pilots", None),
    ("Master Key (& annex)", "https://docs.google.com/spreadsheets/d/1xudmOs3siugNvRJJsnSas7w7P6IFgezZEPGlYGrKLgU/edit?usp=sharing"),
    ("Premier", "https://docs.google.com/spreadsheets/d/1jCVVZEeC17jGP0RQJBp8ooIJOfLuhVduOBRwI9Uu12U/edit?usp=sharing"),
    ("TriLink", "https://docs.google.com/spreadsheets/d/12CU1XPOrW5Dbdg6zOmnYzrAYLmmJAO3uvsXsX0IvYKY/edit?usp=sharing"),
    ("Arnold", "https://docs.google.com/spreadsheets/d/1eqIP35y49PKVPw9pFjs8y2OxLPleFN-ZgMzRjDUa22o/edit?usp=sharing"),
    ("Topeka", "https://docs.google.com/spreadsheets/d/1JUSfpADc2AehXHleuWQEcBg7j9neKOgs166CqnMWXNs/edit?usp=sharing"),
    ("Storage Point", "https://docs.google.com/spreadsheets/d/18fa6klTVUsn5UPfsZYITxRpEKbSj0vFK_beKPt0-m4k/edit?usp=sharing"),
    ("Radiant", "https://docs.google.com/spreadsheets/d/17co0hZeo6ziio3m5pkjDBmh3ws6qQsIVJRjOBBPs5Bg/edit?usp=sharing"),
    ("Metco", "https://docs.google.com/spreadsheets/d/1e6OsdIcoE8Doxaw-uWza5VBRWKzvcXSkbuzVOuUkli0/edit?usp=sharing"),
    ("Red Door", "https://docs.google.com/spreadsheets/d/1uNxqDsXIUPvmND6boWRuD1YMOAR2pC2no9PN94xyxi4/edit?usp=sharing"),
    ("Add A Space", "https://docs.google.com/spreadsheets/d/1CfxuToY7zjNNftaS6Bd2xEsCyAKm1GRDdaBgy-_ymxQ/edit?usp=sharing"),
    ("Rox", "https://docs.google.com/spreadsheets/d/1ALVJOWpKcV2889C2j9Khdx9ww5wqtj-MeuW4u5kxQyY/edit?usp=sharing"),
    ("Storage Depot - SSD", "https://docs.google.com/spreadsheets/d/1MCdgjC0UoBSjNEfPlElu8Dk326qg9-SE3hvQLOwkDCg/edit?usp=sharing"),
    ("Storage Depot - SDU", "https://docs.google.com/spreadsheets/d/1aWEg9KVx7yJX5KUHvgOwMZbNDslagWmQDtUA3lDAIWs/edit?usp=sharing"),
    ("LaGrange", "https://docs.google.com/spreadsheets/d/1Z0KQOw_rCvvvPJ1aUNQRSXS0kmgtv_kfKBlOveEo4l0/edit?usp=sharing"),
    ("Modbox", "https://docs.google.com/spreadsheets/d/1QaXTaQAuZhC8MKcPEYF2HKNxPjH4G4sYmViwlxBQ3FA/edit?usp=drive_link"),
    ("High Country", "https://docs.google.com/spreadsheets/d/1onNGrVQd4dk-iV2ueZpeDTZdz5-CKw0mzp2kzHFL9mE/edit?usp=sharing"),
    ("Harte", "https://docs.google.com/spreadsheets/d/1_t_3m_QpC4YnXatUYvS27SMXMYXv1JV6n3rf2oEVSoQ/edit?usp=sharing"),
    ("Storage Depot - GLS", "https://docs.google.com/spreadsheets/d/1v-Apl1k4nV9Wn5zjvNdLI5ksH5XJxkQqUXv8c8pyLZ0/edit?usp=sharing"),
    ("Storage Depot - TSP", "https://docs.google.com/spreadsheets/d/1QYKjTVFvzw5jAEsIUcyGWaBGR-pBG4U7rj4cKwnGuTs/edit?usp=sharing"),
    ("Premiere Fargo", "https://docs.google.com/spreadsheets/d/1tEr5VuQXivPfPQxvkHShWfsiltAHdX5xXvu_TT-FJWc/edit?usp=sharing"),
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "budgets_2026")


def extract_sheet_id(url):
    """Extract the Google Sheets ID from a URL."""
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None


def download_as_xlsx(name, url, output_dir):
    """Download a Google Sheet as an Excel file."""
    sheet_id = extract_sheet_id(url)
    if not sheet_id:
        print(f"  SKIP: Could not extract sheet ID from {url}")
        return False

    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    safe_name = re.sub(r'[^\w\s\-&()]', '', name).strip()
    filename = f"{safe_name} - 2026 Budget.xlsx"
    filepath = os.path.join(output_dir, filename)

    try:
        req = urllib.request.Request(export_url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; budget-downloader/1.0)'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            with open(filepath, 'wb') as f:
                f.write(data)
            size_kb = len(data) / 1024
            print(f"  OK: {filename} ({size_kb:.1f} KB)")
            return True
    except urllib.error.HTTPError as e:
        print(f"  FAIL: {filename} - HTTP {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"  FAIL: {filename} - {e}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(BUDGETS)
    with_links = [(n, u) for n, u in BUDGETS if u]
    without_links = [n for n, u in BUDGETS if not u]

    print(f"Found {total} budget to-dos ({len(with_links)} with Google Sheet links, {len(without_links)} without)")
    print()

    if without_links:
        print("Properties WITHOUT budget links (no Google Sheet in description):")
        for name in without_links:
            print(f"  - {name}")
        print()

    print(f"Downloading {len(with_links)} budgets as Excel files...")
    print()

    success = 0
    failed = 0
    for name, url in with_links:
        print(f"Downloading: {name}")
        if download_as_xlsx(name, url, OUTPUT_DIR):
            success += 1
        else:
            failed += 1
        time.sleep(0.5)  # Be respectful to Google's servers

    print()
    print(f"Done! {success} downloaded, {failed} failed")
    print(f"Files saved to: {OUTPUT_DIR}")

    if without_links:
        print(f"\nNote: {len(without_links)} properties had no budget link attached in Basecamp.")


if __name__ == "__main__":
    main()
