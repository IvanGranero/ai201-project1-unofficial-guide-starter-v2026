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

## Deployment Criteria — Shape A: Deploy and Instrument

These five criteria measure the deployed service and the operational layer
added for Shape A. The Unit 1 criteria above remain unchanged as the baseline
for the RAG behavior.

### 1. Public health check includes a ready index

For 10 consecutive checks, one per minute, all 10 authenticated requests to
`https://granero.space/health` return HTTP 200 and JSON with
`"index_ready": true`.

**Why this target:**
An HTTP response alone is not enough: the service can be up while the CVE
index is missing, making every question fail. I require 10 of 10 because the
Droplet and index should stay available throughout this short test. Ten checks
are enough to catch an obvious startup or persistence problem without
pretending this small single-Droplet test establishes a long-term uptime SLA.

### 2. Hosted CVE questions retrieve their expected records

For these five prompts submitted through the public form — “What is
CVE-2026-9022?”, “What is CVE-2026-21444?”, “What is CVE-2026-49975?”, “What
is CVE-2026-6409?”, and “What is CVE-2026-23268?” — at least 4 of 5 responses
return HTTP 200, set `"refused": false`, and include the corresponding exact
filename (`CVE-2026-9022.json`, `CVE-2026-21444.json`,
`CVE-2026-49975.json`, `CVE-2026-6409.json`, or `CVE-2026-23268.json`) in
`sources`.

**Why this target:**
This exercises the entire new online path, from the public form through
retrieval and Gemini generation, with a specific expected source instead of a
subjective judgment about answer quality. I allow one miss because the
external model service or network can fail transiently; fewer than 4 of 5
would mean the deployed path is too inconsistent for a class demo.

### 3. Authentication protects both the page and API

Over HTTPS, requests without credentials to `GET /` and `POST /ask` both
return HTTP 401. With the shared class login, `GET /` returns HTTP 200.

**Why this target:**
Protecting only the page would leave the API callable directly and could let
unauthorized users consume my Gemini quota. These three checks cover both
entry points and confirm authorized classmates can reach the form; anything
less leaves an important access path untested.

### 4. Rejected input is both returned and logged

On a `POST /ask` with JSON `{"question":""}`, the service returns HTTP 400 and
the systemd journal contains a matching request record with status 400 and
`"outcome":"invalid_input"`; the log's request ID matches the response's
`X-Request-ID` header.

**Why this target:**
Empty input is a deterministic bad path that should be rejected before
retrieval or a model call. I require the response and log to agree on the
failure so it cannot disappear as an unexplained missing answer. One
reproducible test is sufficient for this deterministic validation path.

### 5. Every measured request has usable instrumentation

For 10 sequential successful `POST /ask` requests, each response has exactly
one matching JSON journal entry containing its request ID, status code 200,
numeric non-negative `duration_ms`, and `"outcome":"answered"`.

**Why this target:**
The request ID and outcome make individual successes traceable, while
duration lets me measure request time. Ten entries provide a small repeatable
sample; a smaller sample could be dominated by one cold request, and a much
larger sample would add API usage without being necessary for this class
deployment check. Requiring exactly one matching entry makes missing or
duplicate logs visible.

### Post-baseline follow-up — Criterion 4 tightened

**Original Criterion 4 (kept unchanged above):** An empty-string question
returns HTTP 400 and has a matching `invalid_input` journal record.

**Follow-up target:** In each run, both `{"question":""}` and
`{"question":123}` return HTTP 400, and each response's `X-Request-ID` has
exactly one matching journal record with status 400 and
`"outcome":"invalid_input"` (2/2 cases).

**Reason:** The original three runs established that empty strings were
handled, but they did not test the JSON value's type. A local pre-change
check showed that a numeric question raised an `AttributeError` in
`serve.py::ask` instead of being rejected as invalid input.
