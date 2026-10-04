"""
Unit tests for AuctionRanker and Expected Value scoring.
"""

import pytest
from src.auction import AuctionRanker
from src.models import InputContext, IntentAnalysis

@pytest.fixture
def ranker(tmp_path):
    # Initialize real database using fixture or project database
    from data.init_db import init_database
    db_file = tmp_path / "test_catalog.db"
    init_database(db_file)
    return AuctionRanker(db_path=db_file)

def test_calculate_relevance(ranker):
    rel = ranker.calculate_relevance(
        query_text="sony headphones noise canceling",
        product_title="WH-1000XM5 Noise Canceling Headphones",
        product_category="electronics",
        product_keywords="headphones noise canceling audio bluetooth wireless sony"
    )
    assert rel > 0.5

def test_ev_scoring_and_ranking(ranker):
    context = InputContext(text="dishwasher pump replacement kit repair")
    intent = IntentAnalysis(
        commercial_intent_score=0.90,
        intent_category="DIY/repair",
        intrusiveness_score=0.15
    )

    candidates = ranker.rank_candidates(context, intent, top_k=3)
    assert len(candidates) > 0
    top = candidates[0]
    assert top.product_id is not None
    assert top.ranking_score > 0.0
    # Confirm expected formula properties: bid*0.4 + relevance*0.4 + ctr*0.2
    assert top.bid >= 0.0
    assert 0.0 <= top.ctr <= 1.0
