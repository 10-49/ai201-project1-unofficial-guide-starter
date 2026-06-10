# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

--university computer science professor reviews. this knowledge
is valuable because it's absent from any official channels and my school lacks any major online community (like reddit) that has been updated within the last four years. University portal and course catalog provide the sanitized descriptions, while information about specific professors is unknown to students, when a professor can make or break a class. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

--- 13 sources: each source is a raw text extraction of a ratemyprofessor.com page of a CS department professor, including professor general information heading and all listed reviews
eg.
prof_daehan_kwak.txt
prof_lakshmi-devi-subramanian.txt
the sources, in total, encompass hundreds of student reviews covering topics like attendance policy, homework loads, exam difficulty, teaching methodologies, teacher attitude and personality, exam platforms, and other information. 

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

-- a unique approach was considered for this project and the chunking strategy. The approach removes the explicit "chunk-size" and need for an overlap size. 

**Chunk size:**
     --A chunk is consistent with the length of the information contained within a review. 
     Note that RateMyProfessor policy limits reviews to 350 characters, which is the upper limit of any given review. Most reviews fall within the upper range of 300 characters, however the review text is not the only information contained in a review. 
     Other information can includes: professor name, course, overall rating, difficulty rating, grade, extra tags*, would take again*
     The extra included information alongside this usually ranges around 150 characters. 

     total chunk size for a review can max out around 500 characters, average is 350-400. Lowest can be around 125. 
     
     *included at reviewers choice
**Overlap:**
     No overlap. 
**Reasoning:**
     the raw string text from RateMyProfessor website is formatted with lots of needless space and cutoff lines, as well as extra information that is not only uneeded but can actively confuse the semantic reasoning of a model. 
     Such an example is the Helpful upvote and downvote count, or the names of related suggested professors. 

     On top of this, if a standard splitter (say 500 characters) were used, not only would it potentially include this confusing information in chunks unpredictably, but the chunking could fracture individual reviews, which might isolate a students rating from their explanation. it could cause contamination between chunks by bleeding together reviews. This problem is especially pronounced in professors who have students with mixed ratings. 

     the method to avoid these issues was simple:
     process the raw text and clean it. 
     the raw text was processed by a Python parsing script into self-contained strings containing both review and other metadata alongside the review in a neat, understandable format while discarding uneeded information.
     (Professor: X | Course: Y | Rating: Z | Review: Text)

     standard token-reading / character splitting is incompatible with this dataset, which can be an upscaling issue. This dataset originally was supposed to include other course information but would require a combination of a different chunking strategy and it's out of the scope for time reasons.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
     all-MiniLM-L6-v2, via sentence-transformers (default)
**Top-k:**
     we will retrieve 5 chunks per query, estimated to be enough variance
**Production tradeoff reflection:**
     open ai text-embedding-3-large offers better semantics for the nuanced reviews, and if in production, it also has multilingual support (which this lacks). however, relying on an api introduces latency and computation costs, whereas local guarantees zero cost at the expense of better precision
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

1. Which professor is known for making students copy code without explaining the underlying concepts?
     Professor Lakshmi-Devi Subramanian.
2. What is the common consensus on Daehan Kwak's exams and study materials?
     He provides accurate study guides, and his exams are nearly identical to the review materials.
3. Does Professor Subramanian curve grades for CPS2231?
     No
4. What specific external resource does Professor Kwak recommend his students purchase, and why?
     He recommends purchasing the textbook because it is utilized across all CPS levels at the university.
5. What is Lakshmi-Devi Subramanian's overall difficulty rating according to her profile summary?
     4.6.

^ai utilized for these questions

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. the llm may attempt to calculate averages from the 5 retrieved text chunks over relying on the profile summary chunk, could lead to inaccurate outputs.

2. a query regarding a specific course (ex. "is CPS2231 hard?") might pull highly rated reviews and poorly rated reviews both. the llm may struggle with a definitive answer if the semantic search retrieves opposed opinions without clear metadata weighting.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
Document Ingestion (PYTHON custom parse script) 
→ Chunking (standard split on newline, string manipulation) 
→ Embedding (sentence-transformers (all-MiniLM-L6-v2)) + Vector Store (local chromadb) 
→ Retrieval (chromadb semantic search) 
→ Generation (groq api - (llama-3.3-70b-versatile)) 
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

i utilized ai to help synthesize the plan by providing it examples of the raw rmp text and my predefined logic rules for parsing and cleaning. it helped me generate the extraction script in Python.

i'll provide the cleaned text arrays as input example to the AI and request the explicit ChromaDB init syntax, i expect the output code to establish the local vector database and add the document lists with their corresponding IDs

i will give the ai the sentence-transformers(all-MiniLM-L6-v2) requirements and my database structure, asking it to help write and configure the query function that embeds a users question and executes the semantic search to return the relevant text chunks

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
