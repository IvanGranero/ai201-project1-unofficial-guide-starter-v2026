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
| Give me the severity of CVE-2026-0123                            | No         | 0.389         |
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

**3.**
When Criterion 5 kept missing, I initially suspected the prompt. Claude traced the actual root cause back through the CVE JSON schema and my chunker code and showed that severity data never made it into the embedded chunk text at all — it only lived in unused metadata. That reframed the fix from "improve prompting" to "fix the chunker," which a prompt-only fix would never have solved.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->
**Stretch features**
Metadata filtering — let people search results by CVE ID.

I added support for retrieving CVE entries directly by ID instead of relying only on semantic similarity. Initially, typing a CVE number (e.g., CVE‑2026‑0123) returned “I don’t have enough information,” even though the document existed. The root cause was that CVE IDs were not embedded into the document text, so pure semantic search could not match them. I fixed this by switching to a hybrid search: exact‑match retrieval when a CVE ID is present in the query, and semantic search otherwise. This ensures CVE‑ID queries always return the correct advisory.

Second embedding model -

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
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |  
| 2. Every answer names a source | 5 of 5 | 4/5 | 3/5 | 4/5 | MISSED
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks are complete, untruncated | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Correct severity surfaced | 4 of 5 | 1/5 | 1/5 | 1/5 | MISSED |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

Criterion 1 - 
Based on the provided documents, OpenSSL 3.x is explicitly stated as **not affected** by the vulnerabilities described in:
- `CVE-2026-41677.json`
- `CVE-2026-41676.json`

Additionally, the documents do not mention version 3.0.2 specifically, but they do mention an integration of libtpms with OpenSSL 3.x in `CVE-2026-21444.json`. However, that document states the vulnerability is in libtpms versions 0.10.0 and 0.10.1 (not OpenSSL itself). 

Therefore, I don’t have enough information to answer that OpenSSL 3.0.2 is affected by any of the listed vulnerabilities.

Criterion 2 - No sources were mentioned in the actual answer in this example
- Best distance: 0.3621 (passed the gate)
- Sources retrieved: CVE-2026-23268.json, CVE-2026-3006.json, CVE-2026-34855.json, CVE-2026-3609.json, CVE-2026-43206.json

```
I don’t have enough information to answer that.
```

Criterion 3 - Gate stops out of scope questions
run_eval.py::check_out_of_scope`
python app.py ask "What is the average lifespan of a blue whale?" --show-prompt
  (best distance 0.802, cutoff 0.5)

I don't have enough information about that.

Criterion 4 - Chunks are complete, untruncated
Documents:

[from CVE-2026-49975.json]
Metadata: {"chunk_id": "CVE-2026-49975", "index": 18371, "produced_by": "chunker.py::split_documents", "product": "Apache HTTP Server", "source": "CVE-2026-49975.json", "vendor": "Apache Software Foundation"}
Retrieval distance: 0.3602600693702698
Chunk ID: CVE-2026-49975
Text:
Memory Allocation with Excessive Size Value vulnerability in Apache HTTP Server's mod_http leads to denial of service via malicious HTTP requests.

This issue affects Apache HTTP Server: from 2.4.17 through 2.4.67.

[from CVE-2026-6409.json]
Metadata: {"chunk_id": "CVE-2026-6409", "index": 20313, "produced_by": "chunker.py::split_documents", "product": "Protobuf-php (Pecl)", "source": "CVE-2026-6409.json", "vendor": "Protocol Buffers"}
Retrieval distance: 0.4012501835823059
Chunk ID: CVE-2026-6409
Text:
A Denial of Service (DoS) vulnerability exists in the Protobuf PHP library during the parsing of untrusted input. Maliciously structured messages—specifically those containing negative varints or deep recursion—can be used to crash the application, impacting service availability.




## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | 4 out of the 5 questions return chunks with the answer, question 3 provided chunks containing relevant information but not specific to the question.
| 2 | Every answer names a source | MISSED | There were a few runs where the actual answer didn't mention the source. Pobably refining the system prompt will fix this.
| 3 | Gate stops out-of-corpus questions | MET | 5 of the 5 out of scope questions were stop and replied right away.
| 4 | Chunks are complete, untruncated | MET | All retrieved chunks were complete with the full CVE. This is due to having a chunk per CVE not per lines or characters.
| 5 | Correct severity surfaced | MISSED | Severity is only displayed when specifically asked for it.


Original: "Chunks are complete, untruncated" — Target 4 of 5
Revised: "At least 4 of 5 sampled chunks map 1:1 to a single CVE, with no merged or split records"
Why: The original criterion was written to catch truncation, but your chunking strategy (one chunk per CVE, not per line/character) makes truncation structurally impossible. The revised version tests something that actually could go wrong such as a malformed source document causing two CVEs to merge into one chunk, or one CVE getting split across two chunks due to a parsing edge case.

## Diagnoses

Question 2 'Show me vulnerabilities affecting OpenSSL 3.0.2' and Question 3 'Are there privilege escalation vulnerabilities in Linux kernel 6.x?' are not able to match a .x or .* with any number, chunks are provided with relevant information but in most cases there is no version available in the provided chunks, our sources do contain version data however our chunker is skipping them additionally there are no specific instructions in the prompt on how to treat these cases.

## The Improvement

**What I changed:**

A second chunking strategy.
The text I am including to embed only ever holds the CVE description. Version data, CWE description, product/vendor for all affected entries, and severity never make it into the embedded text at all, some live in metadata, which isn't searched, it's just displayed once retrieval already succeeded. So a query like "OpenSSL 3.0.2" has nothing to match against in any chunk unless the description mentions it.

I've rewritten the split_documents function to include more data including version ranges. This fix most probably will fix Criterion 5 as well, since the LLM will now have the severity string in front instead of only in unused metadata.

**Why I picked it:**

Version matching is core to what a CVE retrieval system is for. A vulnerability's whole practical value is knowing whether your version is affected. A CVE RAG that can't match versions can retrieve relevant documents and still give a useless or wrong answer, which is exactly what happened in Q2 and Q3. Fixing this at the chunker level, rather than through prompt tuning, ensures version data is actually searchable rather than just displayed after the fact.


### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |  
| 2. Every answer names a source | 5 of 5 | 4/5 | 5/5 | 4/5 | MISSED
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET
| 4. Chunks are complete, untruncated | 4 of 5 | 5/5 | 5/5 | 5/5 | MET
| 5. Correct severity surfaced | 4 of 5 | 1/5 | 2/5 | 1/5 | MISSED


**Did it help?**

Absolutely, criterion 1 went from 4/5 to 5/5. The clearest win is Question 3 (Linux kernel 6.x): the retrieved chunk for CVE-2026-23268 now explicitly lists version ranges (visible in the model citing "6.1.169, 6.6.130, 6.12.77..." in run 1), which wasn't possible before since versions weren't embedded. This question flipped from "I don't have enough information" (before) to a correctly sourced "Yes" in all 3 runs.


## What's Still Broken

Criterion 2 and 5 is still a missed, Criterion 2 failed a couple of times because the retrieval is not always able to generate a correct response for Question 3, looking at the chunks retrieved there were no chunks with the correct answer pulled in those cases, therefore increasing the top_k from 5 to 10 solved the issue. For Criterion 2 the responses are always available but the answer do not include it because the prompt doesn't have instructions for it, this will be fix by refining the system prompt. These are now fixed on an extra eval run.

## What I'd Do Differently

If I were writing these five criteria from scratch again, I'd revise Criterion 5 ("Correct severity surfaced"). Sounds like a retrieval or generation quality issue, but this whole unit showed it was actually two separate, sequential problems bundled into one number: first, severity wasn't even in the embedded text (a chunking bug), and second, once it was, the model still wouldn't surface it consistently. A single pass/fail criterion couldn't distinguish "the data isn't there" from "the data is there but the model isn't told to use it". Next time I'd split it into two criteria, something like "severity is present in the retrieved chunk text" and "severity is stated in the final answer when present in the chunk", so a failure tells me immediately which half of the pipeline to fix instead of leaving me to diagnose it by hand.

## The System

I chose this RAG because I had already developed it for a CVE corpus and know how its pieces work, from loading and chunking CVE records to vector search, the relevance gate, and answer generation. I have already encountered retrieval problems involving product versions and severity, so I have a good starting point for anticipating failure modes and deciding what to measure when I deploy it.

## The Shape

**A — Deploy and instrument.** I will deploy the existing Flask service so the CVE RAG can answer questions online, keep its Chroma index on persistent storage, and add request logging and timing. I will check that the deployed service is healthy and record how it performs on a few CVE questions. The goal is to make the current system run reliably and visibly in production, not to change how it retrieves or answers.

## Out of Scope

- I am not building a separate frontend framework or a complex interface; the UI is one simple Flask-served form.
- I am not changing the chunking, embeddings, or retrieval strategy.
- I am not adding user accounts or multiple service instances.

## Instrumentation

The deployed service logs each HTTP request as JSON in the systemd journal. These ten successful `/ask` requests and one rejected-input request were collected with `journalctl -u ai201-rag --since "30 minutes ago" -o cat --no-pager`. The logs record request ID, method, path, status, duration, and outcome; they do not include the question or prompt.

Ten answered requests:

```text
{"event":"http_request","request_id":"2abb104765fd402e8c07aeb7acd0df67","method":"POST","path":"/ask","status_code":200,"duration_ms":956.43,"outcome":"answered"}
{"event":"http_request","request_id":"a13345b57edf4ff5a72c893d790c6a40","method":"POST","path":"/ask","status_code":200,"duration_ms":8.77,"outcome":"answered"}
{"event":"http_request","request_id":"b64537f01293477d923edbd9855b8b92","method":"POST","path":"/ask","status_code":200,"duration_ms":9.88,"outcome":"answered"}
{"event":"http_request","request_id":"3c1f671870a0436e861b7da036717d4a","method":"POST","path":"/ask","status_code":200,"duration_ms":9.07,"outcome":"answered"}
{"event":"http_request","request_id":"8ae0de60361848e7bd88dc96468f0807","method":"POST","path":"/ask","status_code":200,"duration_ms":7.73,"outcome":"answered"}
{"event":"http_request","request_id":"6b77261dca5b4d73873bad476b010940","method":"POST","path":"/ask","status_code":200,"duration_ms":8.18,"outcome":"answered"}
{"event":"http_request","request_id":"8ac879afd99840f9bb1bda9ed623080f","method":"POST","path":"/ask","status_code":200,"duration_ms":9.53,"outcome":"answered"}
{"event":"http_request","request_id":"4fddc365884646b982f3254d6ec8f51d","method":"POST","path":"/ask","status_code":200,"duration_ms":7.94,"outcome":"answered"}
{"event":"http_request","request_id":"1f31d46ecffa4272b737ad14efba79f4","method":"POST","path":"/ask","status_code":200,"duration_ms":8.96,"outcome":"answered"}
{"event":"http_request","request_id":"ea2ed88c9e3a43c1b5329af1824fbd7d","method":"POST","path":"/ask","status_code":200,"duration_ms":9.82,"outcome":"answered"}
```

Rejected-input run (empty question, HTTP 400):

```text
{"event":"http_request","request_id":"47c244e1be6843efbae32ec617a19b61","method":"POST","path":"/ask","status_code":400,"duration_ms":0.25,"outcome":"invalid_input"}
```

## What It Costs

In deployment Run 1, the mean end-to-end duration for ten answered HTTP
requests was **349.16 ms**; the median was **8.4 ms**, with a range of
**7.11–1342.07 ms**. Method: arithmetic mean and median of the ten
`duration_ms` values in the systemd journal. This is elapsed request time,
including retrieval, cache lookup, and any model-service wait—not CPU-only
time or billed Gemini token usage.

In deployment Run 2, the ten correlated answered requests had a mean duration
of **8.67 ms**, a median of **8.585 ms**, and a range of **7.68–9.48 ms**.

In deployment Run 3, the ten correlated answered requests had a mean duration
of **8.54 ms**, a median of **8.635 ms**, and a range of **7.86–9.01 ms**.

Run 1's low median and much higher mean suggest that some requests were served
from the response cache, but cache status is not in the request logs. These
measurements describe request latency with caching as configured; they are
not the cost of ten uncached Gemini calls.

## Deployment Run Log — Shape A

All three runs are complete, and each criterion met its target in all three
runs. The Run 3 command reused the Run 2 output filename, so
[run2-client-output.txt](./run2-client-output.txt) now contains Run 3's client
transcript; Run 2's evidence is recorded in this README.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Public health check includes a ready index | 10/10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Hosted CVE questions retrieve their expected records | At least 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Authentication protects both the page and API | Unauthenticated requests: 401; authenticated page: 200 | Pass | Pass | Pass | MET |
| 4. Rejected input is both returned and logged | HTTP 400 and log entry with the same request ID | Pass | Pass | Pass | MET |
| 5. Each answered request has a matching instrumentation event | 10/10 response IDs have exactly one matching log entry | 10/10 | 10/10 | 10/10 | MET |

### Run 1 — actual output

#### Criterion 1 — `serve.py::health`

```text
Check 1: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 2: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 3: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 4: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 5: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 6: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 7: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 8: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 9: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 10: HTTP 200 {"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
```

#### Criterion 2 — `serve.py::ask` → `app.py::ask_pipeline`

```text
HTTP/1.1 200 OK
{"answer":"CVE-2026-9022 is a Stored Cross-Site Scripting vulnerability in the Splide Carousel Block plugin for WordPress (up to and including version 1.7.1) via the 'url' Block Attribute, caused by insufficient input sanitization and output escaping. This allows authenticated attackers with contributor-level access and above to inject arbitrary web scripts. The vulnerability has a MEDIUM severity with a CVSS v3.1 score of 6.4.\n\nSource: CVE-2026-9022.json","best_distance":0.0,"corpus":"CVE_2026","question":"What is CVE-2026-9022?","refused":false,"sources":["CVE-2026-9022.json"],"threshold":0.5}

HTTP/1.1 200 OK
{"answer":"CVE-2026-21444 is a vulnerability in libtpms (versions 0.10.0 and 0.10.1) where the library returns the wrong initialization vector (the initial IV instead of the last IV) to the caller when certain symmetric ciphers are used with OpenSSL 3.x. This weakens subsequent encryption and decryption steps, with the highest threat being to data confidentiality. \n\nSeverity: MEDIUM (CVSS v3.1 score: 5.5)\nWeakness type: CWE-327 (Use of a Broken or Risky Cryptographic Algorithm)\n\nSource: CVE-2026-21444.json","best_distance":0.0,"corpus":"CVE_2026","question":"What is CVE-2026-21444?","refused":false,"sources":["CVE-2026-21444.json"],"threshold":0.5}

HTTP/1.1 200 OK
{"answer":"CVE-2026-49975 is a Memory Allocation with Excessive Size Value vulnerability (CWE-789) in Apache HTTP Server's mod_http2 (mod_http) that leads to a denial of service via malicious HTTP requests. This issue affects Apache HTTP Server versions from 2.4.17 through 2.4.67 (up to and including 2.4.67). \n\nSource: CVE-2026-49975.json","best_distance":0.0,"corpus":"CVE_2026","question":"What is CVE-2026-49975?","refused":false,"sources":["CVE-2026-49975.json"],"threshold":0.5}

HTTP/1.1 200 OK
{"answer":"CVE-2026-6409 is a Denial of Service (DoS) vulnerability in the Protobuf PHP library (Protocol Buffers Protobuf-php (Pecl)) that occurs during the parsing of untrusted input. Maliciously structured messages containing negative varints or deep recursion can crash the application and impact service availability. \n\nThe vulnerability has a HIGH severity with a CVSS cvssV4_0 score of 7.1, and is associated with weakness type CWE-20 (Improper input validation).\n\nSource: CVE-2026-6409.json","best_distance":0.0,"corpus":"CVE_2026","question":"What is CVE-2026-6409?","refused":false,"sources":["CVE-2026-6409.json"],"threshold":0.5}

HTTP/1.1 200 OK
{"answer":"CVE-2026-23268 is a vulnerability in the Linux kernel's apparmor component where an unprivileged local user can perform privileged policy management (loading, replacing, and removing profiles) by opening apparmorfs interfaces via a confused deputy attack, passing the opened file descriptor to a privileged process, and having that privileged process write to the interface. \n\nSeverity: HIGH (CVSS cvssV3_1 score: 7.8)\n\nSource: CVE-2026-23268.json","best_distance":0.0,"corpus":"CVE_2026","question":"What is CVE-2026-23268?","refused":false,"sources":["CVE-2026-23268.json"],"threshold":0.5}
```

#### Criterion 3 — Nginx Basic Auth and `serve.py::home`

```text
GET / run 1: HTTP 401
GET / run 2: HTTP 401
GET / run 3: HTTP 401
POST /ask run 1: HTTP 401
POST /ask run 2: HTTP 401
POST /ask run 3: HTTP 401
GET /: HTTP 200, X-Request-ID=36a1543611a74a208a21429672ccfa59
```

#### Criterion 4 — `serve.py::ask` and `serve.py::log_request`

```text
HTTP/1.1 400 BAD REQUEST
X-Request-ID: 18609d4eb90645a2a5cffac0e0cb8a62
{"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}"}

{"event":"http_request","request_id":"18609d4eb90645a2a5cffac0e0cb8a62","method":"POST","path":"/ask","status_code":400,"duration_ms":0.22,"outcome":"invalid_input"}
```

#### Criterion 5 — `serve.py::log_request`, matched by response ID

```text
{"event":"http_request","request_id":"21b57aef04be4ed1879ec26e357a6f84","method":"POST","path":"/ask","status_code":200,"duration_ms":889.56,"outcome":"answered"}
{"event":"http_request","request_id":"aad3297650da416d9cd74d0011fffeb2","method":"POST","path":"/ask","status_code":200,"duration_ms":1342.07,"outcome":"answered"}
{"event":"http_request","request_id":"7f054c034d7948568da9884cbe7e0507","method":"POST","path":"/ask","status_code":200,"duration_ms":1204.45,"outcome":"answered"}
{"event":"http_request","request_id":"9a564126610f42f8ad2a7a65c4b4729a","method":"POST","path":"/ask","status_code":200,"duration_ms":7.91,"outcome":"answered"}
{"event":"http_request","request_id":"16b86c8aa3ed43f0a447dfa3c7d646a9","method":"POST","path":"/ask","status_code":200,"duration_ms":7.11,"outcome":"answered"}
{"event":"http_request","request_id":"47677ff094a3477ebc0853d771bd7084","method":"POST","path":"/ask","status_code":200,"duration_ms":8.57,"outcome":"answered"}
{"event":"http_request","request_id":"eeeb6b5c3c94411baa7d041f12bd2052","method":"POST","path":"/ask","status_code":200,"duration_ms":7.69,"outcome":"answered"}
{"event":"http_request","request_id":"d9a88c4ccc8a46fdb028d9cd37796a29","method":"POST","path":"/ask","status_code":200,"duration_ms":8.51,"outcome":"answered"}
{"event":"http_request","request_id":"a996570a31a643739bdfb86eead192d7","method":"POST","path":"/ask","status_code":200,"duration_ms":7.41,"outcome":"answered"}
{"event":"http_request","request_id":"2bc911d59b5b4dcc8b140f2e0d64da7d","method":"POST","path":"/ask","status_code":200,"duration_ms":8.28,"outcome":"answered"}
```

### Run 2 — actual output

The full client transcript, including all five CVE response bodies, is saved
in [run2-client-output.txt](./run2-client-output.txt).

#### Criterion 1 — `serve.py::health`

```text
Check 1/10 at 2026-11-15T21:12:12-05:00
Health check 1: HTTP 200, X-Request-ID=2780d5d8e62048f8b9e2fd8948ae373f
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 2/10 at 2026-11-15T21:13:12-05:00
Health check 2: HTTP 200, X-Request-ID=b49831eb365c4112aad9cf8f3769c727
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 3/10 at 2026-11-15T21:14:12-05:00
Health check 3: HTTP 200, X-Request-ID=cad0e17414b84209be979d08c9ed0a62
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 4/10 at 2026-11-15T21:15:12-05:00
Health check 4: HTTP 200, X-Request-ID=507840626e634353b1215d3173e15b39
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 5/10 at 2026-11-15T21:16:12-05:00
Health check 5: HTTP 200, X-Request-ID=8c3c86a475e94c98b16b1591308b73c3
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 6/10 at 2026-11-15T21:17:12-05:00
Health check 6: HTTP 200, X-Request-ID=e55b8451cfe647628d1251f7215c5eb1
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 7/10 at 2026-11-15T21:18:12-05:00
Health check 7: HTTP 200, X-Request-ID=56b6e51b47354868a617fe5343772c4c
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 8/10 at 2026-11-15T21:19:12-05:00
Health check 8: HTTP 200, X-Request-ID=d93ca1ce20414f2a9c0fdc5b5922d44a
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 9/10 at 2026-11-15T21:20:12-05:00
Health check 9: HTTP 200, X-Request-ID=3bf543810603495da32a3593a8652bcc
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 10/10 at 2026-11-15T21:21:12-05:00
Health check 10: HTTP 200, X-Request-ID=92e38f1e98ea499ba027f524fb59e9a7
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Criterion 1 total: 10/10
```

#### Criterion 2 — `serve.py::ask` → `app.py::ask_pipeline`

```text
CVE prompt: What is CVE-2026-9022?: HTTP 200, X-Request-ID=d2449be1d42149a280a307c44d2d2937
Expected CVE-2026-9022.json: PASS
CVE prompt: What is CVE-2026-21444?: HTTP 200, X-Request-ID=4f2f78844703450e9fc11a8a23a8bb92
Expected CVE-2026-21444.json: PASS
CVE prompt: What is CVE-2026-49975?: HTTP 200, X-Request-ID=8750c96f401e4388b2a91d1b82718127
Expected CVE-2026-49975.json: PASS
CVE prompt: What is CVE-2026-6409?: HTTP 200, X-Request-ID=24abde50c11b4b6aa1163356057ec70f
Expected CVE-2026-6409.json: PASS
CVE prompt: What is CVE-2026-23268?: HTTP 200, X-Request-ID=36fc322c696846948d48a2966ed6ff7d
Expected CVE-2026-23268.json: PASS
Criterion 2 total: 5/5 (target: at least 4/5)
```

#### Criterion 3 — Nginx Basic Auth and `serve.py::home`

```text
Unauthenticated GET /: HTTP 401, X-Request-ID=(none)
Unauthenticated POST /ask: HTTP 401, X-Request-ID=(none)
Authenticated GET /: HTTP 200, X-Request-ID=624e072049b440098c9a0cad1686a68b
Criterion 3: PASS (expected 401, 401, 200)
```

#### Criterion 4 — `serve.py::ask` and `serve.py::log_request`

```text
Empty-question POST /ask: HTTP 400, X-Request-ID=ffdfab8563f64ee2a0afaa54a2075ced
{"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}"}

{"event":"http_request","request_id":"ffdfab8563f64ee2a0afaa54a2075ced","method":"POST","path":"/ask","status_code":400,"duration_ms":0.19,"outcome":"invalid_input"}
```

#### Criterion 5 — `serve.py::log_request`, matched by response ID

```text
{"event":"http_request","request_id":"ccb76204b1bb48b6af5a9ae6e78f404a","method":"POST","path":"/ask","status_code":200,"duration_ms":8.42,"outcome":"answered"}
{"event":"http_request","request_id":"9ffadddedbe14d8983b5c083d447a900","method":"POST","path":"/ask","status_code":200,"duration_ms":8.74,"outcome":"answered"}
{"event":"http_request","request_id":"813a5b0f1bf94f76a53dfb555b1249d3","method":"POST","path":"/ask","status_code":200,"duration_ms":8.43,"outcome":"answered"}
{"event":"http_request","request_id":"214b1c884ba345068d2307d6b64a479b","method":"POST","path":"/ask","status_code":200,"duration_ms":9.4,"outcome":"answered"}
{"event":"http_request","request_id":"d03f7261696d44af90897f3be43838e7","method":"POST","path":"/ask","status_code":200,"duration_ms":9.48,"outcome":"answered"}
{"event":"http_request","request_id":"d9fb0172dad0404da99c02a4d1909265","method":"POST","path":"/ask","status_code":200,"duration_ms":9.2,"outcome":"answered"}
{"event":"http_request","request_id":"a2014bc327fc4297be0fdeee89d64678","method":"POST","path":"/ask","status_code":200,"duration_ms":7.89,"outcome":"answered"}
{"event":"http_request","request_id":"2e9ede132d2345b4bb11d7a305a9ccd3","method":"POST","path":"/ask","status_code":200,"duration_ms":8.32,"outcome":"answered"}
{"event":"http_request","request_id":"089c528c0a4a4f0ab5b69197c1dd8ffc","method":"POST","path":"/ask","status_code":200,"duration_ms":9.11,"outcome":"answered"}
{"event":"http_request","request_id":"59f9fdab10b54a568e7ae0f16c242ee1","method":"POST","path":"/ask","status_code":200,"duration_ms":7.68,"outcome":"answered"}
```

### Run 3 — actual output

The transcript file is named [run2-client-output.txt](./run2-client-output.txt)
because the Run 3 command reused that filename. The timestamps, response IDs,
and matching Droplet logs below are from Run 3.

#### Criterion 1 — `serve.py::health`

```text
Check 1/10 at 2026-11-15T21:27:04-05:00
Health check 1: HTTP 200, X-Request-ID=118d4b9c031f46acac9c6a3fb3683984
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 2/10 at 2026-11-15T21:28:04-05:00
Health check 2: HTTP 200, X-Request-ID=2d40e0cd627b4c459ecf2bf2b819aa4a
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 3/10 at 2026-11-15T21:29:04-05:00
Health check 3: HTTP 200, X-Request-ID=6827b7af964c49f2b86369293ed8fa06
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 4/10 at 2026-11-15T21:30:04-05:00
Health check 4: HTTP 200, X-Request-ID=d72edb79db35430fa5069cf3bfe8eddd
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 5/10 at 2026-11-15T21:31:04-05:00
Health check 5: HTTP 200, X-Request-ID=a400daf92503448c948d38623c83f02e
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 6/10 at 2026-11-15T21:32:04-05:00
Health check 6: HTTP 200, X-Request-ID=8f437b7e42a148a9b07c5578e65da732
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 7/10 at 2026-11-15T21:33:04-05:00
Health check 7: HTTP 200, X-Request-ID=eecb18e85b754a469ddec885fd58bb59
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 8/10 at 2026-11-15T21:34:04-05:00
Health check 8: HTTP 200, X-Request-ID=1459c665794446d1a6e49a41b43d187f
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 9/10 at 2026-11-15T21:35:04-05:00
Health check 9: HTTP 200, X-Request-ID=6a9964b1df55479e9f638fa1baa42ca0
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Check 10/10 at 2026-11-15T21:36:04-05:00
Health check 10: HTTP 200, X-Request-ID=d9eeb9317de34e379f1dc48bcb3b1097
{"corpus":"CVE_2026","detail":"ready","index_ready":true,"status":"ok"}
Criterion 1 total: 10/10
```

#### Criterion 2 — `serve.py::ask` → `app.py::ask_pipeline`

```text
CVE prompt: What is CVE-2026-9022?: HTTP 200, X-Request-ID=4a537aa8193b46c9b9b6aa987e7811d8
Expected CVE-2026-9022.json: PASS
CVE prompt: What is CVE-2026-21444?: HTTP 200, X-Request-ID=fd16621130ec403484c351ded3f257e7
Expected CVE-2026-21444.json: PASS
CVE prompt: What is CVE-2026-49975?: HTTP 200, X-Request-ID=8f378ad5334e45d99b958e1314a3f83e
Expected CVE-2026-49975.json: PASS
CVE prompt: What is CVE-2026-6409?: HTTP 200, X-Request-ID=b8af66a62f064b489fe16a69c810b36c
Expected CVE-2026-6409.json: PASS
CVE prompt: What is CVE-2026-23268?: HTTP 200, X-Request-ID=7142d91875324b62b53402528d23406f
Expected CVE-2026-23268.json: PASS
Criterion 2 total: 5/5 (target: at least 4/5)
```

#### Criterion 3 — Nginx Basic Auth and `serve.py::home`

```text
Unauthenticated GET /: HTTP 401, X-Request-ID=(none)
Unauthenticated POST /ask: HTTP 401, X-Request-ID=(none)
Authenticated GET /: HTTP 200, X-Request-ID=d96ca93919e34adea6309da4e0d2c541
Criterion 3: PASS (expected 401, 401, 200)
```

#### Criterion 4 — `serve.py::ask` and `serve.py::log_request`

```text
Empty-question POST /ask: HTTP 400, X-Request-ID=4dcf2de01bd8413e9521ad08daf0a888
{"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}"}

{"event":"http_request","request_id":"4dcf2de01bd8413e9521ad08daf0a888","method":"POST","path":"/ask","status_code":400,"duration_ms":0.37,"outcome":"invalid_input"}
```

#### Criterion 5 — `serve.py::log_request`, matched by response ID

```text
{"event":"http_request","request_id":"a231bc0aaf444fd38e0fa6df35919c73","method":"POST","path":"/ask","status_code":200,"duration_ms":8.91,"outcome":"answered"}
{"event":"http_request","request_id":"be2fb76c36144a6ca202eee23a02ac8c","method":"POST","path":"/ask","status_code":200,"duration_ms":8.94,"outcome":"answered"}
{"event":"http_request","request_id":"dc0b1364c3ad4532921bb0abb419f5a9","method":"POST","path":"/ask","status_code":200,"duration_ms":8.63,"outcome":"answered"}
{"event":"http_request","request_id":"5caf534dabb249558d2ac6c75e99ab05","method":"POST","path":"/ask","status_code":200,"duration_ms":9.01,"outcome":"answered"}
{"event":"http_request","request_id":"81a2278c574d49b9ac7ba6b80369f478","method":"POST","path":"/ask","status_code":200,"duration_ms":7.86,"outcome":"answered"}
{"event":"http_request","request_id":"4387773f31f44766a4ac139c14de587a","method":"POST","path":"/ask","status_code":200,"duration_ms":7.98,"outcome":"answered"}
{"event":"http_request","request_id":"00a9dd78e076411ea114f7330696f8fb","method":"POST","path":"/ask","status_code":200,"duration_ms":8.64,"outcome":"answered"}
{"event":"http_request","request_id":"89583e24b1024fd9b9143989d80449dd","method":"POST","path":"/ask","status_code":200,"duration_ms":8.61,"outcome":"answered"}
{"event":"http_request","request_id":"76f6327e420045fd9612ce983b951227","method":"POST","path":"/ask","status_code":200,"duration_ms":8.75,"outcome":"answered"}
{"event":"http_request","request_id":"1b210e47e166429c80f2ff2c01cfc7f0","method":"POST","path":"/ask","status_code":200,"duration_ms":8.06,"outcome":"answered"}
```

