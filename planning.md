# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Domain - University of South Florida Off-Campus Housing Guide

This knowledge is valuable and hard to find through official channels because the official university website only lists the apartments, not how it is to live there. Even if you find an apartment through university's official channel, and go to their website, it will be super polished and would only tell you the advantages of living there. It won't tell you the negatives: how old the apartment is, if the management cares about residents, if they have pest problems, if the the area gets flooded, and so on. It is very hard to find real student's experiences like that. It is spread across google reviews, reddit threads, yelp, and word of the mouth. There is a big gap in between what the official channels tell you and what the actual experience is.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit USF community thread | Student-to-student housing advice thread and opinions on different complexes | https://www.reddit.com/r/USF/comments/1nhb419/off_campus_living |
| 2 | The Oracle Article | USF's student newspaper; covers housing affordability, on-campus shortages, off-campus market conditions | https://www.usforacle.com/2023/11/30/tampa-rent-prices-keep-rising-how-are-usf-students-managing |
| 3 | USF Oracle | Covers the on-campus shortage (7,200 applicants, 6,400 beds) and links to rent reporting | https://www.usforacle.com/2024/03/21/a-bulls-guide-to-applying-for-housing-this-year |
| 4 | Niche reviews of Temple Terrace area | Reviews from public living around Temple Terrace area (where the university is located). Positive and negative experiences | https://www.niche.com/places-to-live/temple-terrace-hillsborough-fl |
| 5 | Google Reviews for "The Standard" | Reviews from public (and students) about USF off-campus complex "The Standard" | https://www.google.com/maps/place/The+Standard+at+Tampa/@28.0573163,-82.43047,16z/data=!4m8!3m7!1s0x88c2c73ede74f5d9:0x4ac45f9ac1a30afc!8m2!3d28.0573116!4d-82.4278951!9m1!1b1!16s%2Fg%2F11f9j689hj?entry=ttu&g_ep=EgoyMDI2MDYwMS4wIKXMDSoASAFQAw%3D%3D |
| 6 | Google reviews for "College Town @ USF" | Reviews from public (and students) about USF off-campus complex "College Town @ USF" | https://www.google.com/maps/place/College+Town+@+USF/@28.065202,-82.4369001,16z/data=!4m8!3m7!1s0x88c2c7a09d6b8e27:0x7bb7e566ece9ee30!8m2!3d28.0652025!4d-82.43175!9m1!1b1!16s%2Fg%2F1q2vyn6dx?entry=ttu&g_ep=EgoyMDI2MDYwMS4wIKXMDSoASAFQAw%3D%3D |
| 7 | Google reviews for "IQ Apartments" | Reviews from public (and students) about USF off-campus complex "IQ Apartments" | https://www.google.com/maps/place/IQ+Apartments/@28.0623786,-82.4296142,16z/data=!4m8!3m7!1s0x88c2c7a3e409d369:0x775c0d061de76d4a!8m2!3d28.0623739!4d-82.4270393!9m1!1b1!16s%2Fg%2F11cn93700b?entry=ttu&g_ep=EgoyMDI2MDYwMS4wIKXMDSoASAFQAw%3D%3D  |
| 8 | Google reviews for "Avalon Heights" | Reviews from public (and students) about USF off-campus complex "Avalon Heights" | https://www.google.com/maps/place/Avalon+Heights/@28.0702067,-82.4148639,17z/data=!4m8!3m7!1s0x88c2c7949323256b:0xf10bce95453a9788!8m2!3d28.070202!4d-82.412289!9m1!1b1!16s%2Fg%2F1tph2j38?entry=ttu&g_ep=EgoyMDI2MDYwMS4wIKXMDSoASAFQAw%3D%3D |
| 9 | Reddit USF community thread | Reddit discussion about different areas around the university to live in | https://www.reddit.com/r/USF/comments/1cw3v52/what_are_the_best_areas_to_live_in_tampa_close_to |
| 10 | USF Bull Runner Transit | Official bus routes, stops, and hours; essential for evaluating any apartment by transit access | documents/bull_runner.txt | 

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
1000 characters
**Overlap:**
0
**Reasoning:**
For review sources (#1, #4-9) we should use chunk size that equals the whole review without any overlap (one review does not depend on the other -> we don't need overlap to keep the context) 

**Chunk size:**
500 characters
**Overlap:**
100 characters
**Reasoning:**
For oracle articles (#2, #3) we should use shorter chunk size with small overlap to keep the context from other paragraphs (in case it cuts mid-sentence)
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2

**Top-k:**
3

**Production tradeoff reflection:**
I think that if I didn't have constrains, I would consider accuracy to be important. While all-MiniLM-L6-v2 is fast, easy, small, and cheap, accuracy isn't it's strongest quality. I don't think that having multilingual support really matters, because my system should evaluate University of South Florida, where English is the main language (all courses are taught in English). So, if the cost wasn't a concern, I would probably pick bge-large.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Why do more students choose to live in off-campus housing than in on-campus housing?| Students choose to live off-campus primarily because of the shortage of on-campus housing as well as high cost of on-campus housing |
| 2 | What transportation options are available to students who live off-campus near USF and do not own a car? | Students can use Bull Runner, which is a bus that connects campus and surrounding off-campus areas |
| 3 | What are the most common complains about off-campus housing that students who live off-campus have? | Students often complain about poor management, maintainance delays, pest issues, noise, and cleaniness |
| 4 | What amenities do students mention the most in their reviews of off-campus housng at USF? | Students often mention that off-campus housing usually offers gym, pool, and study rooms |
| 5 | What factors do students consider when choosing off-campus housing near USF? | Students usually look at the safety of the area, management quality of the complex, cleaniness, transportation access, and amenities |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Conflicting opinions
Different students may have different views on cleaniness, safety, and convenience. What works for one students doesn't mean it will work for others, and vice versa.

2. Outdated information
Things change very rapidly with off-campus housing. The things that were great at the time of reviews might have changed drastically. Maybe management changed for the worse, prices skyrocketed, or the area became more unsafe than it was less than a year ago. This leads to outdated/incorrect information.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

documents\Architecture.png

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
Claude: I plan to give it domain, documents (sources), and chunking strategy. I will expect it to produce a python script that is able to digest and chunk my sources according to my chunking strategy (reviews and articles should have different chunks). I will verify that the output is correct when it produces good chunks (not too big, not too small, and it has the context around it).

**Milestone 4 — Embedding and retrieval:**
Claude: I will give it the retrieval approach from this document and the pipeline diagram. I will expect it to generate the embedding and retrieval code, which loads chuks from ingestion pipeline, does embedding with all-MiniLM-L6-v2, and stores in ChromaDB with source metadata. I might have to play with number of k. I will verify the result when it returns a chunks with relevant scores (0.8+), which produces specific and on-topic results (make sure there is no off-topic answer or wrong source).

**Milestone 5 — Generation and interface:**
Claude: I will ask it to produce the generation and interface code. My prompt will include my grounding requirements and output format that I want (answer and source list). I will verify the result by making sure the answer is grounded and has a source.
