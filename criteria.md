# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
My corpus is structured as one CVE per chunk, so four of the five questions should be straightforward exact‑match or metadata‑match retrievals. The only risky one is the Linux kernel privilege‑escalation query, because “privilege escalation” is semantic rather than literal metadata. That makes “4 of 5” realistic without being trivial.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

Each chunk corresponds to a single CVE JSON file, and my generation prompt already injects the source_id into the answer. The only way this fails is if retrieval returns zero chunks, which is rare for in‑scope questions. Because the pipeline always has at least one chunk for in‑scope queries, “all five” is achievable and meaningful.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
Cybersecurity questions often contain terms that appear in my corpus even when the question itself is out‑of‑scope — for example, “kernel,” “OpenSSL,” or “privilege escalation.” This semantic drift causes embeddings for some out‑of‑scope queries to look deceptively similar to in‑scope ones.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks should contain a complete CVE advisory with no truncated sentences, missing metadata fields, or partial JSON fragments.


**Why this target:**
 My ingestion pipeline flattens CVE JSON into a single advisory string. So requiring 4 of 5 complete chunks ensures my chunking strategy is validated without pretending the corpus is perfectly clean.


---

## 5. Your choice

For at least 4 of 5 test questions, the system should surface the correct severity (LOW/MEDIUM/HIGH/CRITICAL) in the final answer.

**Why this target:**
Severity is one of the most important metadata fields for cybersecurity triage, and my pipeline explicitly flattens cvss.severity into the chunk metadata. Because severity is consistently present in nearly all CVE JSON files, the only failure mode is retrieving the wrong CVE. 


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
