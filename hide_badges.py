import streamlit as st
import streamlit.components.v1 as components


def hide_badges():
    """Hide Streamlit Cloud badges/manage button on all screen sizes."""
    st.markdown(
        """
        <style>
        [class*="viewerBadge"],
        [class*="_profileContainer"],
        [class*="_profilePreview"],
        [data-testid="stStatusWidget"],
        [data-testid="manage-app-button"],
        [data-testid="stAppDeployButton"],
        .stDeployButton,
        button[aria-label*="Manage"],
        button[title*="Manage"],
        [class*="manageApp"],
        a[href*="share.streamlit.io"] {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(
        """
        <script>
        (function() {
            const selectors = [
                '[class*="viewerBadge"]',
                '[class*="_profileContainer"]',
                '[class*="_profilePreview"]',
                '[data-testid="stStatusWidget"]',
                '[data-testid="manage-app-button"]',
                '[data-testid="stAppDeployButton"]',
                '.stDeployButton',
                'button[aria-label*="Manage"]',
                'button[title*="Manage"]',
                '[class*="manageApp"]',
                'a[href*="share.streamlit.io"]'
            ];
            const hideIn = (root) => {
                selectors.forEach((sel) => {
                    root.querySelectorAll(sel).forEach((el) => {
                        el.style.setProperty('display', 'none', 'important');
                        el.style.setProperty('visibility', 'hidden', 'important');
                        el.style.setProperty('pointer-events', 'none', 'important');
                    });
                });
            };
            const run = () => {
                try { hideIn(document); } catch (e) {}
                try {
                    if (window.parent && window.parent !== window && window.parent.document) {
                        hideIn(window.parent.document);
                    }
                } catch (e) {}
            };
            run();
            setInterval(run, 1000);
            [document, (() => { try { return window.parent.document; } catch (e) { return null; } })()]
                .filter(Boolean)
                .forEach((root) => {
                    try {
                        new MutationObserver(run).observe(root.documentElement, {
                            childList: true, subtree: true, attributes: true
                        });
                    } catch (e) {}
                });
        })();
        </script>
        """,
        height=0,
        width=0,
    )
