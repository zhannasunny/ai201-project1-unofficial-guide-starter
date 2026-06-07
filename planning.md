# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Domain - University of South Florida Off-Campus Housing Guide

This knowledge is hard to find in one place because it is scattered across apartment review sites, Reddit threads, student-run listing aggregators, and word-of-mouth. Official university resources only list housing options — they don't tell you that one complex has chronic maintenance issues, that a particular neighborhood floods in summer, or that the Bull Runner bus stops running at a certain hour. The gap between what landlords advertise and what students actually experience is exactly what this system fills
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | USF Off-Campus Housing Search| USF-run listing portal; includes real student reviews on each property page — both positive and negative | https://offcampushousing.usf.edu |
| 2 | Apartments for Bulls | Student-run aggregator specific to USF; listings, pricing, neighborhood descriptions written for Bulls | https://www.apartmentsforbulls.com | 
| 3 | Reddit USF community | Student-to-student housing advice threads; search "off campus," "apartment," "where to live" | https://www.reddit.com/r/USF |
| 4 | The Oracle Article | USF's student newspaper; covers housing affordability, on-campus shortages, off-campus market conditions | https://www.usforacle.com/2023/11/30/tampa-rent-prices-keep-rising-how-are-usf-students-managing |
| 5 | USF Oracle | Covers the on-campus shortage (7,200 applicants, 6,400 beds) and links to rent reporting | https://www.usforacle.com/2024/03/21/a-bulls-guide-to-applying-for-housing-this-year |
| 6 | Apartments.com | Neutral third-party; covers Fletcher Ave corridor, bus system context, neighborhood notes | https://www.apartments.com/off-campus-housing/fl/tampa/university-of-south-florida-at-tampa-tampa-campus |
| 7 | Niche.com | Resident-written neighborhood reviews for the area directly adjacent to USF; covers safety, commute, cost | https://www.niche.com/places-to-live/temple-terrace-hillsborough-fl |
| 8 | Google reviews | General reviews (mostly real) about USF off-campus complexes. Search the most popular compexes | https://www.google.com |
| 9 | Yelp | General reviews (mostly real) about USF off-campus complexes. Search the most popular compexes | https://www.yelp.com |
| 10 | USF Bull Runner Transit | Official bus routes, stops, and hours; essential for evaluating any apartment by transit access | https://www.usf.edu/administrative-services/parking/transportation/bull-runner |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
