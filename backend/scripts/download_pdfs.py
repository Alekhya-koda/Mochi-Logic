"""
Download or render a list of URLs into numbered PDF files.
"""

from __future__ import annotations

import argparse
import re
import json
from pathlib import Path
from typing import Iterable

import requests
from playwright.sync_api import sync_playwright

URLS = [
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC8624285/",
    "https://www.england.nhs.uk/wp-content/uploads/2021/03/Good-practice-guide-March-2021.pdf",
    "https://www.sciencedirect.com/science/article/pii/S2352013225000572",
    "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.561091/full",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC11149646/",
    "https://bmjopen.bmj.com/content/bmjopen/15/8/e106214.full.pdf",
    "https://tandfonline.com/doi/full/10.1111/ajpy.12289",
    "https://www.cambridge.org/core/journals/development-and-psychopathology/article/dyadic-resilience-after-postpartum-depression-the-protective-role-of-motherinfant-respiratory-sinus-arrhythmia-synchrony-during-play-for-maternal-and-child-mental-health-across-early-childhood/2BD80384E343653531DA955E0B8DA77D",
    "https://iris.who.int/bitstream/handle/10665/362880/9789240057142-eng.pdf?sequence=1",
    "https://www.nature.com/articles/s41598-025-04781-z",
    "https://hygieiahealth.org/non-violent-communication-matters/",
    "https://www.poppy-therapy.com/blog/communication-habits-successful-couples",
    "https://www.sciencedirect.com/org/science/article/pii/S1929074815001390",
    "https://bayareacbtcenter.com/postpartum-anxiety-2/",
    "https://ergobaby.com/blog/post/talking-to-your-baby-your-family-yourself-with-compassionate-communication",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC8624285/",
    "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.561091/full",
    "https://bmjopen.bmj.com/content/9/7/e030208",
    "https://hygieiahealth.org/non-violent-communication-matters/",
]

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChatKitPDF/1.0; +https://openai.com)",
    "Accept": "application/pdf, text/html;q=0.9, */*;q=0.8",
}


def normalize_url(url: str) -> str:
    url = re.sub(r"\s+", "", url).strip()
    if not url:
        return url
    if not re.match(r"^https?://", url):
        url = "https://" + url
    return url


def is_pdf_url(url: str) -> bool:
    return url.lower().split("?", 1)[0].endswith(".pdf")


def download_pdf(url: str, destination: Path) -> bool:
    resp = requests.get(url, timeout=60, headers=REQUEST_HEADERS)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "").lower()
    if "pdf" in content_type or is_pdf_url(url):
        destination.write_bytes(resp.content)
        return True
    return False


def render_pdf(url: str, destination: Path) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(2000)
        page.emulate_media(media="screen")
        page.pdf(path=str(destination), format="A4", print_background=True)
        browser.close()


def iter_urls(urls: Iterable[str]) -> list[str]:
    normalized = []
    for url in urls:
        norm = normalize_url(url)
        if norm:
            normalized.append(norm)
    return normalized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download or render URLs to PDFs.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory to write fileN.pdf outputs.",
    )
    return parser.parse_args()


def write_manifest(output_dir: Path, urls: list[str]) -> None:
    manifest = []
    for idx, url in enumerate(urls, start=1):
        manifest.append({"file": f"file{idx}.pdf", "url": url})
    path = output_dir / "pdf_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    urls = iter_urls(URLS)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for idx, url in enumerate(urls, start=1):
        filename = f"file{idx}.pdf"
        destination = args.output_dir / filename
        if destination.exists() and destination.stat().st_size > 0:
            print(f"Skipping existing {filename}")
            continue
        try:
            try:
                is_saved = download_pdf(url, destination)
            except Exception as exc:
                print(f"Download failed for {url}: {exc}")
                is_saved = False
            if not is_saved:
                render_pdf(url, destination)
            print(f"{filename} <- {url}")
        except Exception as exc:
            print(f"Failed {url}: {exc}")
    write_manifest(args.output_dir, urls)


if __name__ == "__main__":
    main()
