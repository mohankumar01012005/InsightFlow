"""
Shared theme constants and reusable UI helper functions.
Used by app.py and every module in pages_logic/.
"""
import streamlit as st

# ---------------------------------------------------------------------------
# Theme colors - dark navy sidebar, light content, blue accent (matches mock)
# ---------------------------------------------------------------------------
NAVY = "#0b1526"
NAVY_2 = "#111e35"
ACCENT = "#2f6feb"
BG = "#f5f7fa"
CARD = "#ffffff"
BORDER = "#e6e9ef"
TEXT_MUTED = "#6b7280"
GREEN = "#16a34a"
RED = "#dc2626"


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {BG}; }}
        section[data-testid="stSidebar"] {{
            background-color: {NAVY};
            min-width: 250px;
        }}
        section[data-testid="stSidebar"] * {{ color: #e5e9f0 !important; }}
        section[data-testid="stSidebar"] .stButton button {{
            width: 100%;
            text-align: left;
            background-color: transparent;
            border: none;
            padding: 0.55rem 0.9rem;
            border-radius: 8px;
            font-size: 0.95rem;
            margin-bottom: 2px;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background-color: {NAVY_2};
            color: #ffffff !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 0.25rem 0.25rem;
        }}
        .kpi-label {{ color: {TEXT_MUTED}; font-size: 0.8rem; font-weight: 600;
                      text-transform: uppercase; letter-spacing: .03em; }}
        .kpi-value {{ font-size: 1.9rem; font-weight: 700; color: #111827; margin: 2px 0; }}
        .section-title {{ font-size: 1.3rem; font-weight: 700; color: #111827; margin-bottom: 0.1rem; }}
        .section-sub {{ color: {TEXT_MUTED}; font-size: 0.9rem; margin-bottom: 1rem; }}
        .badge {{
            display: inline-block; padding: 2px 10px; border-radius: 999px;
            background-color: #e8f0fe; color: {ACCENT}; font-size: 0.75rem; font-weight: 600;
        }}
        .kpi-delta-up {{ color: {GREEN}; font-size: 0.85rem; font-weight: 600; }}
        .kpi-delta-down {{ color: {RED}; font-size: 0.85rem; font-weight: 600; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(col, label, value, delta=None, positive=True):
    with col:
        with st.container(border=True):
            st.markdown(f"<div class='kpi-label'>{label}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>{value}</div>", unsafe_allow_html=True)
            if delta:
                cls = "kpi-delta-up" if positive else "kpi-delta-down"
                arrow = "\u2197" if positive else "\u2198"
                st.markdown(f"<span class='{cls}'>{arrow} {delta}</span>", unsafe_allow_html=True)


def style_fig(fig):
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#374151"),
        legend=dict(orientation="h", y=1.1),
    )
    fig.update_xaxes(tickfont=dict(color="#374151"), gridcolor="#e6e9ef", linecolor="#d1d5db")
    fig.update_yaxes(tickfont=dict(color="#374151"), gridcolor="#e6e9ef", linecolor="#d1d5db")
    return fig