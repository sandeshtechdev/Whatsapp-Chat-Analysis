import streamlit as st

PAGE = "#0b1220"
CARD = "#111a2e"
BORDER = "#1f2b45"
GREEN = "#25d366"
VIOLET = "#8b7cff"
AMBER = "#fbbf24"
SKY = "#38bdf8"
TEXT = "#e8eefc"
MUTED = "#8b9ac0"


def apply_theme():
    """Style the additional dashboard components."""
    st.markdown(
        """
        <style>
        .chatlens-file-chip, .chatlens-card {
            background: #111a2e;
            border: 1px solid #1f2b45;
            border-radius: 16px;
            padding: 1rem;
        }
        .chatlens-file-chip {
            color: #e8eefc;
            font-size: .85rem;
            overflow-wrap: anywhere;
            margin: .8rem 0 1rem;
        }
        .chatlens-card h3, .chatlens-card strong {
            color: #e8eefc;
            font-family: "Space Grotesk", sans-serif;
        }
        .chatlens-card p, .chatlens-muted { color: #8b9ac0; }
        .member-row {
            display: grid;
            grid-template-columns: 2.5rem minmax(7rem, 1fr) 2fr 3.5rem;
            align-items: center;
            gap: .65rem;
            margin: .8rem 0;
            color: #e8eefc;
            font-size: .9rem;
        }
        .member-avatar {
            width: 2rem;
            height: 2rem;
            display: grid;
            place-items: center;
            border-radius: 50%;
            color: #0b1220;
            font-size: .7rem;
            font-weight: 700;
        }
        .member-track {
            height: .55rem;
            background: #1f2b45;
            border-radius: 999px;
            overflow: hidden;
        }
        .member-bar { height: 100%; border-radius: inherit; }
        .award-card {
            min-height: 9rem;
            background: #111a2e;
            border: 1px solid #1f2b45;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .award-title {
            color: #8b7cff;
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .award-name {
            color: #e8eefc;
            font: 700 1.25rem "Space Grotesk", sans-serif;
            margin: .7rem 0 .35rem;
        }
        .award-note { color: #8b9ac0; font-size: .85rem; }
        .hour-strip {
            display: grid;
            grid-template-columns: repeat(24, minmax(1.3rem, 1fr));
            gap: .2rem;
            min-width: 38rem;
        }
        .hour-cell {
            height: 1.65rem;
            border-radius: .3rem;
            text-align: center;
            color: #e8eefc;
            font-size: .62rem;
            line-height: 1.65rem;
        }
        .hour-strip-wrap { overflow-x: auto; }
        </style>
        """,
        unsafe_allow_html=True,
    )
