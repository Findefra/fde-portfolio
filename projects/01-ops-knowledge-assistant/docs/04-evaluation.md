# 04 — Evaluation

## Purpose

This document records how we measure whether the Ops Knowledge Assistant meets the pilot success criteria. Evaluation is not optional for an FDE-style deliverable.

## Evaluation Categories

1. **Answerable operational questions**  
   Questions for which the corpus contains a clear, correct answer.  
   Metric: answer correctness + citation accuracy.

2. **Unanswerable / insufficient evidence**  
   Questions that should produce a refusal.  
   Metric: correct refusal rate (should not hallucinate).

3. **Permission boundary tests**  
   Questions that touch restricted documents, asked by a role that should not see them.  
   Metric: zero leakage of restricted content.

4. **Outdated / conflicting document traps** (stretch)  
   Cases where older versions exist or documents disagree.  
   Metric: prefers current version or surfaces conflict appropriately.

## Evaluation Set

- Target size: 30–50 questions.
- Stored under `/evals/` (questions + expected behavior).
- Each question tagged with category and expected outcome.

## Metrics to Report

| Metric | Description | Target (Pilot) |
|--------|-------------|----------------|
| Answer accuracy | Correct factual content on answerable set | ≥ 80% (to be refined) |
| Citation correctness | Sources actually support the answer | High |
| Refusal rate (unanswerable) | Correct refusals | High |
| Permission leakage | Restricted content shown to wrong role | 0 |
| Latency (p50 / p95) | End-to-end response time | Documented |
| Approx. cost per query | Token usage | Documented |

## Process

1. Build the question set before or in parallel with the system.
2. Run the full set after major changes.
3. Record results in this document or in `/evals/results/`.
4. Explicitly call out failures and known limitations — do not hide them.

## Current Results

*To be filled after the first evaluation run.*

## Known Limitations

*To be filled after evaluation.*
