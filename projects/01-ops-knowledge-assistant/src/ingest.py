"""Document ingestion script.

Usage (from the src directory):

    python ingest.py --corpus ../data/corpus

Expected layout under the corpus path:

    corpus/
      public/
        some-doc.md
      internal/
        runbook-xyz.md
      restricted/
        prod-breakglass.md

Each markdown/text file is turned into one or more chunks and loaded into the
in-memory store used by the skeleton. Later this will write to pgvector.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import List

from retrieval import Chunk, add_chunks, reset_store


SENSITIVITY_FROM_FOLDER = {
    "public": "public",
    "internal": "internal",
    "restricted": "restricted",
}


def chunk_text(text: str, max_chars: int = 800, overlap: int = 100) -> List[str]:
    """Naive character-based chunking. Replace with smarter splitting later."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


def load_file(path: Path, sensitivity: str) -> List[Chunk]:
    content = path.read_text(encoding="utf-8", errors="ignore")
    title = path.stem.replace("-", " ").replace("_", " ").title()
    document_id = hashlib.sha1(str(path).encode()).hexdigest()[:12]

    pieces = chunk_text(content)
    chunks: List[Chunk] = []
    for i, piece in enumerate(pieces):
        chunk_id = f"{document_id}-{i}"
        chunks.append(
            Chunk(
                document_id=document_id,
                chunk_id=chunk_id,
                title=title,
                content=piece,
                sensitivity=sensitivity,
                team="platform",
                version="1.0",
                environment="all",
            )
        )
    return chunks


def ingest_corpus(corpus_path: Path) -> int:
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus path does not exist: {corpus_path}")

    reset_store()
    total = 0

    for folder_name, sensitivity in SENSITIVITY_FROM_FOLDER.items():
        folder = corpus_path / folder_name
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*")):
            if path.suffix.lower() not in {".md", ".txt", ".markdown"}:
                continue
            chunks = load_file(path, sensitivity=sensitivity)
            add_chunks(chunks)
            total += len(chunks)
            print(f"  ingested {path.relative_to(corpus_path)} → {len(chunks)} chunk(s) [{sensitivity}]")

    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest operational documents into the skeleton store")
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "corpus",
        help="Path to the corpus directory",
    )
    args = parser.parse_args()

    print(f"Ingesting from: {args.corpus}")
    count = ingest_corpus(args.corpus)
    print(f"Done. Total chunks loaded: {count}")


if __name__ == "__main__":
    main()
