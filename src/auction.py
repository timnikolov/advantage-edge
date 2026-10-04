"""
Auction Engine and Catalog Retrieval Ranker.
Calculates Expected Value (EV) score combining bid eCPM, relevance, and historical CTR.
"""

import sqlite3
import re
from pathlib import Path
from typing import List, Optional
from src.config import settings
from src.models import AdCandidate, InputContext, IntentAnalysis


class AuctionRanker:
    """
    Deterministic catalog retrieval and auction ranker.
    Uses Expected Value formula:
    Score = (bid * 0.4) + (relevance * 0.4) + (ctr * 0.2)
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or settings.db_path

    def _get_connection(self) -> sqlite3.Connection:
        if not self.db_path.exists():
            raise FileNotFoundError(f"Catalog database not found at {self.db_path}. Please run init_db.py first.")
        return sqlite3.connect(self.db_path)

    def calculate_relevance(self, query_text: str, product_title: str, product_category: str, product_keywords: str) -> float:
        """
        Calculates token-overlap and keyword relevance score (0.0 to 1.0).
        """
        def tokenize(s: str) -> set:
            return set(re.findall(r'\b[a-z0-9]+\b', s.lower()))

        query_tokens = tokenize(query_text)
        if not query_tokens:
            return 0.0

        # Filter out common stop words
        stop_words = {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "is", "how", "what", "where", "why", "video", "channel", "scene", "during"}
        filtered_query_tokens = {t for t in query_tokens if t not in stop_words and len(t) > 2}

        if not filtered_query_tokens:
            filtered_query_tokens = query_tokens

        doc_tokens = tokenize(f"{product_title} {product_category} {product_keywords}")

        # Exact token match overlap ratio
        matched_tokens = filtered_query_tokens.intersection(doc_tokens)
        overlap_score = len(matched_tokens) / float(len(filtered_query_tokens))

        # Title substring boost
        title_lower = product_title.lower()
        title_boost = 0.0
        for token in filtered_query_tokens:
            if token in title_lower:
                title_boost += 0.2

        raw_score = min(1.0, overlap_score * 0.7 + title_boost * 0.3)
        return round(raw_score, 4)

    def rank_candidates(self, context: InputContext, intent: IntentAnalysis, top_k: int = 3) -> List[AdCandidate]:
        """
        Retrieves products matching query, computes EV score, and returns top ranked candidates.
        Formula: EV_Score = (bid * 0.4) + (relevance * 0.4) + (ctr * 0.2)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Query all items from sponsors/inventory table
        cursor.execute("SELECT product_id, title, category, price, bid, ctr, merchant, deep_link, keywords FROM sponsors")
        rows = cursor.fetchall()
        conn.close()

        candidates: List[AdCandidate] = []
        full_query_text = f"{context.text} {intent.intent_category}"

        for row in rows:
            product_id, title, category, price, bid, ctr, merchant, deep_link, keywords = row

            relevance = self.calculate_relevance(full_query_text, title, category, keywords)

            # Calculate Expected Value score
            # Score = (bid * 0.4) + (relevance * 0.4) + (ctr * 0.2)
            ev_score = (bid * 0.4) + (relevance * 0.4) + (ctr * 0.2)

            candidate = AdCandidate(
                product_id=product_id,
                title=title,
                category=category,
                bid=bid,
                ctr=ctr,
                price=price,
                merchant=merchant,
                deep_link=deep_link,
                ranking_score=round(ev_score, 4)
            )
            candidates.append((candidate, relevance))

        # Sort candidates primarily by EV ranking score, using relevance as secondary key
        candidates.sort(key=lambda item: (item[0].ranking_score, item[1]), reverse=True)

        top_candidates = [c[0] for c in candidates[:top_k]]
        return top_candidates
