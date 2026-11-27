import streamlit as st


def hide_badges():
    """Hide Streamlit's viewer and profile badges without hiding app controls."""
    # CSS injected into parent <head> via st.html (works on Streamlit Cloud)
    st.html(
        """
        <style>
        [class*="viewerBadge"],
        [class*="_profileContainer"],
        [class*="_profilePreview"],
        [data-testid="stStatusWidget"],
        [data-testid="manage-app-button"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stHeader"],
        a[href*="streamlit.io"],
        a[href*="streamlit.io"] img,
        footer,
        header,
        [class^="_"][style*="position:fixed"][style*="right:0"][style*="bottom:0"],
        [class^="_"][style*="position: fixed"][style*="right: 0"][style*="bottom: 0"],
        /* Manage button and toolbar variants */
        button[aria-label*="Manage"],
        button[title*="Manage"],
        [class*="manageApp"],
        [class*="toolbar"],
        [class*="stToolbar"] {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        </style>
        """
    )

    # JS fallback for late-injected badges (also runs in parent via st.html)
    st.html(
        """
        <script>
        // CSS cannot match computed fixed positioning, so watch for late badges.
        try {
            const doc = document;
            const appContent = [
                '[data-testid="stMain"]',
                '[data-testid="stMainBlockContainer"]',
                '[data-testid="stAppViewBlockContainer"]',
                '[data-testid="stSidebar"]'
            ].join(",");

            const hideBottomRight = () => {
                for (const element of doc.querySelectorAll("body *")) {
                    if (element.closest(appContent)) continue;

                    const style = getComputedStyle(element);
                    const bounds = element.getBoundingClientRect();
                    const fixedBottomRight =
                        style.position === "fixed" &&
                        bounds.right >= window.innerWidth - 2 &&
                        bounds.bottom >= window.innerHeight - 2;

                    if (fixedBottomRight && style.display !== "none") {
                        element.style.setProperty("display", "none", "important");
                    }
                }
                
                // Also hide manage button and toolbar by known selectors
                const manageSelectors = [
                    '[data-testid="manage-app-button"]',
                    '[data-testid="stToolbar"]',
                    '[data-testid="stDecoration"]',
                    '[data-testid="stHeader"]',
                    'button[aria-label*="Manage"]',
                    'button[title*="Manage"]',
                    '[class*="manageApp"]',
                    '[class*="toolbar"]',
                    '[class*="stToolbar"]'
                ];
                
                manageSelectors.forEach(sel => {
                    doc.querySelectorAll(sel).forEach(el => {
                        el.style.setProperty("display", "none", "important");
                        el.style.setProperty("visibility", "hidden", "important");
                        el.style.setProperty("pointer-events", "none", "important");
                    });
                });
            };

            hideBottomRight();
            new MutationObserver(hideBottomRight).observe(doc.documentElement, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ["class", "style"]
            });
        } catch (error) {
            console.warn("Badge fallback cannot inspect the host page.", error);
        }
        </script>
        """
    )