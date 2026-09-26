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

import json
import uuid

def _extract_metrics(metrics_list):
    """Pull the first available CVSS score/severity, checking all known versions."""
    for m in metrics_list:
        for key in ("cvssV4_0", "cvssV3_1", "cvssV3_0", "cvssV2_0"):
            if key in m:
                cvss = m[key]
                return cvss.get("baseScore"), cvss.get("baseSeverity"), key
    return None, None, None


def _extract_cwe(problem_types):
    """Return (cweId, description) from the first entry that has one."""
    for pt in problem_types:
        for desc in pt.get("descriptions", []):
            if desc.get("cweId"):
                return desc.get("cweId"), desc.get("description")
    return None, None


def _format_versions(affected_entry):
    """Turn a single affected{} block's version list into a readable string."""
    lines = []
    default_status = affected_entry.get("defaultStatus", "unknown")
    for v in affected_entry.get("versions", []):
        status = v.get("status", default_status)
        version = v.get("version", "unspecified")
        piece = f"version {version}: {status}"
        if v.get("lessThan"):
            piece += f" (up to but not including {v['lessThan']})"
        elif v.get("lessThanOrEqual"):
            piece += f" (up to and including {v['lessThanOrEqual']})"
        if v.get("versionType"):
            piece += f" [{v['versionType']}]"
        lines.append(piece)
    return default_status, lines


def split_documents(documents: list[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []
    index = 0

    for doc in documents:
        try:
            data = json.loads(doc.text)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON: {doc.source}")
            continue

        cve_meta = data.get("cveMetadata", {})
        cve_id = cve_meta.get("cveId")

        # Skip rejected/reserved records — little usable content, pollutes retrieval
        if cve_meta.get("state") != "PUBLISHED":
            continue

        cna = data.get("containers", {}).get("cna", {})
        adp_list = data.get("containers", {}).get("adp", [])

        # English description
        text = None
        for desc in cna.get("descriptions", []):
            if desc.get("lang") == "en":
                text = desc.get("value")
                break
        if not text:
            continue

        # Walk ALL affected entries, not just [0]
        affected_list = cna.get("affected", [])
        vendor = affected_list[0].get("vendor") if affected_list else None
        product = affected_list[0].get("product") if affected_list else None

        version_blocks = []
        for entry in affected_list:
            v = entry.get("vendor", "unknown")
            p = entry.get("product", "unknown")
            default_status, lines = _format_versions(entry)
            if lines:
                version_blocks.append(
                    f"{v} {p} (default status: {default_status}): " + "; ".join(lines)
                )

        # Metrics: check cna.metrics first, then every adp entry
        cvss_score, severity, cvss_version = _extract_metrics(cna.get("metrics", []))
        if cvss_score is None:
            for adp in adp_list:
                cvss_score, severity, cvss_version = _extract_metrics(adp.get("metrics", []))
                if cvss_score is not None:
                    break

        # CWE: check cna.problemTypes first, then every adp entry
        cwe, cwe_desc = _extract_cwe(cna.get("problemTypes", []))
        if cwe is None:
            for adp in adp_list:
                cwe, cwe_desc = _extract_cwe(adp.get("problemTypes", []))
                if cwe is not None:
                    break

        title = cna.get("title")
        references = [r.get("url") for r in cna.get("references", []) if r.get("url")]

        # Build embedded text: description + versions + severity + CWE all folded in,
        # since only `text` gets embedded/searched — metadata alone won't match a query.
        text_parts = [text]
        if title:
            text_parts.insert(0, title)
        if version_blocks:
            text_parts.append("Affected versions: " + " | ".join(version_blocks))
        if severity or cvss_score:
            text_parts.append(f"Severity: {severity or 'unknown'} (CVSS {cvss_version or ''} score: {cvss_score or 'unknown'})")
        if cwe:
            text_parts.append(f"Weakness type: {cwe} {cwe_desc or ''}".strip())

        full_text = "\n\n".join(text_parts)

        chunks.append(
            Chunk(
                chunk_id=cve_id or str(uuid.uuid4()),
                source=doc.source,
                index=index,
                text=full_text,
                produced_by="chunker.py::split_documents",
                metadata={
                    "product": product,
                    "vendor": vendor or "unknown",
                    "severity": severity,
                    "cvss": cvss_score,
                    "cvss_version": cvss_version,
                    "cwe": cwe,
                    "references": "; ".join(references) if references else None,
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
