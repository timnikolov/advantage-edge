"""
Deterministic Policy Guardrail Engine.
Applies zero-tolerance policy checks, brand safety filters, and intrusiveness boundaries.
"""

from typing import List, Tuple
from src.config import settings
from src.models import InputContext, IntentAnalysis, PolicyDecision


class DeterministicGuardrail:
    """
    Hard-coded safety guardrail enforcing Google Ads policy compliance.
    Decouples probabilistic LLM analysis from safety gating.
    """

    # Direct keyword safety net for zero-tolerance compliance
    SENSITIVE_KEYWORDS = {
        "medical_emergency": ["cardiac arrest", "heart attack", "stroke", "overdose", "unconscious", "ambulance", "er doctor", "chest pain", "choking", "anaphylactic", "hypothermia", "burn unit", "triage"],
        "mental_health_crisis": ["suicide", "self-harm", "severe depression", "crisis hotline", "want to die", "ending it all", "crisis support", "crisis intervention"],
        "political_debate": ["election riot", "political scandal", "candidate debate", "partisan vote", "ballot fraud", "campaign speech", "election tampering", "senate hearing", "congressional hearing"],
        "tragedy_violence": ["fatal accident", "mass shooting", "homicide", "terrorist attack", "grief", "funeral", "plane crash", "war zone", "explosion", "shooting", "crime scene", "murder trial", "mass casualty"],
        "legal_distress": ["arrest warrant", "criminal trial", "lawsuit summons", "custody dispute", "prison sentence", "indictment", "garnishment", "summons", "legal distress", "felony", "injunction", "eviction"],
    }

    def __init__(self):
        self.prohibited_categories = settings.prohibited_categories
        self.min_commercial_intent = settings.min_commercial_intent_threshold
        self.max_intrusiveness = settings.max_intrusiveness_threshold

    def evaluate_text_safety_net(self, text: str) -> List[str]:
        """Scans raw input text for prohibited sensitive domain triggers."""
        text_lower = text.lower()
        detected_flags = []
        for category, keywords in self.SENSITIVE_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    detected_flags.append(category)
                    break
        return list(set(detected_flags))

    def evaluate(self, context: InputContext, intent: IntentAnalysis) -> PolicyDecision:
        """
        Evaluates monetization eligibility using deterministic policy rules.
        Returns a PolicyDecision.
        """
        sensitive_flags: List[str] = []

        # Layer 1: Check LLM classified category against prohibited set
        llm_category = intent.intent_category.lower()
        if llm_category in self.prohibited_categories:
            sensitive_flags.append(llm_category)

        # Layer 2: Deterministic keyword fallback scan for 100% zero-tolerance safety
        text_flags = self.evaluate_text_safety_net(context.text)
        for flag in text_flags:
            if flag not in sensitive_flags:
                sensitive_flags.append(flag)

        # Hard Suppression Rule 1: Sensitive Category / Prohibited Vertical
        if sensitive_flags:
            return PolicyDecision(
                allow_monetization=False,
                suppression_reason=f"Zero-Tolerance Brand Safety Suppression: Sensitive domain detected ({', '.join(sensitive_flags)})",
                sensitive_flags=sensitive_flags,
            )

        # Hard Suppression Rule 2: Narrative Disruption / Excessive Intrusiveness
        if intent.intrusiveness_score > self.max_intrusiveness:
            return PolicyDecision(
                allow_monetization=False,
                suppression_reason=f"Intrusiveness Guardrail Triggered: Score {intent.intrusiveness_score:.2f} exceeds threshold {self.max_intrusiveness:.2f}",
                sensitive_flags=[],
            )

        # Hard Suppression Rule 3: Insufficient Commercial Intent
        if intent.commercial_intent_score < self.min_commercial_intent:
            return PolicyDecision(
                allow_monetization=False,
                suppression_reason=f"Commercial Intent Guardrail Triggered: Score {intent.commercial_intent_score:.2f} below minimum threshold {self.min_commercial_intent:.2f}",
                sensitive_flags=[],
            )

        # Cleared for monetization
        return PolicyDecision(
            allow_monetization=True,
            suppression_reason=None,
            sensitive_flags=[],
        )
