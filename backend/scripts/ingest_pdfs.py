"""
Embed local PDF files into the JSONL knowledge base for RAG.
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

from openai import OpenAI
from pypdf import PdfReader
from tqdm import tqdm

try:
    from dotenv import load_dotenv
except ImportError:  # Optional dependency for local .env support.
    load_dotenv = None

EMBED_MODEL = "text-embedding-3-small"
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "app" / "data" / "knowledge_base.jsonl"
DEFAULT_PDF_DIR = Path(__file__).resolve().parent.parent / "app" / "data"
DEFAULT_MANIFEST = DEFAULT_PDF_DIR / "pdf_manifest.json"


@dataclass
class Chunk:
    id: str
    url: str
    title: str | None
    text: str
    source_type: str
    chunk_index: int


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


def load_manifest(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    mapping: dict[str, str] = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        file_name = item.get("file")
        url = item.get("url")
        if isinstance(file_name, str) and isinstance(url, str):
            mapping[file_name] = url
    return mapping


def sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"file(\d+)\.pdf$", path.name, re.IGNORECASE)
    if match:
        return (int(match.group(1)), path.name)
    return (10**9, path.name)


def build_chunks(pdf_paths: Iterable[Path], url_map: dict[str, str]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for pdf_path in tqdm(list(pdf_paths), desc="Reading PDFs"):
        try:
            raw = pdf_path.read_bytes()
            text = extract_pdf(raw)
        except Exception as exc:
            print(f"Skipping {pdf_path} due to error: {exc}", file=sys.stderr)
            continue
        url = url_map.get(pdf_path.name, str(pdf_path))
        for idx, chunk_text_block in enumerate(chunk_text(text)):
            chunks.append(
                Chunk(
                    id=str(uuid4()),
                    url=url,
                    title=pdf_path.stem,
                    text=chunk_text_block,
                    source_type="pdf",
                    chunk_index=idx,
                )
            )
    return chunks


def write_jsonl(
    chunks: Iterable[Chunk],
    embeddings: list[list[float]],
    output: Path,
    append: bool,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with output.open(mode, encoding="utf-8") as f:
        for chunk, emb in zip(chunks, embeddings):
            row = asdict(chunk)
            row["embedding"] = emb
            json_line = json.dumps(row, ensure_ascii=False)
            f.write(json_line + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build knowledge base from local PDFs.")
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        default=DEFAULT_PDF_DIR,
        help="Directory containing fileN.pdf outputs.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Optional manifest mapping file names to source URLs.",
    )
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
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to the knowledge base instead of overwriting.",
    )
    return parser.parse_args()


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()

    args = parse_args()
    if not args.pdf_dir.exists():
        print(f"PDF directory not found: {args.pdf_dir}", file=sys.stderr)
        return

    pdf_paths = sorted(args.pdf_dir.glob("file*.pdf"), key=sort_key)
    if not pdf_paths:
        print("No PDFs found to ingest.", file=sys.stderr)
        return

    url_map = load_manifest(args.manifest)
    chunks = build_chunks(pdf_paths, url_map)
    if not chunks:
        print("No text could be extracted from the PDFs.", file=sys.stderr)
        return

    client = OpenAI()
    embeddings = []
    for i in tqdm(range(0, len(chunks), 100), desc="Embedding chunks"):
        batch = chunks[i : i + 100]
        batch_embeddings = embed_texts(client, [c.text for c in batch], args.model)
        embeddings.extend(batch_embeddings)

    write_jsonl(chunks, embeddings, args.output, args.append)
    print(f"Wrote {len(chunks)} chunks to {args.output}")


if __name__ == "__main__":
    main()
