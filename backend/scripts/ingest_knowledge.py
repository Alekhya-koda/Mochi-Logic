"""
Download domain sources, chunk content, embed with OpenAI, and write a local JSONL
knowledge base consumable by the ChatKit server.

Usage:
    python -m app.scripts.ingest_knowledge --output app/data/knowledge_base.jsonl

You need OPENAI_API_KEY in the environment. By default, the script uses the
curated URLs provided by the user; pass --source-file to override with your own
newline-separated list.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path
from typing import Iterable, Sequence
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from pypdf import PdfReader
from tqdm import tqdm

try:
    from dotenv import load_dotenv
except ImportError:  # Optional dependency for local .env support.
    load_dotenv = None

EMBED_MODEL = "text-embedding-3-small"
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "app" / "data" / "knowledge_base.jsonl"

DEFAULT_SOURCES = [
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
    "https://bmjopen.bmj.com/content/9/7/e030208",
]

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChatKitIngest/1.0; +https://openai.com)",
    "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8",
}


@dataclass
class Chunk:
    id: str
    url: str
    title: str | None
    text: str
    source_type: str
    chunk_index: int


def normalize_url(url: str) -> str:
    url = re.sub(r"\s+", "", url)
    url = url.strip()
    if not url:
        return url
    if not re.match(r"^https?://", url):
        url = "https://" + url
    return url


def load_sources(source_file: str | None, inline_sources: Sequence[str]) -> list[str]:
    sources: list[str] = []
    if source_file:
        path = Path(source_file)
        if not path.exists():
            print(f"Source file {path} not found", file=sys.stderr)
            sys.exit(1)
        with path.open() as f:
            for line in f:
                norm = normalize_url(line)
                if norm:
                    sources.append(norm)
    else:
        sources.extend(inline_sources)
    # Remove duplicates while preserving order
    seen: set[str] = set()
    deduped = []
    for src in sources:
        if src in seen:
            continue
        seen.add(src)
        deduped.append(src)
    return deduped


def is_pdf_url(url: str) -> bool:
    base = url.lower().split("?", 1)[0]
    return base.endswith(".pdf")


def fetch_url(url: str) -> tuple[str, str | None, str]:
    resp = requests.get(url, timeout=30, headers=REQUEST_HEADERS)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "").lower()
    if "pdf" in content_type or is_pdf_url(url):
        text, title = extract_pdf(resp.content), None
        return text, title, "pdf"
    text, title = extract_html(resp.text)
    return text, title, "html"


def extract_html(html: str) -> tuple[str, str | None]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    text = " ".join(s.strip() for s in soup.stripped_strings)
    return text, title


def extract_pdf(raw: bytes) -> str:
    reader = PdfReader(BytesIO(raw))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(pages)


def chunk_text(text: str, max_words: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(max_words - overlap, 1)
    for start in range(0, len(words), step):
        window = words[start : start + max_words]
        if len(window) < 50:
            continue
        chunks.append(" ".join(window))
    return chunks


def embed_texts(client: OpenAI, texts: Sequence[str], model: str) -> list[list[float]]:
    response = client.embeddings.create(model=model, input=list(texts))
    return [item.embedding for item in response.data]


def build_chunks(sources: list[str]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for url in tqdm(sources, desc="Downloading sources"):
        try:
            text, title, source_type = fetch_url(url)
        except Exception as err:
            print(f"Skipping {url} due to error: {err}", file=sys.stderr)
            continue
        for idx, chunk_text_block in enumerate(chunk_text(text)):
            chunks.append(
                Chunk(
                    id=str(uuid4()),
                    url=url,
                    title=title,
                    text=chunk_text_block,
                    source_type=source_type,
                    chunk_index=idx,
                )
            )
    return chunks


def write_jsonl(chunks: Iterable[Chunk], embeddings: list[list[float]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for chunk, emb in zip(chunks, embeddings):
            row = asdict(chunk)
            row["embedding"] = emb
            json_line = json.dumps(row, ensure_ascii=False)
            f.write(json_line + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build local knowledge base from URLs.")
    parser.add_argument("--source-file", help="Path to newline-delimited URLs to ingest.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination JSONL file for the knowledge base.",
    )
    parser.add_argument(
        "--model",
        default=EMBED_MODEL,
        help="Embedding model to use (default: text-embedding-3-small).",
    )
    return parser.parse_args()


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()
    args = parse_args()
    sources = load_sources(args.source_file, DEFAULT_SOURCES)
    if not sources:
        print("No sources to ingest", file=sys.stderr)
        return

    print(f"Ingesting {len(sources)} sources...")
    chunks = build_chunks(sources)
    if not chunks:
        print("No text could be extracted from the provided sources.", file=sys.stderr)
        return

    client = OpenAI()
    embeddings = []
    for i in tqdm(range(0, len(chunks), 100), desc="Embedding chunks"):
        batch = chunks[i : i + 100]
        batch_embeddings = embed_texts(client, [c.text for c in batch], args.model)
        embeddings.extend(batch_embeddings)

    write_jsonl(chunks, embeddings, args.output)
    print(f"Wrote {len(chunks)} chunks to {args.output}")


if __name__ == "__main__":
    main()
