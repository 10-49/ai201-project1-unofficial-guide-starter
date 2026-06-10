# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

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

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*


# Kean CS Professor RAG System

## Project Overview
A RAG pipeline designed to provide  grounded answers about computer science professors based on student evaluation data. 

## System Architecture
- **Ingestion Pipeline:** Reads local files from `data/cleaned/`, filters out noise/formatting lines, extracts chunks using deterministic line anchors (`Professor:`), and tracks source document metadata.
- **Vector Database:** Local ChromaDB instance using `all-MiniLM-L6-v2` for 384-dimensional vector space embeddings.
- **Generation & Interface:** Zero-temperature execution loop utilizing Groq's `llama-3.3-70b-versatile` via a lightweight interactive terminal command-line interface.


## Eval Report

### Test Question 1
- **Question:** Which professor is known for making students copy code without explaining the underlying concepts?
- **Expected Answer:** Professor Lakshmi-Devi Subramanian.
- **Actual Response:** Professor Lakshmi-Devi Subramanian 
- **Retrieved From:** `prof_lakshmi-devi_subramanian.txt, patricia morreale, mark karol, yulia kumar`
- **Accuracy Judgment:** Accurate
- note : other professors were included in the retrieved chunks for this
due to the prevelance of this description among multiple reviews
consistent with multiple professors

### Test Question 2
- **Question:** What is the common consensus on Daehan Kwak's exams and study materials?
- **Expected Answer:** Exams are fair if you study the provided materials; notes are crucial.
- **Actual Response:** The consensus is that Daehan Kwak's exams directly align with lecture notes and study guides. Diligent review of provided materials guarantees passing marks.
- **Retrieved From:** `prof_daehan_kwak.txt`
- **Accuracy Judgment:** Accurate

### Test Question 3
- **Question:** Does Professor Subramanian curve grades for CPS2231?
- **Expected Answer:** No.
- **Actual Response:** I do not have enough information in my database to answer this.
- **Retrieved From:** `prof_lakshmi-devi_subramanian.txt`
- **Accuracy Judgment:** Wrong, tricky question though, as it is only explicitly stated in one review, and she has ~15. 

### Test Question 4
- **Question:** What specific external resource does Professor Kwak recommend his students purchase, and why?
- **Expected Answer:** Textbook, utilized throughout other courses
- **Actual Response:** Professor Kwak recommends that students purchase a textbook because it is used throughout all levels of CPS at Kean.
- **Retrieved From:** `prof_daehan_kwak.txt`
- **Accuracy Judgment:** Accurate (Correctly identified missing data within the given context bounds)

### Test Question 5
- **Question:** What is the parking situation near the computer science building?
- **Expected Answer:** The database does not contain this information.
- **Actual Response:** I do not have enough information in my database to answer this.
- **Retrieved From:** None
- **Accuracy Judgment:** Accurate 

---

## Failure Case Analysis

### Symptom & Pipeline Trace
During the evaluation of Test Question 3, the vector store pulled context chunks for multiple unrelated professors alongside the correct target professor. The top matches had distance scores ranging tightly between `0.42` and `0.44`.

### Underlying Technical Cause
The failure traces back directly to the **Embedding & Retrieval Stage**. 

because our chunking strategy splits data at the individual review line level, each chunk has low text density. When a query contains a dense semantic concept like *"curve grades"*, the vector embedding model matches the mathematical representation of that action across the entire vector space. The embedding function prioritized the semantic weight of the word "curve" over the name token `"Subramanian"`. 

Because vector search computes distance across the entire string representation, the name was diluted by the shared keyword context. The LLM managed to filter out the false-positive text chunks during the generation phase, but the raw retrieval stage pulled noisy context.

Alongside this, the term "curve" only appears in a single chunk (review). *noted earlier*

---

## Specification Reflection

### How the Spec Guided Implementation
The structural mapping inside `planning.md` forced a strict enforcement of the chunk limits (targeting between 50 and 2000 total chunks). When the original raw loading script malfunctioned and returned only 13 massive monolithic files, checking against the spec metrics immediately signaled that the delimiter extraction logic was broken.

### Divergence from the Spec
The implementation split from the initial spec regarding **Metadata Handling**. The original plan assumed a basic double-newline (`\n\n`) separation format would isolate reviews naturally. 

During implementation, invisible padding characters caused the original parser to miss the line splits entirely. The pipeline had to be refactored to look for line starts matching the string anchor `Professor:` and, programmatically map a dedicated `{"source": filename}` dictionary structure.

---

## AI Usage Log
- **Prompt provided:** I asked for help constructing the original parsing script to create clean chunks. 
- **AI Output:** It provided the script
-**Human Modification:**


- **Prompt provided:** I asked how to fix a `.split('\n\n')` loop that was returning only 13 total chunks because of hidden spaces inside a pre-formatted text block.
- **AI Output:** It provided a regex pattern to strip lines and isolate empty lines.
- **Human Modification:** I bypassed the complex regex suggestion entirely. my script generated an exact `Professor:` string at the start of every chunk, so i overwrote the AI's idea and wrote a simpler condition: `if line.strip().startswith("Professor:")`. 


- **Prompt provided:** I asked how to satisfy the project requirement of tracking document source names when using ChromaDB collections, since i missed that after moving on to the next step.
- **AI Output:** It gave me code that used automated string splitting inside the main query script to find names.
- **Human Modification:** rejected, because it did not actually save the metadata inside the vector engine itself. i had to modify the core data by splitting the change across two files: altering `load_and_validate_chunks` to return a secondary list of dictionaries (`all_metadatas.append({"source": filename})`), and manually changing the `collection.add()` call in `ingest_to_chroma.py` to accept the `metadatas=metadatas` parameter. Used AI to help deduce the correct path forward for this. 