"""
Contextual Intent Arbiter Pipeline.
Orchestrates Context Ingestion -> Dual-Head Evaluation -> Guardrail Check -> Catalog Auction -> Rich Card Synthesis.
"""

import time
from typing import Optional
from src.auction import AuctionRanker
from src.engine import LLMIntentEngine
from src.guardrails import DeterministicGuardrail
from src.models import (
    AdCandidate,
    ArbiterOutput,
    EvaluationMode,
    InputContext,
    RichCardPayload,
)


class ContextualArbiterPipeline:
    """
    End-to-end Contextual Intent Arbiter & Quality-Gated Monetization Engine pipeline.
    """

    def __init__(self, engine: Optional[LLMIntentEngine] = None, guardrail: Optional[DeterministicGuardrail] = None, ranker: Optional[AuctionRanker] = None):
        self.engine = engine or LLMIntentEngine()
        self.guardrail = guardrail or DeterministicGuardrail()
        self.ranker = ranker or AuctionRanker()

    def process(self, context: InputContext, mode: EvaluationMode = EvaluationMode.SEARCH) -> ArbiterOutput:
        """
        Processes an input context and returns structured ArbiterOutput.
        """
        start_time = time.perf_counter()

        # Step 1: Ingestion & Dual-Head Intent & Safety Evaluation
        intent_analysis, organic_response = self.engine.evaluate(context, mode)

        # Step 2: Deterministic Safety & Policy Guardrail Check
        policy_decision = self.guardrail.evaluate(context, intent_analysis)

        sponsored_card: Optional[RichCardPayload] = None

        # Step 3: Conditional Auction Ranking & Payload Synthesis if cleared
        if policy_decision.allow_monetization:
            candidates = self.ranker.rank_candidates(context, intent_analysis, top_k=1)
            if candidates:
                top_ad: AdCandidate = candidates[0]
                sponsored_card = RichCardPayload(
                    headline=top_ad.title,
                    merchant_name=top_ad.merchant,
                    price_display=f"${top_ad.price:.2f}",
                    call_to_action_url=top_ad.deep_link,
                    attribution_label="Sponsored",
                    explanation=f"Relevance matched to '{context.text[:40]}...' with auction score {top_ad.ranking_score:.2f}."
                )

        end_time = time.perf_counter()
        latency_ms = round((end_time - start_time) * 1000.0, 2)

        return ArbiterOutput(
            mode=mode,
            organic_response=organic_response,
            decision=policy_decision,
            sponsored_card=sponsored_card,
            latency_ms=latency_ms,
        )
