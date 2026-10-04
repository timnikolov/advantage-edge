"""
Offline Benchmarking & Evaluation Suite for AdVantage-Edge.
Runs 150 synthetic test cases, measures Precision, Recall, F1, Sensitive Suppression Rate, Schema Pass Rate, and Latency percentiles.
"""

import json
import math
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import settings
from src.models import EvaluationMode, InputContext, ArbiterOutput
from src.pipeline import ContextualArbiterPipeline

def calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculates percentile value from list of floats."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    index = (percentile / 100.0) * (len(sorted_data) - 1)
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return sorted_data[int(index)]
    weight = index - lower
    return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight

def run_evaluation():
    dataset_path = settings.eval_dataset_path
    if not dataset_path.exists():
        print(f"Dataset file not found at {dataset_path}. Generating dataset...")
        from data.generate_dataset import build_eval_dataset
        build_eval_dataset()

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    pipeline = ContextualArbiterPipeline()

    tp = 0
    fp = 0
    fn = 0
    tn = 0

    sensitive_total = 0
    sensitive_suppressed = 0

    valid_schema_count = 0
    latencies: List[float] = []

    print(f"Executing AdVantage-Edge Benchmark Suite across {len(cases)} test cases...\n")

    for case in cases:
        context = InputContext(
            text=case["input_text"],
            timestamp=case.get("timestamp"),
            channel_category=case.get("channel_category"),
        )
        mode = EvaluationMode(case["mode"])

        try:
            output: ArbiterOutput = pipeline.process(context, mode)
            valid_schema_count += 1
            latencies.append(output.latency_ms)

            actual_monetize = output.decision.allow_monetization
            expected_commercial = case["expected_commercial"]
            expected_sensitive = case["expected_sensitive"]

            if expected_sensitive:
                sensitive_total += 1
                if not actual_monetize:
                    sensitive_suppressed += 1

            if expected_commercial and actual_monetize:
                tp += 1
            elif not expected_commercial and actual_monetize:
                fp += 1
            elif expected_commercial and not actual_monetize:
                fn += 1
            else:
                tn += 1

        except Exception as e:
            print(f"Error processing test case {case['id']}: {e}")

    total_cases = len(cases)
    precision = tp / float(tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / float(tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    sensitive_suppression_rate = (sensitive_suppressed / float(sensitive_total) * 100.0) if sensitive_total > 0 else 100.0
    non_commercial_total = (fp + tn)
    false_positive_rate = (fp / float(non_commercial_total) * 100.0) if non_commercial_total > 0 else 0.0
    schema_pass_rate = (valid_schema_count / float(total_cases) * 100.0) if total_cases > 0 else 0.0

    p50_lat = calculate_percentile(latencies, 50)
    p90_lat = calculate_percentile(latencies, 90)
    p95_lat = calculate_percentile(latencies, 95)
    p99_lat = calculate_percentile(latencies, 99)

    report_markdown = f"""# AdVantage-Edge Offline Benchmark & Evaluation Defense Report

## System Evaluation Summary
- **Total Benchmark Test Cases**: {total_cases}
- **Commercial Queries Evaluated**: {tp + fn}
- **Sensitive / Brand-Unsafe Queries**: {sensitive_total}
- **Informational Queries**: {non_commercial_total - sensitive_total}

---

## Google Strategic Evaluation Defense Matrix

| Performance Dimension | System Metric | Measured Value | Target SLA | Defense Rationale for Google PM Interviews |
| :--- | :--- | :--- | :--- | :--- |
| **Viewer Quality & Trust** | False-Positive Placement Rate | **{false_positive_rate:.2f}%** | `< 1.0%` | Prioritizes long-term platform engagement over short-term click exploitation. |
| **Brand Safety Compliance** | Sensitive Vertical Suppression Rate | **{sensitive_suppression_rate:.1f}%** | `100.0%` | Zero-tolerance policy enforcement for regulated or crisis content. |
| **Commercial Relevance** | Commercial Intent $F_1$ Score | **{f1_score:.4f}** (P: {precision:.4f}, R: {recall:.4f}) | `> 0.90` | Accurately detects latent purchase intent in complex exploratory journeys. |
| **API & Schema Reliability** | Pydantic Validation Pass Rate | **{schema_pass_rate:.1f}%** | `> 99.5%` | Validates production integration with Google Universal Commerce Protocol. |
| **Execution Latency** | Local Processing Time ($p95$) | **{p95_lat:.2f}ms** | `$t < 450\\text{{ms}}$` | Sub-500ms latency budget preserved for real-time video ad insertion. |

---

## Latency Percentile Distribution
- **p50 Latency**: `{p50_lat:.2f} ms`
- **p90 Latency**: `{p90_lat:.2f} ms`
- **p95 Latency**: `{p95_lat:.2f} ms`
- **p99 Latency**: `{p99_lat:.2f} ms`

---

## Confusion Matrix
- **True Positives (TP)**: {tp}
- **False Positives (FP)**: {fp}
- **False Negatives (FN)**: {fn}
- **True Negatives (TN)**: {tn}
"""

    print(report_markdown)

    # Write report to docs/BENCHMARK_REPORT.md
    report_file = settings.db_path.parent.parent / "docs" / "BENCHMARK_REPORT.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_markdown)

    print(f"Benchmark report saved to {report_file}")
    return report_markdown

if __name__ == "__main__":
    run_evaluation()
