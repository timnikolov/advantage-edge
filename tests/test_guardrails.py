"""
Unit tests for DeterministicGuardrail policy enforcement.
"""

import pytest
from src.guardrails import DeterministicGuardrail
from src.models import InputContext, IntentAnalysis, PolicyDecision

@pytest.fixture
def guardrail():
    return DeterministicGuardrail()

def test_sensitive_category_suppression(guardrail):
    context = InputContext(text="first aid for acute cardiac arrest emergency")
    intent = IntentAnalysis(
        commercial_intent_score=0.85,
        intent_category="medical_emergency",
        intrusiveness_score=0.20
    )
    decision = guardrail.evaluate(context, intent)
    assert decision.allow_monetization is False
    assert "medical_emergency" in decision.sensitive_flags or "Zero-Tolerance" in (decision.suppression_reason or "")

def test_intrusiveness_threshold_suppression(guardrail):
    context = InputContext(text="video timestamp during intense dramatic climax scene")
    intent = IntentAnalysis(
        commercial_intent_score=0.80,
        intent_category="casual_entertainment",
        intrusiveness_score=0.75  # > 0.65 threshold
    )
    decision = guardrail.evaluate(context, intent)
    assert decision.allow_monetization is False
    assert "Intrusiveness Guardrail Triggered" in decision.suppression_reason

def test_low_commercial_intent_suppression(guardrail):
    context = InputContext(text="what is the capital of Switzerland")
    intent = IntentAnalysis(
        commercial_intent_score=0.10,  # < 0.70 threshold
        intent_category="informational",
        intrusiveness_score=0.10
    )
    decision = guardrail.evaluate(context, intent)
    assert decision.allow_monetization is False
    assert "Commercial Intent Guardrail Triggered" in decision.suppression_reason

def test_valid_monetization_cleared(guardrail):
    context = InputContext(text="how to fix a noisy dishwasher pump impeller")
    intent = IntentAnalysis(
        commercial_intent_score=0.90,
        intent_category="DIY/repair",
        intrusiveness_score=0.20
    )
    decision = guardrail.evaluate(context, intent)
    assert decision.allow_monetization is True
    assert decision.suppression_reason is None
    assert decision.sensitive_flags == []
