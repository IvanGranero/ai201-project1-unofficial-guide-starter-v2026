# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:**
**Overlap:**

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

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

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**

**Answer:**

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

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
