# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain
 
University of South Florida Off-Campus Housing Guide

This knowledge is valuable and hard to find through official channels because the official university website only lists the apartments, not how it is to live there. Even if you find an apartment through university's official channel, and go to their website, it will be super polished and would only tell you the advantages of living there. It won't tell you the negatives: how old the apartment is, if the management cares about residents, if they have pest problems, if the the area gets flooded, and so on. It is very hard to find real student's experiences like that. It is spread across google reviews, reddit threads, yelp, and word of the mouth. There is a big gap in between what the official channels tell you and what the actual experience is.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit USF community thread | Student-to-student housing advice thread and opinions on different complexes | documents\reddit_thread_off_campus_living.txt |
| 2 | The Oracle Article | USF's student newspaper; covers housing affordability, on-campus shortages, off-campus market conditions | documents\oracle_rent_article.txt |
| 3 | USF Oracle | Covers the on-campus shortage (7,200 applicants, 6,400 beds) and links to rent reporting | documents\oracle_housing_guide.txt |
| 4 | Niche reviews of Temple Terrace area | Reviews from public living around Temple Terrace area (where the university is located). Positive and negative experiences | documents\niche_temple_terrace.txt |
| 5 | Google Reviews for "The Standard" | Reviews from public (and students) about USF off-campus complex "The Standard" | documents\google_reviews_the_standard.txt |
| 6 | Google reviews for "College Town @ USF" | Reviews from public (and students) about USF off-campus complex "College Town @ USF" | documents\google_reviews_college_town.txt |
| 7 | Google reviews for "IQ Apartments" | Reviews from public (and students) about USF off-campus complex "IQ Apartments" | documents\google_reviews_iq_apartments.txt |
| 8 | Google reviews for "Avalon Heights" | Reviews from public (and students) about USF off-campus complex "Avalon Heights" | documents\google_reviews_avalon_heights.txt |
| 9 | Reddit USF community thread | Reddit discussion about different areas around the university to live in | documents\reddit_thread_best_areas.txt |
| 10 | USF Bull Runner Transit | Official bus routes, stops, and hours; essential for evaluating any apartment by transit access | documents/bull_runner.txt | 


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

Review sources:
**Chunk size:**
1000
**Overlap:**
0

Articles:
**Chunk size:**
800
**Overlap:**
200

**Why these choices fit your documents:**
For review sources (#1, #4-9) we should use chunk size that equals the whole review without any overlap (one review does not depend on the other -> we don't need overlap to keep the context). On the other hand, we should use slightly smaller chunk size for the articles. Additionally, we should include an overlap of 200 characters to make sure that the chunk isn't taken out of the context.

**Final chunk count:**
103
---

## Embedding Model

**Model used:**
all-MiniLM-L6-v2

**Production tradeoff reflection:**
all-MiniLM-L6-v2 is a decent local model that is not expensive, doesn't have rate limits, and does not require an API key. That makes it a good choice for this codepath project. For a production deployment, on the other hand, I would consider accuracy, as student language (sland) might not mix so well with this system. For this reason, I would consider bge-large for better accurancy, although highest cost. We don't need multilangual support here because the domain is in the US for a university, where the primary language is English. Finally, API requirement could add reliability and scalability, but it would introduce the need for the API key, which could add additional cost.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Why do more students choose to live in off-campus housing than in on-campus housing? | Students choose to live off-campus primarily because of the shortage of on-campus housing as well as high cost of on-campus housing | According to the documents, students choose to live in off-campus housing because of the "insane rent prices on campus" which make living off campus "more worth it" due to larger spaces, privacy, and more affordable options. Additionally, on-campus housing rates are set to increase annually by 4.5%, with hall rates ranging from $760.50 to $1,287 per month, making off-campus options like College Town and The Standard more affordable. | Partially relevant | Patially accurate |
| 2 | What transportation options are available to students who live off-campus near USF and do not own a car? | Students can use Bull Runner, which is a bus that connects campus and surrounding off-campus areas | According to Document 5, students without a car can use the Bull Runner, USF's free bus service, to get to and from campus at no cost. The Bull Runner connects the main Tampa campus to surrounding off-campus housing complexes, including The Standard and HUB Tampa, and nearby neighborhoods. The routes run Monday through Thursday 7 AM to midnight, Friday 7 AM to 6 PM, and Saturday/Sunday 11 AM to 6 PM. Additionally, Document 4 mentions that Collegetown has 2 stops on the Red bus line, providing another transportation option. | Relevant | Accurate |
| 3 | What are the most common complains about off-campus housing that students who live off-campus have? | Students often complain about poor management, maintainance delays, pest issues, noise, and cleaniness | Based on the documents, the most common complaints about off-campus housing that students who live off-campus have are:
1. High rent prices, with increases ranging from $25 to $200, making it difficult for students to afford (Document 5).
2. Poor maintenance and plumbing issues, such as flooding of bathrooms, as experienced by a student at The Standard (Document 2).
3. Lack of visitor parking, with only 5 visitor spots available at The Standard (Document 2).
4. Dishonest management and excessive fees, as experienced by a student's family at College Town at USF (Document 3).
5. Stress and difficulty in affording rent, with students having to balance schoolwork and part-time jobs to cover living expenses (Document 5). | Relevant | Accurate |
| 4 | What amenities do students mention the most in their reviews of off-campus housing at USF? | Students often mention that off-campus housing usually offers gym, pool, and study rooms | The amenities that students mention the most in their reviews of off-campus housing at USF are the pool, gym, and study rooms, specifically at The Standard. The rooftop pool is mentioned in Document 1, and the pool and gym are mentioned in Document 3. Additionally, the study rooms are mentioned in Document 3 as a great resource for students to do homework. | Relevant | Accurate |
| 5 | What factors do students consider when choosing off-campus housing near USF? | Students usually look at the safety of the area, management quality of the complex, cleaniness, transportation access, and amenities | According to the documents, students consider the following factors when choosing off-campus housing near USF: 
1. Location (ease of getting to campus) - Document 2
2. Amenities - Documents 2 and 3
3. Price (affordability, cheaper than on-campus housing) - Documents 3 and 4
4. Space and privacy - Document 4
5. Community and events - Document 3 
These factors are mentioned in the documents as influencing students' decisions when selecting off-campus housing near the University of South Florida. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**
 Why do more students choose to live in off-campus housing than in on-campus housing?

**What the system returned:**
According to the documents, students choose to live in off-campus housing because of the "insane rent prices on campus" which make living off campus "more worth it" due to larger spaces, privacy, and more affordable options. Additionally, on-campus housing rates are set to increase annually by 4.5%, with hall rates ranging from $760.50 to $1,287 per month, making off-campus options like College Town and The Standard more affordable.

**Root cause (tied to a specific pipeline stage):**
First, let's see what it was supposed to return. Shortage of on-campus housing (mentioned in oracle_housing_article, even though indirectly: "..approximately 7,200 students had applied for on-campus housing for fall 2024. The Tampa campus has around 6,400 beds for students."). Second, it reasoned that the Standard or College Town are more affordable (they are most definetely not - these are more expesive, actually!). 

The fact that the system didn't mention the shortage of on-campus housing is a retrieval failure. This is because the chunk that contained that statistic (7200 students applied but 6400 beds are available) wasn't retrieved as relevant to this question. The system didn't connect these numbers with the shortage and therefore the need for students to live off-campus.

The part where the system said that The Standard or College Town were more affordable is a hallucination. It is a generation/grounding failure. The system saw positive reviews about The Standard and College Town and inferred that they must be more affordable than on-campus husing. It tried to reason. I think it is a grounding failure because the answer sounds correct and specific, but it is not actually supported by the documents I provided.

**What you would change to fix it:**
For the retrieval failure: I would add more context to the oracle_housing_guide article connecting the number of beds available to on-campus shortage.
For the grounding failure: I would make the prompt more strict and tell it to mention specific documents when providing information, as well as not allowing assumptions.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
It really helped me to separate the project into stages. It would also give me something more concrete to work with - like I already laid the foundation, so doing the rest wasn't as hard mentally and physically. Mentally, it is a lot harder to look at the blank page than follow something/modify existing things. Physically, I had to think less about the approach, and could focus on the code.

**One way your implementation diverged from the spec, and why:**
I had to change the Oracle articles from web scraping to manual txt files. The reason is that the web scraping wasn't working properly. It would include unrelated things (photo credit, related articles). Manually scraping allowed me to make sure that it is the article itself that is going into the source.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* 
I asked Claude why my articles were being chunked so terribly even after I manually scraped them into txt files. 
- *What it produced:*
"Since you manually split the articles into good sections with blank lines, chunk_reviews will work perfectly — it just splits on blank lines, same logic. No need for sliding window anymore."
- *What I changed or overrode:*
I did not follow this advice. I played with chuking size and overlap instead. I wanted to follow what I learned in the lecture, and treating the articles the same way I treat reviews seemed wrong.

**Instance 2**

- *What I gave the AI:*
I asked AI to generate ingest.py file
- *What it produced:*
It produced a good ingest.py file overall.
- *What I changed or overrode:*
I had issues with web scraping the articles. I had to move them into local sources instead and manually scrap them into txt. I had to change function calls so that now it would treat articles as local sources.