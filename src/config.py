"""
Configuration settings for the AdVantage-Edge Monetization Engine.
"""

import os
from pathlib import Path
from typing import Set
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    # Local LLM Runtime configuration (LM Studio / Ollama OpenAI-compatible endpoint)
    ollama_host: str = Field(default_factory=lambda: os.getenv("LLM_HOST", os.getenv("OLLAMA_HOST", "http://192.168.1.24:1234")))
    ollama_model: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", os.getenv("OLLAMA_MODEL", "local-model")))
    request_timeout_seconds: float = 2.0

    # Catalog DB configuration
    db_path: Path = Field(default_factory=lambda: BASE_DIR / "data" / "catalog.db")

    # Evaluation Dataset Path
    eval_dataset_path: Path = Field(default_factory=lambda: BASE_DIR / "data" / "eval_dataset.json")

    # Deterministic Guardrail Policy Thresholds
    min_commercial_intent_threshold: float = 0.70
    max_intrusiveness_threshold: float = 0.65

    # Zero-Tolerance Brand Safety & Sensitive Domain Categories
    prohibited_categories: Set[str] = Field(default_factory=lambda: {
        "medical_emergency",
        "mental_health_crisis",
        "political_debate",
        "tragedy_violence",
        "legal_distress",
        "self_harm",
        "elections",
        "acute_medical",
    })

settings = Settings()
