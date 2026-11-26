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
    """Apply the shared theme and responsive layout."""
    st.markdown(
        """
        <style>
        :root {
            --page: #0b1220;
            --sidebar: #0e1628;
            --card: #111a2e;
            --border: #1f2b45;
            --green: #25d366;
            --text: #e8eefc;
            --muted: #8b9ac0;
        }

        [data-testid="stAppViewContainer"], .stApp {
            width: 100%;
            max-width: 100%;
            overflow-x: hidden;
            background: var(--page);
        }
        [data-testid="stHeader"] {
            min-height: 48px;
            background: var(--page);
            z-index: 1100;
        }
        [data-testid="stMainBlockContainer"],
        [data-testid="stAppViewBlockContainer"] {
            width: 100%;
            max-width: 1240px;
            margin: 0 auto;
            padding: 56px 40px 48px;
            box-sizing: border-box;
        }
        h1, .hero-title {
            font-size: clamp(1.6rem, 3vw, 2.4rem) !important;
            line-height: 1.15;
        }
        h2 { font-size: clamp(1.35rem, 2.5vw, 2rem); }
        h3 { font-size: clamp(1.1rem, 2vw, 1.5rem); }

        /* Sidebar body and controls */
        [data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            color: var(--text);
            background: var(--sidebar) !important;
            border-right: 1px solid var(--border);
            overflow-x: hidden;
        }
        [data-testid="stSidebar"] > div {
            width: 100% !important;
            background: var(--sidebar) !important;
        }
        [data-testid="stSidebarContent"] {
            max-height: 100vh;
            padding-bottom: 4rem;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            scrollbar-width: thin;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: var(--text);
        }
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: var(--muted) !important;
        }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
            color: var(--text);
            background: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
            display: flex;
            align-items: center;
            min-height: 44px;
            padding: .55rem .65rem;
            border-radius: 10px;
            color: var(--text);
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
            background: var(--card);
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
            background: #16233f;
        }
        .sidebar-footer {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            z-index: 2;
            width: 280px !important;
            margin-top: 0;
            padding: .8rem 1rem !important;
            box-sizing: border-box;
            color: var(--muted) !important;
            background: var(--sidebar);
        }

        /* Restyle both native sidebar toggles without disabling their buttons. */
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ):is(button, [role="button"]),
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ) button,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"],
        [data-testid="stSidebar"] button[data-testid="baseButton-header"],
        [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"] {
            position: relative;
            display: inline-flex !important;
            align-items: center;
            justify-content: center;
            width: 40px !important;
            min-width: 40px !important;
            height: 40px !important;
            min-height: 40px !important;
            padding: 0 !important;
            color: var(--text) !important;
            background: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            box-sizing: border-box;
        }
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"]
        ):is(button, [role="button"]),
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"]
        ) button {
            position: fixed !important;
            top: 8px !important;
            left: 8px !important;
            z-index: 1201 !important;
        }
        [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"],
        [data-testid="stSidebar"] button[data-testid="baseButton-header"],
        [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"] {
            position: sticky !important;
            top: 8px !important;
            z-index: 1201 !important;
            margin-left: auto !important;
            margin-right: 12px !important;
        }
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ):is(button, [role="button"]) :is(svg, span, [data-testid="stIconMaterial"]),
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ) button :is(svg, span, [data-testid="stIconMaterial"]),
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] :is(svg, span, [data-testid="stIconMaterial"]),
        [data-testid="stSidebar"] button[data-testid="baseButton-header"] :is(svg, span, [data-testid="stIconMaterial"]),
        [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"] :is(svg, span, [data-testid="stIconMaterial"]) {
            opacity: 0 !important;
            color: transparent !important;
            fill: transparent !important;
            font-size: 0 !important;
        }
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ):is(button, [role="button"])::before,
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ) button::before,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]::before,
        [data-testid="stSidebar"] button[data-testid="baseButton-header"]::before,
        [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"]::before {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            width: 18px;
            height: 2px;
            border-radius: 2px;
            background: var(--text);
            box-shadow: 0 -6px 0 var(--text), 0 6px 0 var(--text);
            transform: translate(-50%, -50%);
        }
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ):is(button, [role="button"]):hover,
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ) button:hover,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]:hover,
        [data-testid="stSidebar"] button[data-testid="baseButton-header"]:hover,
        [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"]:hover {
            border-color: var(--green) !important;
        }
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ):is(button, [role="button"]):focus-visible,
        :where(
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            [data-testid="stExpandSidebarButton"],
            [data-testid="stSidebarCollapseButton"]
        ) button:focus-visible,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]:focus-visible,
        [data-testid="stSidebar"] button[data-testid="baseButton-header"]:focus-visible,
        [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"]:focus-visible {
            outline: 2px solid var(--green);
            outline-offset: 2px;
        }

        /* Keep charts and tables within their own content width. */
        [data-testid="stImage"],
        [data-testid="stPyplot"],
        [data-testid="stPlotlyChart"] {
            width: 100% !important;
            max-width: 100% !important;
        }
        [data-testid="stImage"] img,
        [data-testid="stPyplot"] img,
        [data-testid="stPlotlyChart"] canvas {
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
        }
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: auto !important;
        }
        [data-testid="stDataFrame"] > div {
            max-width: 100% !important;
        }
        .hour-strip-wrap { max-width: 100%; overflow-x: auto; }
        .st-key-chatlens_responsive_navigation { display: block; }

        @media (max-width: 768px) {
            [data-testid="stSidebar"][aria-expanded="false"] {
                transform: translateX(-100%) !important;
            }
            [data-testid="stSidebar"][aria-expanded="true"] {
                transform: translateX(0) !important;
            }
        }

        /* Phone: one column and compact page gutters. */
        @media (max-width: 480px) {
            [data-testid="stMainBlockContainer"],
            [data-testid="stAppViewBlockContainer"] { padding: 56px 12px 32px; }
            [data-testid="stSidebar"] {
                width: 85vw !important;
                min-width: 85vw !important;
                max-width: 85vw !important;
            }
            [data-testid="stSidebar"] .sidebar-footer { width: 85vw !important; }
            [data-testid="stHorizontalBlock"] {
                display: flex;
                flex-wrap: wrap !important;
                gap: 12px !important;
            }
            [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
                flex: 0 0 100% !important;
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
            }
            .feature-grid { grid-template-columns: 1fr; }
            .member-row {
                grid-template-columns: 2.5rem minmax(5rem, 1fr) 1.5fr 3rem;
                gap: .4rem;
            }
            [data-testid="stButton"] button,
            [data-testid="stFileUploader"] button,
            [data-testid="stSelectbox"] [role="combobox"],
            input, textarea {
                min-height: 44px;
            }
        }

        /* Large phones and small tablets: two columns. */
        @media (min-width: 481px) and (max-width: 768px) {
            [data-testid="stMainBlockContainer"],
            [data-testid="stAppViewBlockContainer"] { padding: 56px 20px 36px; }
            [data-testid="stSidebar"] {
                width: 85vw !important;
                min-width: 85vw !important;
                max-width: 85vw !important;
            }
            [data-testid="stSidebar"] .sidebar-footer { width: 85vw !important; }
            [data-testid="stHorizontalBlock"] {
                display: flex;
                flex-wrap: wrap !important;
                gap: 16px !important;
            }
            [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
                flex: 0 0 calc(50% - 8px) !important;
                width: calc(50% - 8px) !important;
                max-width: calc(50% - 8px) !important;
                min-width: 0 !important;
            }
            .feature-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            [data-testid="stButton"] button,
            [data-testid="stFileUploader"] button,
            [data-testid="stSelectbox"] [role="combobox"],
            input, textarea {
                min-height: 44px;
            }
        }

        /* Tablet and small laptop: keep two-column blocks and tablet gutters. */
        @media (min-width: 769px) and (max-width: 1024px) {
            [data-testid="stMainBlockContainer"],
            [data-testid="stAppViewBlockContainer"] { padding: 56px 20px 40px; }
            [data-testid="stHorizontalBlock"] {
                display: flex;
                flex-wrap: wrap !important;
                gap: 16px !important;
            }
            [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
                flex: 0 0 calc(50% - 8px) !important;
                width: calc(50% - 8px) !important;
                max-width: calc(50% - 8px) !important;
                min-width: 0 !important;
            }
            .feature-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }

        /* Laptop and large desktop: retain normal columns and the 280px sidebar. */
        @media (min-width: 1025px) {
            [data-testid="stMainBlockContainer"],
            [data-testid="stAppViewBlockContainer"] { padding: 56px 40px 48px; }
            .st-key-chatlens_responsive_navigation { display: none; }
        }

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
