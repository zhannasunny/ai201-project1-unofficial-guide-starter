"""
ingest.py — Document ingestion and chunking pipeline
USF Off-Campus Housing Unofficial Guide

Chunking strategy (from planning.md):
- Reviews (Reddit, Google Reviews, Niche): 1000 char max, one review per chunk, no overlap
- Articles (Oracle): 500 char chunks, 100 char overlap
- Structured text (Bull Runner .txt): one section per chunk, no overlap

Sources that are JavaScript-rendered (Reddit, Google Reviews, Niche) must be saved
manually as .txt files in the documents/ folder before running this script.
Sources that are plain HTML articles (Oracle) will be fetched and parsed automatically.
"""

import os
import re
import requests
from bs4 import BeautifulSoup

# ── Configuration ────────────────────────────────────────────────────────────

DOCUMENTS_DIR = "documents"

# Oracle article URLs to fetch automatically
ARTICLE_SOURCES = [
    {
        "url": "https://www.usforacle.com/2023/11/30/tampa-rent-prices-keep-rising-how-are-usf-students-managing",
        "source": "oracle_rent_article",
        "source_type": "article",
    },
    {
        "url": "https://www.usforacle.com/2024/03/21/a-bulls-guide-to-applying-for-housing-this-year",
        "source": "oracle_housing_guide",
        "source_type": "article",
    },
]

# Local .txt files and their metadata
# Each file should contain one item per line (one review, one comment, one route)
# Separate items with a blank line
LOCAL_SOURCES = [
    {
        "filename": "reddit_thread_off_campus_living.txt",
        "source": "reddit_off_campus_living",
        "source_type": "reddit",
        "url": "https://www.reddit.com/r/USF/comments/1nhb419/off_campus_living",
    },
    {
        "filename": "reddit_thread_best_areas.txt",
        "source": "reddit_best_areas",
        "source_type": "reddit",
        "url": "https://www.reddit.com/r/USF/comments/1cw3v52/what_are_the_best_areas_to_live_in_tampa_close_to",
    },
    {
        "filename": "google_reviews_the_standard.txt",
        "source": "google_reviews_the_standard",
        "source_type": "google_review",
        "url": "https://maps.google.com/?cid=the_standard_tampa",
    },
    {
        "filename": "google_reviews_college_town.txt",
        "source": "google_reviews_college_town",
        "source_type": "google_review",
        "url": "https://maps.google.com/?cid=college_town_usf",
    },
    {
        "filename": "google_reviews_iq_apartments.txt",
        "source": "google_reviews_iq_apartments",
        "source_type": "google_review",
        "url": "https://maps.google.com/?cid=iq_apartments_tampa",
    },
    {
        "filename": "google_reviews_avalon_heights.txt",
        "source": "google_reviews_avalon_heights",
        "source_type": "google_review",
        "url": "https://maps.google.com/?cid=avalon_heights_tampa",
    },
    {
        "filename": "niche_temple_terrace.txt",
        "source": "niche_temple_terrace",
        "source_type": "niche_review",
        "url": "https://www.niche.com/places-to-live/temple-terrace-hillsborough-fl",
    },
    {
        "filename": "bull_runner.txt",
        "source": "bull_runner_transit",
        "source_type": "transit",
        "url": "https://www.usf.edu/administrative-services/parking/transportation/bull-runner",
    },
]

# ── Cleaning ─────────────────────────────────────────────────────────────────

def clean_text(text):
    """Remove HTML artifacts, extra whitespace, and boilerplate."""
    # Remove HTML tags if any slipped through
    text = re.sub(r"<[^>]+>", "", text)
    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'").replace("&quot;", '"')
    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


# ── Chunking ─────────────────────────────────────────────────────────────────

def chunk_reviews(text, max_chars=1000):
    """
    One review = one chunk. Reviews are separated by blank lines.
    If a single review exceeds max_chars, it is kept as-is (don't split mid-review).
    """
    raw_chunks = re.split(r"\n\s*\n", text)
    chunks = []
    for chunk in raw_chunks:
        chunk = chunk.strip()
        if len(chunk) > 0:
            chunks.append(chunk)
    return chunks


def chunk_article(text, chunk_size=500, overlap=100):
    """
    Sliding window chunking for article text.
    Tries to break at sentence boundaries within the window.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:].strip())
            break
        # Try to break at a sentence boundary (. ! ?) near the end of the window
        boundary = max(
            text.rfind(". ", start, end),
            text.rfind("! ", start, end),
            text.rfind("? ", start, end),
        )
        if boundary != -1 and boundary > start + (chunk_size // 2):
            end = boundary + 1  # include the punctuation
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap  # step back by overlap amount
    return chunks


def chunk_transit(text):
    """
    One section = one chunk for structured transit data.
    Sections are separated by blank lines (e.g., one route per section).
    """
    raw_chunks = re.split(r"\n\s*\n", text)
    chunks = [c.strip() for c in raw_chunks if c.strip()]
    return chunks


# ── Fetching articles ─────────────────────────────────────────────────────────

def fetch_article(url):
    """Fetch and extract body text from an Oracle article."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove nav, footer, ads, scripts
        for tag in soup(["nav", "footer", "script", "style", "aside", "header"]):
            tag.decompose()

        # Oracle uses article body in <div class="entry-content"> or <article>
        article = soup.find("div", class_="entry-content") or soup.find("article")
        if article:
            text = article.get_text(separator="\n")
        else:
            text = soup.get_text(separator="\n")

        return clean_text(text)
    except Exception as e:
        print(f"  WARNING: Could not fetch {url}: {e}")
        return None


# ── Loading local files ───────────────────────────────────────────────────────

def load_local_file(filename):
    """Load a local .txt file from the documents directory."""
    path = os.path.join(DOCUMENTS_DIR, filename)
    if not os.path.exists(path):
        print(f"  WARNING: File not found: {path} — skipping. Save the content manually first.")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return clean_text(f.read())


# ── Main pipeline ─────────────────────────────────────────────────────────────

def build_chunks():
    """
    Run the full ingestion and chunking pipeline.
    Returns a list of dicts: {text, source, source_type, url}
    """
    all_chunks = []

    # 1. Fetch and chunk Oracle articles
    print("Fetching Oracle articles...")
    for source in ARTICLE_SOURCES:
        print(f"  {source['source']}...")
        text = fetch_article(source["url"])
        if text:
            chunks = chunk_article(text, chunk_size=500, overlap=100)
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "source": source["source"],
                    "source_type": source["source_type"],
                    "url": source["url"],
                    "chunk_index": i,
                })
            print(f"    → {len(chunks)} chunks")

    # 2. Load and chunk local files
    print("\nLoading local documents...")
    for source in LOCAL_SOURCES:
        print(f"  {source['filename']}...")
        text = load_local_file(source["filename"])
        if text is None:
            continue

        source_type = source["source_type"]

        if source_type == "transit":
            chunks = chunk_transit(text)
        else:
            # reddit, google_review, niche_review → one review per chunk
            chunks = chunk_reviews(text, max_chars=1000)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": source["source"],
                "source_type": source_type,
                "url": source["url"],
                "chunk_index": i,
            })
        print(f"    → {len(chunks)} chunks")

    return all_chunks


# ── Inspection ────────────────────────────────────────────────────────────────

def inspect_chunks(chunks, n=5):
    """Print n sample chunks for manual verification."""
    import random
    print(f"\n{'='*60}")
    print(f"CHUNK INSPECTION — {n} random samples from {len(chunks)} total")
    print(f"{'='*60}")
    samples = random.sample(chunks, min(n, len(chunks)))
    for i, chunk in enumerate(samples, 1):
        print(f"\n[Sample {i}]")
        print(f"Source: {chunk['source']} ({chunk['source_type']})")
        print(f"Length: {len(chunk['text'])} chars")
        print(f"Text:\n{chunk['text'][:300]}{'...' if len(chunk['text']) > 300 else ''}")
        print("-" * 40)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    chunks = build_chunks()

    print(f"\nTotal chunks: {len(chunks)}")

    # Warn if chunk count is outside the expected range
    if len(chunks) < 50:
        print("WARNING: Fewer than 50 chunks — chunks may be too large, or some files are missing.")
    elif len(chunks) > 2000:
        print("WARNING: More than 2000 chunks — chunks may be too small.")
    else:
        print("Chunk count looks good.")

    inspect_chunks(chunks, n=5)