"""LLM-as-a-judge scoring for the RAG evaluation questions."""

import json

from generate import generate


JUDGE_SYSTEM = """You are a strict evaluator for a retrieval-augmented generation system.
Judge only whether the answer satisfies the expected answer using the retrieved
evidence. Do not award credit for plausible outside knowledge or unsupported
inferences. A refusal is correct only when the expected answer calls for a
refusal; otherwise it is incorrect. Return exactly one JSON object with a
boolean `pass` field and a short `reason` field. Do not use markdown fences."""


def _evidence(results) -> str:
	"""Serialize retrieved chunks without depending on a specific Chunk class."""
	chunks = []
	for index, result in enumerate(results, start=1):
		metadata = getattr(result, "metadata", {}) or {}
		chunks.append(
			f"[{index}] source={getattr(result, 'source', 'unknown')} "
			f"metadata={json.dumps(metadata, sort_keys=True, default=str)}\n"
			f"{getattr(result, 'text', '')}"
		)
	return "\n\n".join(chunks) or "(no retrieved evidence)"


def _parse_verdict(raw: str) -> bool:
	"""Accept only an explicit JSON boolean; model uncertainty fails closed."""
	try:
		verdict = json.loads(raw)
	except (TypeError, json.JSONDecodeError):
		return False
	return isinstance(verdict, dict) and verdict.get("pass") is True


def judge(question, expects, answer, results) -> bool:
	"""Return whether an answer is correct and supported by retrieved chunks."""
	prompt = f"""Evaluate this RAG response.

Question:
{question}

Expected answer or requirement:
{expects}

System answer:
{answer}

Retrieved evidence:
{_evidence(results)}

The answer must address the question, satisfy the expected requirement, and
be supported by the retrieved evidence. Return only the required JSON object."""
	return _parse_verdict(generate(prompt, system=JUDGE_SYSTEM))
