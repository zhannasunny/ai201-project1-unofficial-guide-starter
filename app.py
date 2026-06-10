"""
app.py — Generation and query interface
USF Off-Campus Housing Unofficial Guide

- Loads chunks from ingest.py and embeddings from embed.py
- Retrieves relevant chunks using ChromaDB
- Generates grounded answers using Groq (llama-3.3-70b-versatile)
- Serves a Gradio web interface at http://localhost:7860
"""

import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

from embedding import get_collection, get_embedding_model, retrieve

# ── Setup ─────────────────────────────────────────────────────────────────────

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file.")

groq_client = Groq(api_key=GROQ_API_KEY)
embedding_model = get_embedding_model()
collection = get_collection()

# ── Prompt ────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful assistant for University of South Florida (USF) students 
looking for honest information about off-campus housing near campus.

You must answer ONLY using the information provided in the documents below.
Do NOT use your general knowledge or make up information not found in the documents.
If the documents do not contain enough information to answer the question, say exactly:
"I don't have enough information in my sources to answer that question."

Always be specific — mention complex names, prices, or details when they appear in the documents.
Keep your answer concise and helpful."""


def build_context(chunks):
    """Format retrieved chunks into a numbered context block for the prompt."""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[Document {i} — {chunk['source']}]\n{chunk['text']}")
    return "\n\n".join(context_parts)


def format_sources(chunks):
    """Format source attribution from retrieved chunks."""
    seen = set()
    sources = []
    for chunk in chunks:
        key = chunk["source"]
        if key not in seen:
            seen.add(key)
            sources.append(f"• {chunk['source']} ({chunk['url']})")
    return "\n".join(sources)


# ── Core ask function ─────────────────────────────────────────────────────────

def ask(question):
    """
    Full RAG pipeline:
    1. Retrieve top-k chunks
    2. Build grounded prompt
    3. Generate answer with Groq
    4. Return answer + sources
    """
    if not question.strip():
        return "Please enter a question.", ""

    # Retrieve relevant chunks
    chunks = retrieve(question, embedding_model, collection)

    if not chunks:
        return "No relevant documents found.", ""

    # Build context from retrieved chunks
    context = build_context(chunks)

    # Build the user message
    user_message = f"""Documents:
{context}

Question: {question}

Answer using only the documents above. If the answer isn't in the documents, say so."""

    # Generate answer with Groq
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,  # low temperature for factual, grounded responses
        max_tokens=500,
    )

    answer = response.choices[0].message.content.strip()
    sources = format_sources(chunks)

    return answer, sources


# ── Gradio interface ──────────────────────────────────────────────────────────

def handle_query(question):
    answer, sources = ask(question)
    return answer, sources


with gr.Blocks(title="USF Off-Campus Housing Guide") as demo:
    gr.Markdown("""
    # 🏠 USF Off-Campus Housing Unofficial Guide
    Ask anything about off-campus housing near the University of South Florida.
    Answers are grounded in real student reviews, Reddit threads, and news articles.
    """)

    with gr.Row():
        with gr.Column():
            question_input = gr.Textbox(
                label="Your question",
                placeholder="e.g. What do students say about safety at IQ Apartments?",
                lines=2,
            )
            submit_btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        with gr.Column():
            answer_output = gr.Textbox(
                label="Answer",
                lines=8,
                interactive=False,
            )
        with gr.Column():
            sources_output = gr.Textbox(
                label="Sources",
                lines=8,
                interactive=False,
            )

    # Example questions
    gr.Examples(
        examples=[
            "Why do more students choose to live off-campus than on-campus at USF?",
            "What transportation options are available for students without a car?",
            "What are the most common complaints about off-campus housing near USF?",
            "What amenities do students mention most in off-campus housing reviews?",
            "What factors do students consider when choosing off-campus housing near USF?",
        ],
        inputs=question_input,
    )

    # Wire up button and enter key
    submit_btn.click(handle_query, inputs=question_input, outputs=[answer_output, sources_output])
    question_input.submit(handle_query, inputs=question_input, outputs=[answer_output, sources_output])


if __name__ == "__main__":
    print("Starting USF Off-Campus Housing Guide...")
    print("Open http://localhost:7860 in your browser")
    demo.launch()