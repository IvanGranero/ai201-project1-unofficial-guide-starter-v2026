"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document
from typing import Dict, Any


@dataclass
class Chunk:
    """One piece of one CVE document."""

    chunk_id: str                 # CVE ID or UUID
    source: str                   # filename it came from
    index: int                    # index within that file
    text: str                     # CVE description text
    produced_by: str              # function that made it
    metadata: Dict[str, Any]      # product, severity, cvss, cwe

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"

def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks

def split_documents(documents: list[Document]) -> list[Chunk]:
    import json
    import uuid

    chunks: list[Chunk] = []
    index = 0

    for doc in documents:
        try:
            data = json.loads(doc.text)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON: {doc.source}")
            continue

        # Extract CVE ID
        cve_id = data.get("cveMetadata", {}).get("cveId", None)

        # Extract description (English only)
        descriptions = (
            data.get("containers", {})
            .get("cna", {})
            .get("descriptions", [])
        )
        text = None
        for desc in descriptions:
            if desc.get("lang") == "en":
                text = desc.get("value")
                break

        if not text:
            continue

        # Extract metadata (vendor, product, severity, CWE, CVSS)
        affected = (
            data.get("containers", {})
            .get("cna", {})
            .get("affected", [])
        )
        vendor = None
        product = None
        if affected:
            vendor = affected[0].get("vendor")
            product = affected[0].get("product")

        metrics = (
            data.get("containers", {})
            .get("adp", [{}])[0]
            .get("metrics", [])
        )
        cvss_score = None
        severity = None
        cwe = None
        if metrics:
            cvss = metrics[0].get("cvssV3_1", {})
            cvss_score = cvss.get("baseScore")
            severity = cvss.get("baseSeverity")

            problem_types = (
                data.get("containers", {})
                .get("adp", [{}])[0]
                .get("problemTypes", [])
            )
            if problem_types:
                cwe = problem_types[0]["descriptions"][0].get("cweId")

        # Build chunk
        chunks.append(
            Chunk(
                chunk_id=cve_id or str(uuid.uuid4()),
                source=doc.source,
                index=index,
                text=text,
                produced_by="chunker.py::split_documents",
                metadata={
                    "product": product,
                    "vendor": vendor or "unknown",                    
                    "severity": severity,
                    "cvss": cvss_score,
                    "cwe": cwe,
                },
            )
        )
        index += 1
    return chunks

def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )

if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents("CVE_2026"))
    print(describe(chunks))
