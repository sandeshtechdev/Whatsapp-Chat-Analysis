import streamlit as st
import streamlit.components.v1


def hide_badges():
    """Hide Streamlit's viewer and profile badges without hiding app controls."""
    st.markdown(
        """
        <style>
        [class*="viewerBadge"],
        [class*="_profileContainer"],
        [class*="_profilePreview"],
        [data-testid="stStatusWidget"],
        [data-testid="manage-app-button"],
        a[href*="streamlit.io"],
        a[href*="streamlit.io"] img,
        footer,
        [class^="_"][style*="position:fixed"][style*="right:0"][style*="bottom:0"],
        [class^="_"][style*="position: fixed"][style*="right: 0"][style*="bottom: 0"] {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.components.v1.html(
        """
        <script>
        // CSS cannot match computed fixed positioning, so watch for late badges.
        try {
            const host = window.parent;
            const doc = host.document;
            const appContent = [
                '[data-testid="stMain"]',
                '[data-testid="stMainBlockContainer"]',
                '[data-testid="stAppViewBlockContainer"]',
                '[data-testid="stSidebar"]'
            ].join(",");

            const hideBottomRight = () => {
                for (const element of doc.querySelectorAll("body *")) {
                    if (element.closest(appContent)) continue;

                    const style = host.getComputedStyle(element);
                    const bounds = element.getBoundingClientRect();
                    const fixedBottomRight =
                        style.position === "fixed" &&
                        bounds.right >= host.innerWidth - 2 &&
                        bounds.bottom >= host.innerHeight - 2;

                    if (fixedBottomRight && style.display !== "none") {
                        element.style.setProperty("display", "none", "important");
                    }
                }
            };

            hideBottomRight();
            new host.MutationObserver(hideBottomRight).observe(doc.documentElement, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ["class", "style"]
            });
        } catch (error) {
            console.warn("Badge fallback cannot inspect the host page.", error);
        }
        </script>
        """,
        height=0,
    )#chnages are do i