import html

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

import extras
import helper
import ml
import theme


PAGE_OPTIONS = [
    "Overview",
    "People",
    "Activity",
    "Words and emoji",
    "Predictions",
    "Existing analysis",
]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ACCENTS = [theme.GREEN, theme.VIOLET, theme.AMBER, theme.SKY]


def _set_navigation_page(selected: str):
    st.session_state["chatlens_current_page"] = selected
    st.session_state["chatlens_sidebar_page"] = selected
    st.session_state["chatlens_main_page"] = selected


def _remember_page_change(selected: str):
    previous = st.session_state["chatlens_current_page"]
    if selected != previous:
        history = st.session_state.get("chatlens_page_history", [])
        history.append(previous)
        st.session_state["chatlens_page_history"] = history
    _set_navigation_page(selected)


def _sync_sidebar_page():
    _remember_page_change(st.session_state["chatlens_sidebar_page"])


def _sync_main_page():
    _remember_page_change(st.session_state["chatlens_main_page"])


def _navigate_back():
    history = st.session_state.get("chatlens_page_history", [])
    if history:
        _set_navigation_page(history.pop())
        st.session_state["chatlens_page_history"] = history


def navigation() -> str:
    current = st.session_state.get("chatlens_current_page", "Overview")
    if current not in PAGE_OPTIONS:
        current = "Overview"
    st.session_state["chatlens_current_page"] = current
    st.session_state["chatlens_sidebar_page"] = current
    st.session_state["chatlens_main_page"] = current

    st.sidebar.radio(
        "Navigation",
        PAGE_OPTIONS,
        key="chatlens_sidebar_page",
        on_change=_sync_sidebar_page,
    )
    st.sidebar.button(
        "← Back",
        key="chatlens_back_page",
        disabled=not st.session_state.get("chatlens_page_history"),
        on_click=_navigate_back,
    )
    with st.container(key="chatlens_responsive_navigation"):
        back_column, page_column = st.columns([1, 3])
        with back_column:
            st.button(
                "← Back",
                key="chatlens_responsive_back",
                disabled=not st.session_state.get("chatlens_page_history"),
                on_click=_navigate_back,
            )
        with page_column:
            st.selectbox(
                "Navigate to a section",
                PAGE_OPTIONS,
                key="chatlens_main_page",
                label_visibility="collapsed",
                on_change=_sync_main_page,
            )
    return st.session_state["chatlens_current_page"]


def _sync_sidebar_user():
    selected = st.session_state["chatlens_sidebar_user"]
    st.session_state["chatlens_main_user"] = selected
    st.session_state["chatlens_current_user"] = selected


def _sync_main_user():
    selected = st.session_state["chatlens_main_user"]
    st.session_state["chatlens_sidebar_user"] = selected
    st.session_state["chatlens_current_user"] = selected


def user_selectors(users: list[str]) -> str:
    selected = st.session_state.get("chatlens_current_user", "Overall")
    if selected not in users:
        selected = users[0]
    st.session_state["chatlens_current_user"] = selected
    st.session_state["chatlens_sidebar_user"] = selected
    st.session_state["chatlens_main_user"] = selected

    st.sidebar.selectbox(
        "Show analysis for",
        users,
        key="chatlens_sidebar_user",
        on_change=_sync_sidebar_user,
    )
    st.selectbox(
        "Show analysis for",
        users,
        key="chatlens_main_user",
        on_change=_sync_main_user,
    )
    return st.session_state["chatlens_current_user"]


def file_chip(filename: str, demo_mode: bool = False):
    if demo_mode:
        label = "Sample demo data"
    else:
        label = html.escape(filename or "Uploaded chat")
    st.sidebar.markdown(
        f'<div class="chatlens-file-chip">Chat file<br><strong>{label}</strong></div>',
        unsafe_allow_html=True,
    )


def _axis_style(ax):
    ax.set_facecolor(theme.CARD)
    ax.tick_params(colors=theme.MUTED)
    ax.xaxis.label.set_color(theme.MUTED)
    ax.yaxis.label.set_color(theme.MUTED)
    for spine in ax.spines.values():
        spine.set_color(theme.BORDER)
    ax.grid(color=theme.BORDER, alpha=0.55)


def _member_rows(df: pd.DataFrame):
    counts = extras.member_counts(df).head(7)
    if counts.empty:
        st.info("No participant messages are available.")
        return
    maximum = max(int(counts.max()), 1)
    for index, (name, count) in enumerate(counts.items()):
        color = ACCENTS[index % len(ACCENTS)]
        initials = "".join(part[0] for part in str(name).split()[:2]).upper()
        width = int(count / maximum * 100)
        safe_name = html.escape(str(name))
        st.markdown(
            f"""
            <div class="member-row">
                <span class="member-avatar" style="background:{color}">{initials}</span>
                <span>{safe_name}</span>
                <div class="member-track"><div class="member-bar"
                    style="width:{width}%;background:{color}"></div></div>
                <strong>{int(count):,}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _overview(df: pd.DataFrame, selected_user: str):
    st.title("Overview")
    current_month, previous_month, metrics = extras.monthly_stat_comparison(
        df, selected_user
    )
    st.caption(
        f"{current_month} compared with {previous_month} · "
        "Changes use the latest and previous calendar months in this export."
    )
    columns = st.columns(4)
    for column, (label, (value, delta)) in zip(columns, metrics.items()):
        column.metric(label, f"{value:,}", delta=delta)

    timeline = helper.monthly_timeline(selected_user, df)
    st.subheader("Monthly timeline")
    if timeline.empty:
        st.info("No participant messages are available for this timeline.")
    else:
        fig, ax = plt.subplots(figsize=(11, 3.5))
        fig.patch.set_facecolor(theme.CARD)
        ax.plot(timeline["time"], timeline["message"], color=theme.GREEN, marker="o")
        ax.set_ylabel("Messages")
        ax.tick_params(axis="x", rotation=35)
        _axis_style(ax)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    left, right = st.columns(2)
    with left:
        st.subheader("Sentiment")
        _, sentiment_counts, _ = ml.sentiment_analysis(df, selected_user)
        values = [sentiment_counts[label] for label in ["Positive", "Neutral", "Negative"]]
        if sum(values):
            fig, ax = plt.subplots(figsize=(4.5, 3.5))
            fig.patch.set_facecolor(theme.CARD)
            ax.pie(
                values,
                labels=["Positive", "Neutral", "Negative"],
                colors=[theme.GREEN, theme.VIOLET, theme.AMBER],
                startangle=90,
                wedgeprops={"width": 0.38, "edgecolor": theme.CARD},
                autopct=lambda pct: f"{pct:.0f}%" if pct >= 1 else "",
                textprops={"color": theme.TEXT},
            )
            ax.axis("equal")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("No participant messages are available for sentiment analysis.")
    with right:
        st.subheader("Most active members")
        _member_rows(df)

    st.subheader("Busiest days")
    messages = extras.participant_messages(df, selected_user)
    counts = messages["day_name"].value_counts().reindex(WEEKDAYS, fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 3.2))
    fig.patch.set_facecolor(theme.CARD)
    ax.bar(range(len(WEEKDAYS)), counts.values, color=theme.GREEN)
    ax.set_xticks(
        range(len(WEEKDAYS)),
        labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    )
    ax.set_ylabel("Messages")
    _axis_style(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def _people(df: pd.DataFrame):
    st.title("People and awards")
    st.caption("Awards are calculated from participant messages in this chat.")
    awards = extras.awards(df)
    columns = st.columns(3)
    for index, award in enumerate(awards):
        winner = html.escape(award["winner"])
        note = html.escape(award["note"])
        columns[index % 3].markdown(
            f"""
            <div class="award-card">
                <div class="award-title">{html.escape(award["title"])}</div>
                <div class="award-name">{winner}</div>
                <div class="award-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _activity(df: pd.DataFrame, selected_user: str):
    st.title("Activity")
    st.subheader("Day by hour")
    heatmap = extras.activity_heatmap(df, selected_user)
    fig, ax = plt.subplots(figsize=(12, 4.5))
    fig.patch.set_facecolor(theme.CARD)
    image = ax.imshow(heatmap.values, aspect="auto", cmap="Greens")
    ax.set_yticks(range(len(heatmap.index)), labels=heatmap.index)
    ax.set_xticks(range(0, 24, 2), labels=[f"{hour:02d}:00" for hour in range(0, 24, 2)])
    ax.set_xlabel("Hour")
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(theme.MUTED)
    fig.colorbar(image, ax=ax, label="Messages")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    left, right = st.columns(2)
    with left:
        st.subheader("Messages by hour")
        hours = helper.hour_activity(selected_user, df).reindex(range(24), fill_value=0)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        fig.patch.set_facecolor(theme.CARD)
        ax.bar(hours.index, hours.values, color=theme.SKY)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Messages")
        _axis_style(ax)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    with right:
        st.subheader("Busiest month")
        months = helper.month_activity(selected_user, df)
        if months.empty:
            st.info("No participant activity is available.")
        else:
            st.metric("Most active month", str(months.idxmax()), f"{int(months.max()):,} messages")
            fig, ax = plt.subplots(figsize=(6, 3.5))
            fig.patch.set_facecolor(theme.CARD)
            ax.bar(months.index, months.values, color=theme.VIOLET)
            ax.set_ylabel("Messages")
            ax.tick_params(axis="x", rotation=35)
            _axis_style(ax)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)


def _words_and_emoji(df: pd.DataFrame, selected_user: str):
    st.title("Words and emoji")
    frequencies = extras.word_frequencies(df, selected_user)
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Word cloud")
        if frequencies:
            cloud = WordCloud(
                width=900,
                height=420,
                background_color=theme.CARD,
                colormap="Greens",
                max_words=120,
                stopwords=set(),
            ).generate_from_frequencies(frequencies)
            fig, ax = plt.subplots(figsize=(9, 4.2))
            fig.patch.set_facecolor(theme.CARD)
            ax.imshow(cloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("No words remain after filtering stop words and media messages.")
    with right:
        st.subheader("Top 20 words")
        top_words = pd.DataFrame(
            list(frequencies.items())[:20], columns=["word", "count"]
        )
        st.dataframe(top_words, width="stretch", hide_index=True)

    st.subheader("Top emojis")
    emojis = helper.most_common_emojis(selected_user, df)
    st.dataframe(emojis.head(20), width="stretch", hide_index=True)


def _predictions(df: pd.DataFrame, selected_user: str):
    st.title("Predictions")
    st.caption("Seven-day moving-average forecast · calculated from this chat.")
    forecast = ml.forecast_messages(df, selected_user)

    if forecast["peak"] is None:
        st.info("Not enough participant messages to make a forecast.")
        return

    peak_day, peak_hour = forecast["peak"]
    mood = forecast["mood"] or "Not enough data"
    confidence = forecast["confidence"]
    change = forecast["change_percent"]
    metrics = st.columns(4)
    metrics[0].metric("Predicted peak time", f"{peak_day}, {peak_hour % 12 or 12} {'am' if peak_hour < 12 else 'pm'}")
    metrics[1].metric(
        "Expected messages next week",
        f"{forecast['expected']:,}",
        delta=f"{change:+.1f}%" if change is not None else None,
    )
    mood_delta = (
        f"{forecast['mood_confidence']:.0f}% of recent messages"
        if forecast["mood_confidence"] is not None else None
    )
    metrics[2].metric("Mood outlook", mood, delta=mood_delta)
    metrics[3].metric(
        "Model confidence",
        f"{confidence:.0f}%" if confidence is not None else "Not enough history",
        help="Confidence proxy from a rolling 7-day backtest of the moving-average model.",
    )

    st.subheader("Messages: actual and forecast")
    actual = forecast["actual"]
    expected = forecast["forecast"]
    fig, ax = plt.subplots(figsize=(11, 4))
    fig.patch.set_facecolor(theme.CARD)
    ax.plot(actual.index, actual.values, color=theme.GREEN, label="Actual")
    ax.plot(expected.index, expected.values, color=theme.VIOLET, linestyle="--", label="Forecast")
    ax.fill_between(
        expected.index,
        forecast["lower"].values,
        forecast["upper"].values,
        color=theme.VIOLET,
        alpha=0.18,
        label="Backtest error range",
    )
    ax.set_ylabel("Messages per day")
    ax.legend(facecolor=theme.CARD, labelcolor=theme.TEXT)
    _axis_style(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    left, right = st.columns(2)
    with left:
        st.subheader("Who will reply first")
        profile = extras.reply_profile(df)
        if profile.empty:
            st.info("Not enough reply pairs to estimate reply probabilities.")
        else:
            for _, row in profile.iterrows():
                st.write(f"{row['user']} · {row['probability']:.0%}")
                st.progress(float(row["probability"]))
    with right:
        st.subheader("Best time to get a quick reply")
        quick_hours = extras.quick_reply_hours(df)
        valid = quick_hours.dropna()
        if valid.empty:
            st.info("Not enough reply pairs to estimate response times.")
        else:
            fastest, slowest = float(valid.min()), float(valid.max())
            cells = []
            for hour, delay in quick_hours.items():
                if pd.isna(delay):
                    color = "#1f2b45"
                    tooltip = f"{hour:02d}:00 · no reply data"
                else:
                    speed = 1 if fastest == slowest else (slowest - delay) / (slowest - fastest)
                    lightness = 68 - speed * 36
                    color = f"hsl(145, 55%, {lightness:.0f}%)"
                    tooltip = f"{hour:02d}:00 · median {delay:.0f} minutes"
                cells.append(
                    f'<div class="hour-cell" title="{tooltip}" '
                    f'style="background:{color}">{hour:02d}</div>'
                )
            st.markdown(
                f'<div class="hour-strip-wrap"><div class="hour-strip">{"".join(cells)}</div></div>',
                unsafe_allow_html=True,
            )
            st.caption("Darker green indicates faster median reply times.")

    st.subheader("Sentiment per user (VADER)")
    _, _, user_sentiment = ml.sentiment_analysis(df, "Overall")
    if user_sentiment.empty:
        st.info("No participant messages are available for sentiment analysis.")
    else:
        st.dataframe(
            user_sentiment[["user", "messages", "sentiment", "compound"]].rename(
                columns={"user": "member", "messages": "messages", "compound": "average score"}
            ),
            width="stretch",
            hide_index=True,
        )


def render_page(page: str, df: pd.DataFrame, selected_user: str):
    if page == "Overview":
        _overview(df, selected_user)
    elif page == "People":
        _people(df)
    elif page == "Activity":
        _activity(df, selected_user)
    elif page == "Words and emoji":
        _words_and_emoji(df, selected_user)
    elif page == "Predictions":
        _predictions(df, selected_user)
