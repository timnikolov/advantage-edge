"""
AdVantage-Edge: Streamlit UX & Admin Governance Console.
3-panel Google NotebookLM / AI Studio aesthetic interface.
"""

import sys
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

# Ensure project root is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import settings
from src.models import EvaluationMode, InputContext, ArbiterOutput, IntentAnalysis
from src.guardrails import DeterministicGuardrail
from src.auction import AuctionRanker
from src.engine import LLMIntentEngine, MockLocalEngine
from src.pipeline import ContextualArbiterPipeline

# Set Page Config to Wide Layout with Custom Title & Icon
st.set_page_config(
    page_title="AdVantage-Edge | Admin & Intent Arbiter Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Google Material Design & NotebookLM Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Header Styling */
    .app-header {
        background: linear-gradient(90deg, #1A73E8 0%, #4285F4 100%);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.15);
    }
    .app-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
    }
    .app-header p {
        margin: 0.2rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.9;
    }
    
    /* Panel Cards */
    .panel-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    
    /* Metric Tiles */
    .metric-box {
        background: #F1F3F4;
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        border: 1px solid #E8EAED;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #202124;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #5F6368;
        text-transform: uppercase;
        font-weight: 500;
    }
    
    /* Status Badges */
    .badge-monetized {
        background-color: #E6F4EA;
        color: #137333;
        border: 1px solid #CEEAD6;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        text-align: center;
        width: 100%;
    }
    .badge-suppressed {
        background-color: #FCE8E6;
        color: #C5221F;
        border: 1px solid #FAD2CF;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        text-align: center;
        width: 100%;
    }
    
    /* Shoppable Card Preview */
    .shoppable-card {
        background: #FFFFFF;
        border: 2px solid #34A853;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 16px rgba(52, 168, 83, 0.12);
        margin-top: 1rem;
    }
    .shoppable-badge {
        background: #E6F4EA;
        color: #137333;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .shoppable-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1A73E8;
        margin-bottom: 0.3rem;
    }
    .shoppable-merchant {
        font-size: 0.85rem;
        color: #5F6368;
        margin-bottom: 0.6rem;
    }
    .shoppable-price {
        font-size: 1.4rem;
        font-weight: 700;
        color: #202124;
        margin-bottom: 0.8rem;
    }
    .shoppable-btn {
        background-color: #1A73E8;
        color: white !important;
        text-decoration: none;
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.9rem;
        display: inline-block;
        text-align: center;
        width: 100%;
    }
    
    /* Organic View */
    .organic-card {
        background: #F8F9FA;
        border: 1px solid #DADCE0;
        border-radius: 12px;
        padding: 1.2rem;
        color: #3C4043;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="app-header">
    <h1>AdVantage-Edge</h1>
    <p>Edge-Native Contextual Intent Arbiter & Quality-Gated Monetization Engine | Google NotebookLM & AI Studio Console</p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State Presets
PRESETS = {
    "Select a Preset...": None,
    "Commercial Search (Best Cordless Drill)": {
        "text": "best cordless drill for concrete walls with hammer function",
        "mode": EvaluationMode.SEARCH,
        "category": None,
        "timestamp": None
    },
    "Sensitive Crisis (Emergency Stroke Symptoms)": {
        "text": "emergency signs of acute stroke and FAST protocol response",
        "mode": EvaluationMode.SEARCH,
        "category": None,
        "timestamp": None
    },
    "Low-Intent Educational (Swiss Railway History)": {
        "text": "history of the Swiss Federal Railway system in 19th century",
        "mode": EvaluationMode.SEARCH,
        "category": None,
        "timestamp": None
    },
    "YouTube Product Review (Mechanical Keyboards)": {
        "text": "hands-on testing of mechanical keyboards custom switches sound test",
        "mode": EvaluationMode.YOUTUBE_STREAM,
        "category": "Tech Reviews",
        "timestamp": 142.5
    },
    "YouTube High-Tension (Post-Disaster Grief Document)": {
        "text": "documentary segment discussing post-disaster grief and tragic loss",
        "mode": EvaluationMode.YOUTUBE_STREAM,
        "category": "Documentary",
        "timestamp": 310.0
    }
}

# ==============================================================================
# PANEL 1: LEFT SIDEBAR / SOURCES & ADMIN CONTROL PLANE
# ==============================================================================
with st.sidebar:
    st.header("🎛️ Governance & Sources")
    
    # 1. Notebook Sources & Governance
    with st.expander("📚 Notebook Sources & Governance", expanded=False):
        st.markdown("### Brand Safety Policy Guidelines")
        st.info(
            "**Zero-Tolerance Domains**: Medical Emergency, Mental Health Crisis, "
            "Political Debate, Tragedy/Violence, Legal Distress, Elections, Self-Harm."
        )
        st.markdown("### Universal Commerce Protocol Schema")
        st.code("""
RichCardPayload {
  headline: string;
  merchant_name: string;
  price_display: string;
  call_to_action_url: string;
  attribution_label: "Sponsored";
  explanation: string;
}
        """, language="typescript")

    # 2. Catalog Inspector
    with st.expander("🗄️ Catalog Inspector (Live SQLite)", expanded=False):
        try:
            conn = sqlite3.connect(settings.db_path)
            df_sponsors = pd.read_sql_query("SELECT product_id, title, category, price, bid, ctr, merchant FROM sponsors", conn)
            conn.close()
            st.metric("Total Sponsor SKUs", len(df_sponsors))
            st.dataframe(df_sponsors, height=200, use_container_width=True)
        except Exception as e:
            st.error(f"Catalog DB Error: {e}")

    st.markdown("---")
    st.subheader("⚙️ Admin Hyperparameters")
    
    # Sliders & Checkbox as requested
    intent_threshold = st.slider(
        "Commercial Intent Floor (τ)",
        min_value=0.0,
        max_value=1.0,
        value=0.70,
        step=0.05,
        help="Minimum intent score required to clear ad insertion."
    )
    
    intrusiveness_cap = st.slider(
        "Intrusiveness Cap (τ_int)",
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        step=0.05,
        help="Maximum allowable narrative disruption score."
    )
    
    zero_tolerance_mode = st.checkbox(
        "Sensitive Domain Zero-Tolerance Mode",
        value=True,
        help="Hard-suppress any query matching prohibited brand safety categories."
    )

    st.markdown("---")
    st.subheader("🤖 Engine Mode")
    engine_choice = st.radio(
        "Evaluation Runtime",
        options=["Local LLM (LM Studio / Ollama)", "Mock Engine (Deterministic Fallback)"],
        index=0
    )


# ==============================================================================
# PANEL 2: CENTER COLUMN / INTERACTIVE DEMO SIMULATOR
# ==============================================================================
col_center, col_right = st.columns([1.1, 0.9])

with col_center:
    st.subheader("💡 Interactive Context Simulator")
    
    # Preset Selector
    preset_choice = st.selectbox(
        "🎯 Quick Presets (Interview Demo Cases)",
        options=list(PRESETS.keys()),
        index=0
    )
    
    preset_data = PRESETS.get(preset_choice)
    
    # Default values based on selected preset
    default_text = preset_data["text"] if preset_data else "how to fix a noisy dishwasher pump impeller"
    default_mode_idx = 0 if (not preset_data or preset_data["mode"] == EvaluationMode.SEARCH) else 1
    default_category = preset_data["category"] if (preset_data and preset_data["category"]) else "General"
    default_timestamp = preset_data["timestamp"] if (preset_data and preset_data["timestamp"]) else 0.0

    # Ingestion Mode Tabs
    tab_search, tab_youtube = st.tabs(["🔍 Search AI Overview (Mode A)", "▶️ YouTube Video Stream (Mode B)"])
    
    selected_mode = EvaluationMode.SEARCH
    input_text = ""
    channel_category = None
    timestamp = None

    with tab_search:
        if default_mode_idx == 0:
            search_text_val = default_text
        else:
            search_text_val = "best cordless drill for concrete walls"
            
        search_input = st.text_area(
            "Multi-Turn Conversational Search Input",
            value=search_text_val,
            height=110,
            key="search_text_input"
        )
        if default_mode_idx == 0:
            input_text = search_input
            selected_mode = EvaluationMode.SEARCH

    with tab_youtube:
        if default_mode_idx == 1:
            yt_text_val = default_text
        else:
            yt_text_val = "unboxing and review of Sony WH-1000XM5 headphones"
            
        yt_input = st.text_area(
            "Video Transcript Snippet",
            value=yt_text_val,
            height=90,
            key="yt_text_input"
        )
        col_cat, col_ts = st.columns(2)
        with col_cat:
            yt_category = st.text_input("Channel Vertical", value=default_category, key="yt_cat")
        with col_ts:
            yt_timestamp = st.number_input("Timestamp (seconds)", value=float(default_timestamp), step=10.0, key="yt_ts")
            
        if default_mode_idx == 1:
            input_text = yt_input
            selected_mode = EvaluationMode.YOUTUBE_STREAM
            channel_category = yt_category
            timestamp = yt_timestamp

    run_pipeline = st.button("🚀 Run Arbiter Pipeline", type="primary", use_container_width=True)


# ==============================================================================
# PANEL 3: RIGHT COLUMN / TELEMETRY, DECISION TRACE & ARTIFACT STUDIO
# ==============================================================================
with col_right:
    st.subheader("📊 Telemetry & Artifact Studio")

    if run_pipeline or preset_choice != "Select a Preset...":
        # Instantiate Pipeline with Runtime Hyperparameter Overrides
        guardrail = DeterministicGuardrail()
        guardrail.min_commercial_intent = intent_threshold
        guardrail.max_intrusiveness = intrusiveness_cap
        if not zero_tolerance_mode:
            guardrail.prohibited_categories = set()

        ranker = AuctionRanker()
        
        # Engine setup based on toggle
        if "Mock Engine" in engine_choice:
            class CustomMockEngine:
                def evaluate(self, ctx, m):
                    return MockLocalEngine().evaluate(ctx, m)
            engine = CustomMockEngine()
        else:
            engine = LLMIntentEngine()

        pipeline = ContextualArbiterPipeline(engine=engine, guardrail=guardrail, ranker=ranker)

        # Build Context & Execute Pipeline
        context = InputContext(
            text=input_text,
            timestamp=timestamp if selected_mode == EvaluationMode.YOUTUBE_STREAM else None,
            channel_category=channel_category if selected_mode == EvaluationMode.YOUTUBE_STREAM else None
        )

        output: ArbiterOutput = pipeline.process(context, mode=selected_mode)

        # 1. Status Badge
        if output.decision.allow_monetization:
            st.markdown('<div class="badge-monetized">🟢 MONETIZED (Shoppable Ad Cleared)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge-suppressed">🔴 POLICY SUPPRESSED (Organic Response Only)</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Metric Tiles
        # Retrieve actual intent scores from engine evaluation
        intent_analysis, _ = engine.evaluate(context, selected_mode)
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{intent_analysis.commercial_intent_score:.2f}</div>
                <div class="metric-label">Commercial Intent</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{intent_analysis.intrusiveness_score:.2f}</div>
                <div class="metric-label">Intrusiveness</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{output.latency_ms:.1f} ms</div>
                <div class="metric-label">Processing Time</div>
            </div>
            """, unsafe_allow_html=True)

        # 3. Guardrail Decision Trace Card
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("#### 🛡️ Guardrail Decision Trace")
            if output.decision.allow_monetization:
                st.success("✅ **Cleared**: Commercial intent meets threshold ($\ge 0.70$), narrative intrusiveness is within acceptable bounds ($\le 0.65$), and no brand safety flags were detected.")
            else:
                st.error(f"⛔ **Suppression Justification**: {output.decision.suppression_reason}")
                if output.decision.sensitive_flags:
                    st.warning(f"**Detected Safety Flags**: {', '.join(output.decision.sensitive_flags)}")

        # 4. Rendered UI Preview (Monetized vs Organic)
        st.markdown("#### 📱 Rendered Artifact Preview")
        if output.decision.allow_monetization and output.sponsored_card:
            card = output.sponsored_card
            st.markdown(f"""
            <div class="shoppable-card">
                <span class="shoppable-badge">{card.attribution_label}</span>
                <div class="shoppable-title">{card.headline}</div>
                <div class="shoppable-merchant">Sold by <b>{card.merchant_name}</b> ✓ Verified Merchant</div>
                <div class="shoppable-price">{card.price_display}</div>
                <p style="font-size: 0.8rem; color: #5F6368; margin-bottom: 0.8rem;"><i>Rationale: {card.explanation}</i></p>
                <a href="{card.call_to_action_url}" target="_blank" class="shoppable-btn">Buy on Google / View Offer</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="organic-card">
                <div style="font-weight: 700; color: #1A73E8; margin-bottom: 0.5rem;">AI Overview (Organic Response)</div>
                <div>{output.organic_response}</div>
                <p style="font-size: 0.75rem; color: #70757A; margin-top: 0.8rem;"><i>Notice: Commercial ads are suppressed to preserve viewer quality and platform trust.</i></p>
            </div>
            """, unsafe_allow_html=True)

        # 5. Developer Drawer
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛠️ Developer Raw Pydantic Payload (JSON)", expanded=False):
            st.json(output.model_dump())
    else:
        st.info("👈 Select a Quick Preset or click **Run Arbiter Pipeline** to simulate contextual monetization arbitration.")
