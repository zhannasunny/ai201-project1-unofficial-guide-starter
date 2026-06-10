"""
embed.py — Embedding and retrieval pipeline
USF Off-Campus Housing Unofficial Guide

- Embeds all chunks from ingest.py using all-MiniLM-L6-v2
- Stores them in ChromaDB with source metadata
- Provides a retrieve() function for querying the vector store
"""

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import build_chunks

# ── Configuration ─────────────────────────────────────────────────────────────

COLLECTION_NAME = "usf_housing"
CHROMA_PATH = "chroma_db"  # local folder where ChromaDB stores data
TOP_K = 5                  # number of chunks to retrieve per query
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ── Setup ─────────────────────────────────────────────────────────────────────

def get_collection():
    """Return the ChromaDB collection, creating it if it doesn't exist."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # cosine similarity for text
    )
    return collection


def get_embedding_model():
    """Load the sentence-transformers embedding model."""
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    return SentenceTransformer(EMBEDDING_MODEL)


# ── Embedding and storing ─────────────────────────────────────────────────────

def embed_and_store(chunks, model, collection):
    """
    Embed all chunks and store them in ChromaDB.
    Skips embedding if the collection already has documents.
    """
    existing = collection.count()
    if existing > 0:
        print(f"Collection already has {existing} chunks — skipping re-embedding.")
        print("Delete the chroma_db/ folder and re-run to rebuild from scratch.")
        return

    print(f"Embedding {len(chunks)} chunks...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    # ChromaDB requires string IDs
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # Metadata stored alongside each chunk
    metadatas = [
        {
            "source": chunk["source"],
            "source_type": chunk["source_type"],
            "url": chunk["url"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB.")


# ── Retrieval ─────────────────────────────────────────────────────────────────

def retrieve(query, model, collection, top_k=TOP_K):
    """
    Retrieve the top-k most relevant chunks for a query.
    Returns a list of dicts with text, metadata, and distance score.
    """
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "source_type": results["metadatas"][0][i]["source_type"],
            "url": results["metadatas"][0][i]["url"],
            "distance": round(results["distances"][0][i], 4),
        })

    return chunks


# ── Test retrieval ─────────────────────────────────────────────────────────────

def test_retrieval(model, collection):
    """Run 3 test queries and print results for manual verification."""
    test_queries = [
        "What do students say about safety near USF apartments?",
        "How do students without a car get to USF campus?",
        "What are common complaints about off-campus housing management?",
    ]

    print("\n" + "=" * 60)
    print("RETRIEVAL TEST")
    print("=" * 60)

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        results = retrieve(query, model, collection)
        for i, chunk in enumerate(results, 1):
            print(f"  [{i}] distance={chunk['distance']} | source={chunk['source']}")
            print(f"      {chunk['text'][:200]}...")
        print()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Load chunks from ingestion pipeline
    chunks = build_chunks()

    # Load embedding model
    model = get_embedding_model()

    # Set up ChromaDB
    collection = get_collection()

    # Embed and store
    embed_and_store(chunks, model, collection)

    # Test retrieval
    test_retrieval(model, collection)
