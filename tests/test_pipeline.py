"""
Unit tests for ContextualArbiterPipeline end-to-end flow.
"""

import pytest
from src.pipeline import ContextualArbiterPipeline
from src.models import EvaluationMode, InputContext, ArbiterOutput, PolicyDecision

@pytest.fixture
def pipeline():
    return ContextualArbiterPipeline()

def test_pipeline_search_mode_commercial(pipeline):
    context = InputContext(text="unboxing and review of Sony WH-1000XM5 headphones")
    output: ArbiterOutput = pipeline.process(context, mode=EvaluationMode.SEARCH)

    assert output.mode == EvaluationMode.SEARCH
    assert output.decision.allow_monetization is True
    assert output.sponsored_card is not None
    assert output.sponsored_card.headline != ""
    assert output.sponsored_card.attribution_label == "Sponsored"
    assert output.latency_ms > 0.0

def test_pipeline_youtube_mode_sensitive_suppressed(pipeline):
    context = InputContext(
        text="video timestamp during a tragic documentary scene discussing death",
        timestamp=145.0,
        channel_category="Documentary"
    )
    output: ArbiterOutput = pipeline.process(context, mode=EvaluationMode.YOUTUBE_STREAM)

    assert output.mode == EvaluationMode.YOUTUBE_STREAM
    assert output.decision.allow_monetization is False
    assert output.sponsored_card is None
    assert "Zero-Tolerance" in output.decision.suppression_reason or "Intrusiveness" in output.decision.suppression_reason

def test_pipeline_informational_suppressed(pipeline):
    context = InputContext(text="what is the capital of Switzerland")
    output: ArbiterOutput = pipeline.process(context, mode=EvaluationMode.SEARCH)

    assert output.decision.allow_monetization is False
    assert output.sponsored_card is None
    assert "Commercial Intent Guardrail Triggered" in output.decision.suppression_reason
