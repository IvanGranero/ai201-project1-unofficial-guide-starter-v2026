# The Unofficial Guide

Ivan Granero. I picked my own corpus extracted from https://www.cve.org/Downloads

---

# Unit 1

## What This Does

CORPUS: Cybersecurity Vulnerabilities and advisories
I built my system on a corpus of CVE vulnerability records, which are short, structured security advisories published by vendors and the NVD. The system answers questions that ask about specific CVE IDs, vulnerabilities affecting a particular product or version, or descriptions of issues such as buffer overflows, misconfigurations, or denial‑of‑service conditions. Because CVE entries follow a consistent format but vary widely in the kinds of vulnerabilities they describe, the corpus supports both precise lookups and semantic searches grounded in the text.

## Chunking Strategy

**Chunk size:**
Variable size chunk, I will parse each Vulnerability entry and embed as a single chunk.

**Overlap:**
No overlap

**What about YOUR documents made you pick these numbers?**
Keeps each advisory intact (CVE description + metadata).
More natural for structured data (CVE entries, API docs, JSON feeds).
Reduces preprocessing complexity — one CVE = one chunk.

## Sample Chunks

**Chunk 1** — source: CVE-2026-5107.json`` — produced by:split_documents``
Chunk(chunk_id='f326b030-aa62-4269-af4b-be52b100ae1e', source='CVE-2026-5107.json', index=0, text='A vulnerability has been found in FRRouting FRR up to 10.5.1. This affects the function process_type2_route of the file bgpd/bgp_evpn.c of the component EVPN Type-2 Route Handler. The manipulation leads to improper access controls. The attack can be initiated remotely. The attack is considered to have high complexity. The exploitability is reported as difficult. The identifier of the patch is 7676cad65114aa23adde583d91d9d29e2debd045. To fix this issue, it is recommended to deploy a patch.', produced_by='chunker.py::split_documents', metadata={'product': 'FRR', 'severity': None, 'cvss': None, 'cwe': None})
```
```

**Chunk 2** — source: CVE-2026-5007.json`` — produced by:split_documents``
Chunk(chunk_id='2da3aacd-98c1-49f3-9004-b5b857468f04', source='CVE-2026-5007.json', index=1, text='A vulnerability was identified in kazuph mcp-docs-rag up to 0.5.0. Affected is the function cloneRepository of the file src/index.ts of the component add_git_repository/add_text_file. The manipulation leads to os command injection. The attack needs to be performed locally. The exploit is publicly available and might be used. The project was informed of the problem early through an issue report but has not responded yet.', produced_by='chunker.py::split_documents', metadata={'product': 'mcp-docs-rag', 'severity': None, 'cvss': None, 'cwe': None})
```
```

**Chunk 3** — source: CVE-2026-5445.json`` — produced by:split_documents``
Chunk(chunk_id='6e8db3df-a8fb-4d6d-8538-774cbb3f9e0a', source='CVE-2026-5445.json', index=2, text='An out-of-bounds read vulnerability exists in the `DecodeLookupTable` function within `DicomImageDecoder.cpp`. The lookup-table decoding logic used for `PALETTE COLOR` images does not validate pixel indices against the lookup table size. Crafted images containing indices larger than the palette size cause the decoder to read beyond allocated lookup table memory and expose heap contents in the output image.', produced_by='chunker.py::split_documents', metadata={'product': 'DICOM Server', 'severity': 'CRITICAL', 'cvss': 9.1, 'cwe': None})
```
```

**Chunk 4** — source: CVE-2026-5321.json`` — produced by: split_documents``
Chunk(chunk_id='0b450275-9e75-4dd1-a69f-79b81fbb5ec6', source='CVE-2026-5321.json', index=3, text='A flaw has been found in vanna-ai vanna up to 2.0.2. Affected by this issue is some unknown functionality of the component FastAPI/Flask Server. Executing a manipulation can lead to permissive cross-domain policy with untrusted domains. The attack can be launched remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.', produced_by='chunker.py::split_documents', metadata={'product': 'vanna', 'severity': None, 'cvss': None, 'cwe': None})
```
```

**Chunk 5** — source: CVE-2026-5146.json`` — produced by: split_documents``
Chunk(chunk_id='42f196b6-e5ce-4ac0-9c79-d348c8f74d02', source='CVE-2026-5146.json', index=4, text='Improper access control in the notification management endpoints in Devolutions Server allows an unauthenticated attacker to modify or delete arbitrary user notification records via missing session validation.\n\n\n\nThis issue affects the following versions :\n\n  *  \n\nDevolutions Server 2026.1.6.0 through 2026.1.15.0\n\n\n  *  \n\nDevolutions Server 2025.3.19.0 and earlier', produced_by='chunker.py::split_documents', metadata={'product': 'Server', 'severity': 'MEDIUM', 'cvss': 4.3, 'cwe': None})
```
```

## Sample Answer

**Question:**
Question: Show me vulnerabilities affecting OpenSSL 3.0.2

**Answer:**
Based on the provided documents, libtpms versions 0.10.0 and 0.10.1 contain a vulnerability in their integration with OpenSSL 3.x related to the returned IV when certain symmetric ciphers are used (CVE-2026-21444.json).

Sources retrieved: CVE-2026-21444.json, CVE-2026-2184.json, CVE-2026-34054.json, CVE-2026-41676.json, CVE-2026-41677.json
```
```

**My relevance cutoff:**
0.5

| Question                                                         | In corpus? | Best distance |
|------------------------------------------------------------------|------------|---------------|
| What is CVE‑2026‑0005?                                           | No         | 0.293         |
| Show me vulnerabilities affecting OpenSSL 3.0.2                  | No         | 0.427         |
| Are there privilege escalation vulnerabilities in Linux kernel 6 | No         | 0.362         |
| CVEs describing denial‑of‑service in Apache HTTP Server          | Yes        | 0.360         |
| CVE‑2026‑0123                                                    | No         | 0.389         |
| What is the average lifespan of a blue whale                     | No         | 0.802         |
| How do I bake a sourdough loaf with a crispy crust               | No         | 0.797         |
| Who painted The Garden of Earthly Delights                       | No         | 0.757         |
| What is the orbital period of Jupiter around the Sun             | No         | 0.750         |
| How do I solve a quadratic equation using the factoring method   | No         | 0.811         |


## How I Used AI

**1.** 
I asked AI to help me separate my own CVE monolithic split_documents() function into a clean two‑stage pipeline that matches the course architecture: load_documents() for raw file ingestion and split_documents() for JSON parsing and chunk creation. The AI produced a full rewrite that loaded JSON files into Document objects and then parsed them into Chunk objects. I kept the structure but changed several details: I corrected how CVE IDs were extracted, restored my metadata fields (product, severity, cvss, cwe), and added my own defaults for missing values so the chunk schema stayed consistent across the corpus.

**2.**
I used AI to evaluate whether my system instruction was strict enough for a CVE corpus after seeing a drifted answer (“OpenSSL 3.x” instead of “OpenSSL 3.0.2”). The AI proposed a stricter version that forbade inference beyond literal text. I adopted the core rule — “only answer if the exact product/version appears in the documents” — but tightened it further by adding my own constraint: semantic neighbors like “OpenSSL bindings,” “OpenSSL providers,” or “OpenSSL 1.1.x” must not be treated as matches. This ensured the model refuses near‑miss queries instead of stretching the meaning of the documents.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->
**Stretch features**
Metadata filtering — let people search results by CVE ID.

I added support for retrieving CVE entries directly by ID instead of relying only on semantic similarity. Initially, typing a CVE number (e.g., CVE‑2026‑0123) returned “I don’t have enough information,” even though the document existed. The root cause was that CVE IDs were not embedded into the document text, so pure semantic search could not match them. I fixed this by switching to a hybrid search: exact‑match retrieval when a CVE ID is present in the query, and semantic search otherwise. This ensures CVE‑ID queries always return the correct advisory.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
