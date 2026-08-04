# ES-1100: Evaluation Specification — Metrics, Profiles & Thresholds

**Status:** Active
**Date:** 2026-07-30
**Paired Plan:** EP-1100
**Evidence:** EV-1100
**Owner:** Product Engineering

---

## 1. Quality Profiles

| Profile | Description | Evaluators | Case Count | Gate Threshold |
|---------|-------------|-----------|------------|----------------|
| Smoke | Quick sanity check after each commit | EVA-1, EVA-5 | 1-2 | 100% |
| Regression | Pre-merge validation | All 5 EVAs | 5-10 | 90% |
| Release | Full pipeline verification | All 5 EVAs | All | 92% |
| Research | Exploration and tuning | All 5 EVAs | All | Informational only |

---

## 2. Promotion Gate Metrics (MUST pass thresholds)

### 2.1 Unsupported Assertion Rate (UAR)
```
UAR = unsupported_claims / total_claims
Threshold: UAR <= 0.15
```
Claims are unsupported when `GroundingValidator` cannot link them to cited evidence.

### 2.2 Projection Determinism (PD)
```
PD = (deterministic_projections / total_projections)
Threshold: PD == 1.0
```
A projection is deterministic if two calls to `WorkbenchProjector.project()` with identical inputs produce identical `WorkbenchViewModel` instances.

### 2.3 Workflow Success Rate (WSR)
```
WSR = successful_pipeline_runs / total_pipeline_runs
Threshold: WSR >= 0.92
```
A pipeline run is successful if all stages (Bind→Validate→Understand→Chat→Inspect) complete without error.

### 2.4 Route Correctness (nominal exec)
```
RC = correct_routes / total_routes
Threshold: RC >= 0.92
```
A route is correct if the bidirectional lookup returns the expected target within 1 hop.

---

## 3. Understanding Metrics

### 3.1 Citation Coverage (CC)
```
CC = claims_with_citations / total_claims
Threshold: CC >= 0.85
```
Measures the fraction of claims attached to verified citations over the complete pipeline.

### 3.2 Precision@K
```
P@k = |retrieved ∩ expected| / |retrieved|
```
### 3.3 Recall@K
```
R@k = |retrieved ∩ expected| / |expected|
```

### 3.4 Retrieval Depth
```
Depth = sum of evidence count per response / total responses
```
Informational only.

---

## 4. Information-al Metrics (Observed, Not Gated)

- **Latency**: Wall-clock time per evaluation case in ms.
- **Memory Usage**: Peak RSS observed per run.
- **Average Citations**: Mean citations captured in `AssistantResponse.cited_evidence`.
- **Retrieval Depth (RD)**: Granularity depth of observed matched evidence.

---

## 5. Golden Dataset Format

Each case is a JSON file containing:
```json
{
  "case_id": "case_001",
  "input_evidence": [...],
  "expected_findings": [...],
  "expected_understanding": {...},
  "expected_citations": [...],
  "expected_routes": {...}
}
```

Cases are grouped by dataset version in `evaluation/datasets/golden/<dataset_name>/`.

---

## 6. Promotion Gates vs Profiles

| Metric | Gate? | Smoke | Regression | Release |
|--------|-------|--------|-----------|------|
| Unsupported Assertion Rate | YES | <= 0.15 | <= 0.15 | <= 0.15 |
| Projection Determinism | YES | 1.0 | 1.0 | 1.0 |
| Workflow Success Rate | YES | >= 0.90 | >= 0.90 | >= 0.92 |
| Route Correctness | YES | >= 0.95 | >= 0.95 | >= 0.98 |
| ― | | | | |
| Precision@K | NO | Observed | Observed | Observed |
| Recall@K | NO | Observed | Observed | Observed |
| Coverage | NO | Observed | Observed | Observed |
| Latency | NO | Observed | Observed | Observed |
| Memory | NO | Observed | Observed | Observed |
| Avg Citations | NO | Observed | Observed | Observed |

---

## 7. Evaluation Provenance (MUST)

Every `EvaluationReport` MUST include:

```python
@dataclass(frozen=True)
class EvaluationProvenance:
    framework_version: str
    specification_version: str
    dataset_version: str
    target_platform_version: str
    execution_timestamp: str