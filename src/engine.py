"""
Dual-Head Intent & Safety Evaluation Engine.
Interfaces with local LLM runtime (Ollama OpenAI-compatible API) with high-fidelity deterministic fallback mock.
"""

import json
import re
from typing import Tuple, Optional
import httpx
from src.config import settings
from src.models import EvaluationMode, InputContext, IntentAnalysis


class MockLocalEngine:
    """
    High-fidelity local fallback NLP classifier engine.
    Ensures out-of-the-box offline execution without an active local LLM daemon.
    """

    COMMERCIAL_PATTERNS = [
        r"\b(buy|purchase|price|cost|deal|discount|coupon|review|unboxing|vs|best|cheap|repair|fix|replacement|part|install|upgrade|order|shop|where to get)\b",
        r"\b(headphones|laptop|phone|monitor|keyboard|mouse|smartwatch|drone|camera|earbuds|tv|speaker|drill|thermostat|shower|shelving|faucet|shoes|jacket|jeans|sunglasses|shorts|backpack|boots|dumbbells|treadmill|water bottle|yoga mat|massager|diffuser|jump starter|scanner|oil|tire|floor mats|brake pads|dash cam)\b"
    ]

    SENSITIVE_PATTERNS = {
        "medical_emergency": [r"cardiac arrest", r"heart attack", r"stroke", r"overdose", r"unconscious", r"ambulance", r"er doctor", r"chest pain", r"choking", r"symptoms of acute", r"anaphylactic", r"hypothermia", r"burn unit", r"triage"],
        "mental_health_crisis": [r"suicide", r"self-harm", r"severe depression", r"crisis hotline", r"want to die", r"ending it all", r"crisis support", r"crisis intervention"],
        "political_debate": [r"election riot", r"political scandal", r"candidate debate", r"partisan vote", r"ballot fraud", r"campaign speech", r"election tampering", r"senate hearing", r"congressional hearing"],
        "tragedy_violence": [r"tragic documentary", r"discussing death", r"fatal accident", r"mass shooting", r"homicide", r"terrorist", r"grief", r"funeral", r"plane crash", r"war zone", r"shooting", r"crime scene", r"murder trial", r"mass casualty"],
        "legal_distress": [r"arrest warrant", r"criminal trial", r"lawsuit summons", r"custody dispute", r"prison sentence", r"indictment", r"garnishment", r"summons", r"legal distress", r"felony", r"injunction", r"eviction"],
    }

    INFORMATIONAL_PATTERNS = [
        r"\b(capital of|what is|who is|history of|definition of|explain|formula for|how does gravity|distance to|population of|meaning of|symbol for|syntax of)\b"
    ]

    def evaluate(self, context: InputContext, mode: EvaluationMode) -> Tuple[IntentAnalysis, str]:
        text_lower = context.text.lower()
        channel_cat = (context.channel_category or "").lower()

        # Check Sensitive Categories first
        detected_category = "casual_entertainment"
        for category, patterns in self.SENSITIVE_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, text_lower):
                    detected_category = category
                    break
            if detected_category != "casual_entertainment":
                break

        # High Intrusiveness Risk Detection (e.g. sensitive context or high tension video scene)
        intrusiveness = 0.15
        if detected_category in settings.prohibited_categories:
            intrusiveness = 0.85
        elif "tragic" in text_lower or "death" in text_lower or "funeral" in text_lower or "crisis" in text_lower:
            intrusiveness = 0.75

        # Commercial Intent Calculation
        commercial_score = 0.10
        if detected_category not in settings.prohibited_categories:
            # Check commercial patterns
            commercial_matches = 0
            for pat in self.COMMERCIAL_PATTERNS:
                if re.search(pat, text_lower):
                    commercial_matches += 1

            if commercial_matches > 0:
                commercial_score = min(0.95, 0.70 + (commercial_matches * 0.12))
                if "repair" in text_lower or "fix" in text_lower or "replacement" in text_lower:
                    detected_category = "DIY/repair"
                elif "review" in text_lower or "unboxing" in text_lower or "vs" in text_lower:
                    detected_category = "product_review"
                else:
                    detected_category = "product_inquiry"

            # Informational query check
            for pat in self.INFORMATIONAL_PATTERNS:
                if re.search(pat, text_lower):
                    commercial_score = max(0.05, commercial_score - 0.50)
                    if detected_category not in settings.prohibited_categories:
                        detected_category = "informational"

        intent = IntentAnalysis(
            commercial_intent_score=round(commercial_score, 2),
            intent_category=detected_category,
            intrusiveness_score=round(intrusiveness, 2)
        )

        # Organic text synthesis based on mode
        if mode == EvaluationMode.SEARCH:
            organic_response = f"AI Overview: Here is direct informational guidance addressing your query regarding '{context.text[:50]}...'"
        else:
            organic_response = f"YouTube Context: Transcript snippet analyzed at timestamp {context.timestamp or 0.0}s in channel [{context.channel_category or 'General'}]."

        return intent, organic_response


class LLMIntentEngine:
    """
    Main evaluation engine with Ollama primary LLM connector and deterministic fallback mock.
    """

    def __init__(self):
        self.ollama_host = settings.ollama_host
        self.ollama_model = settings.ollama_model
        self.mock_engine = MockLocalEngine()

    def _call_ollama(self, context: InputContext, mode: EvaluationMode) -> Optional[Tuple[IntentAnalysis, str]]:
        """Attempts to invoke local LLM endpoint (LM Studio / Ollama OpenAI API)."""
        url = f"{self.ollama_host.rstrip('/')}/v1/chat/completions"
        system_prompt = (
            "You are an Edge Intent Arbiter. Analyze the input context and respond strictly with JSON matching:\n"
            "{\n"
            '  "commercial_intent_score": float (0.0 to 1.0),\n'
            '  "intent_category": string (e.g. medical_emergency, mental_health_crisis, political_debate, tragedy_violence, DIY/repair, product_review, casual_entertainment, informational),\n'
            '  "intrusiveness_score": float (0.0 to 1.0),\n'
            '  "organic_response": string\n'
            "}"
        )

        payload = {
            "model": self.ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Mode: {mode.value}\nContext: {context.text}\nCategory: {context.channel_category}"}
            ],
            "temperature": 0.1
        }

        try:
            with httpx.Client(timeout=settings.request_timeout_seconds) as client:
                response = client.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    raw_text = data["choices"][0]["message"]["content"]
                    
                    # Extract JSON payload if wrapped in markdown fenced code blocks
                    json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
                    if json_match:
                        raw_text = json_match.group(0)

                    content = json.loads(raw_text)
                    intent = IntentAnalysis(
                        commercial_intent_score=float(content["commercial_intent_score"]),
                        intent_category=str(content["intent_category"]),
                        intrusiveness_score=float(content["intrusiveness_score"])
                    )
                    organic = str(content.get("organic_response", "AI Overview response."))
                    return intent, organic
        except Exception:
            pass  # Fall through to local fallback mock engine

        return None

    def evaluate(self, context: InputContext, mode: EvaluationMode) -> Tuple[IntentAnalysis, str]:
        """
        Evaluates input context using primary Ollama LLM if available, otherwise fallback mock.
        """
        result = self._call_ollama(context, mode)
        if result is not None:
            return result
        return self.mock_engine.evaluate(context, mode)
