
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper
import extras
import ml
import pages
import theme

UPLOAD_LIMIT_HELP = (
    "Maximum upload: 200 MB per .txt file. Split larger exports before uploading."
)

st.set_page_config(
    page_title="ChatLens",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="auto",
)
sns.set_theme(
    style="darkgrid",
    palette=["#25d366", "#8b7cff", "#fbbf24", "#38bdf8"],
    context="notebook",
    rc={
        "figure.facecolor": "#111a2e",
        "axes.facecolor": "#111a2e",
        "axes.edgecolor": "#1f2b45",
        "axes.labelcolor": "#8b9ac0",
        "text.color": "#e8eefc",
        "xtick.color": "#8b9ac0",
        "ytick.color": "#8b9ac0",
        "grid.color": "#1f2b45",
    },
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --page: #0b1220;
        --card: #111a2e;
        --border: #1f2b45;
        --green: #25d366;
        --violet: #8b7cff;
        --amber: #fbbf24;
        --sky: #38bdf8;
        --text: #e8eefc;
        --muted: #8b9ac0;
    }
    .stApp, [data-testid="stAppViewContainer"] {
        background: var(--page);
        color: var(--text);
        font-family: Inter, sans-serif;
    }
    footer { display: none; }
    [data-testid="stMainBlockContainer"] {
        max-width: 1240px;
        padding: 1.5rem 2rem 3rem;
    }
    h1, h2, h3, [data-testid="stMetricValue"] {
        color: var(--text);
        font-family: "Space Grotesk", Inter, sans-serif;
    }
    p, label, [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }
    [data-testid="stSidebar"] {
        background: #0e1628;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--muted);
    }
    [data-testid="stFileUploader"] section {
        background: var(--card);
        border: 1px dashed #344567;
        border-radius: 14px;
    }
    [data-testid="stFileUploader"] button,
    [data-testid="stButton"] button {
        background: var(--green);
        color: #062312;
        border: 0;
        border-radius: 10px;
        font-weight: 700;
    }
    [data-testid="stButton"] button:hover {
        background: #42e47e;
        color: #062312;
        border: 0;
    }
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background: var(--card);
        border-color: var(--border);
    }
    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.1rem;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stAlert"] { border-radius: 12px; }
    .chatlens-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--border);
        padding: .2rem 0 1.4rem;
        margin-bottom: 3.2rem;
    }
    .chatlens-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--text);
        font: 700 1.2rem "Space Grotesk", sans-serif;
    }
    .chatlens-mark {
        width: 28px;
        height: 24px;
        border-radius: 8px;
        background: var(--green);
        display: inline-block;
        position: relative;
    }
    .chatlens-mark:after {
        content: "";
        position: absolute;
        left: 5px;
        bottom: -4px;
        border-width: 5px 5px 0 0;
        border-style: solid;
        border-color: var(--green) transparent transparent transparent;
    }
    .chatlens-mark:before {
        content: "";
        position: absolute;
        left: 7px;
        top: 6px;
        width: 10px;
        height: 7px;
        border: 2px solid #0b1220;
        border-radius: 4px;
    }
    .chatlens-nav {
        color: var(--muted);
        font: 500 .9rem Inter, sans-serif;
        word-spacing: 1.5rem;
    }
    .hero-kicker {
        color: var(--green);
        font: 700 .82rem Inter, sans-serif;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin: .2rem 0 1rem;
    }
    .hero-title {
        color: var(--text);
        font: 700 clamp(2.8rem, 5vw, 4rem)/1.08 "Space Grotesk", sans-serif;
        letter-spacing: -.045em;
        margin: 0 0 1.4rem;
    }
    .hero-copy {
        color: var(--muted);
        font: 500 1.12rem/1.65 Inter, sans-serif;
        max-width: 540px;
        margin-bottom: 1.4rem;
    }
    .upload-hint {
        color: var(--muted);
        font-size: .9rem;
        padding-top: .2rem;
    }
    .mood-card, .feature-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
    }
    .mood-card {
        padding: 1.25rem;
        margin-top: 4.5rem;
    }
    .mood-top, .mood-bottom, .mood-line {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .mood-label { color: var(--muted); font-size: .9rem; }
    .sample-pill {
        background: #192641;
        border-radius: 999px;
        color: var(--text);
        padding: .35rem .8rem;
        font-size: .8rem;
    }
    .mood-positive {
        color: var(--green);
        font: 700 2rem "Space Grotesk", sans-serif;
        margin: .5rem 0 1.1rem;
    }
    .mood-content { display: flex; align-items: center; gap: 1.5rem; }
    .sentiment-ring {
        width: 96px;
        height: 96px;
        border-radius: 50%;
        background: conic-gradient(var(--green) 0 60%, var(--violet) 60% 85%, var(--amber) 85% 100%);
        position: relative;
        flex: 0 0 auto;
    }
    .sentiment-ring:after {
        content: "";
        position: absolute;
        inset: 16px;
        background: var(--card);
        border-radius: 50%;
    }
    .mood-legend { color: var(--text); font-size: .9rem; line-height: 1.9; }
    .mood-legend .positive { color: var(--green); }
    .mood-legend .neutral { color: var(--violet); }
    .mood-legend .negative { color: var(--amber); }
    .mood-bottom { justify-content: flex-start; gap: .75rem; margin-top: 1.4rem; }
    .sample-avatars { display: flex; }
    .sample-avatar {
        width: 32px;
        height: 32px;
        margin-right: -6px;
        border: 2px solid var(--card);
        border-radius: 50%;
        display: grid;
        place-items: center;
        color: #092116;
        font-size: .68rem;
        font-weight: 700;
    }
    .sample-avatar:nth-child(1) { background: var(--green); }
    .sample-avatar:nth-child(2) { background: var(--violet); color: white; }
    .sample-avatar:nth-child(3) { background: var(--amber); }
    .mood-peak { color: var(--muted); font-size: .8rem; margin-left: .3rem; }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.2rem;
        margin-top: 3.2rem;
    }
    .feature-card { padding: 1.3rem; min-height: 124px; }
    .feature-card h3 {
        color: var(--text);
        font: 700 1.15rem "Space Grotesk", sans-serif;
        margin: 0 0 .55rem;
    }
    .feature-card p { margin: 0; color: var(--muted); line-height: 1.6; }
    .sidebar-footer {
        color: var(--muted);
        font-size: .8rem;
        padding-top: .8rem;
        border-top: 1px solid var(--border);
    }
    @media (max-width: 760px) {
        .chatlens-topbar { margin-bottom: 2rem; }
        .chatlens-nav { display: none; }
        .mood-card { margin-top: 1rem; }
        .feature-grid { grid-template-columns: 1fr; margin-top: 1.5rem; }
        .hero-title { font-size: 2.8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
theme.apply_theme()

st.sidebar.markdown(
    '<div class="chatlens-brand"><span class="chatlens-mark"></span>ChatLens</div>',
    unsafe_allow_html=True,
)
uploaded_file = st.sidebar.file_uploader(
    "Upload a WhatsApp chat",
    type=["txt"],
    help=UPLOAD_LIMIT_HELP,
)
st.sidebar.caption(UPLOAD_LIMIT_HELP)

if uploaded_file is not None:
    chat_bytes = uploaded_file.getvalue()
    st.session_state["chatlens_chat_bytes"] = chat_bytes
    st.session_state["chatlens_chat_filename"] = uploaded_file.name
    st.session_state["chatlens_demo_mode"] = False
else:
    chat_bytes = st.session_state.get("chatlens_chat_bytes")

demo_mode = chat_bytes is None and st.session_state.get("chatlens_demo_mode", False)
filename = st.session_state.get("chatlens_chat_filename", "")

if chat_bytes is None and not demo_mode:
    st.markdown(
        """
        <div class="chatlens-topbar">
            <div class="chatlens-brand"><span class="chatlens-mark"></span>ChatLens</div>
            <div class="chatlens-nav">Features&nbsp;&nbsp;&nbsp; Privacy</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.08, 1], gap="large")
    with left:
        st.markdown(
            """
            <div class="hero-kicker">WhatsApp chat analytics with ML</div>
            <div class="hero-title">Know your chats.<br>Predict what<br>comes next.</div>
            <div class="hero-copy">
                Upload an exported chat to see who talks most, how the mood
                changes, and when your group will be most active.
            </div>
            <div style="color:#e8eefc;font-weight:600;margin-bottom:.3rem">
                Drop your exported .txt here
            </div>
            """,
            unsafe_allow_html=True,
        )
        landing_upload = st.file_uploader(
            "Choose a WhatsApp .txt export",
            type=["txt"],
            label_visibility="collapsed",
            key="chatlens_landing_upload",
            help=UPLOAD_LIMIT_HELP,
        )
        st.markdown(
            '<div class="upload-hint">Processed in memory, never saved.<br>'
            'Maximum upload: 200 MB per file. Split larger exports before '
            'uploading.</div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="mood-card">
                <div class="mood-top">
                    <span class="mood-label">Mood this month</span>
                    <span class="sample-pill">Sample</span>
                </div>
                <div class="mood-positive">Positive</div>
                <div class="mood-content">
                    <div class="sentiment-ring"></div>
                    <div class="mood-legend">
                        <div><b class="positive">60%</b> positive</div>
                        <div><b class="neutral">25%</b> neutral</div>
                        <div><b class="negative">15%</b> negative</div>
                    </div>
                </div>
                <div class="mood-bottom">
                    <div class="sample-avatars">
                        <span class="sample-avatar">DK</span>
                        <span class="sample-avatar">MH</span>
                        <span class="sample-avatar">UM</span>
                    </div>
                    <span class="mood-peak">Predicted peak: Friday, 9 pm</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card">
                <h3>Awards and stats</h3>
                <p>Night owl, emoji king, fastest replier and more.</p>
            </div>
            <div class="feature-card">
                <h3>Sentiment analysis</h3>
                <p>A model reads the mood of every member.</p>
            </div>
            <div class="feature-card">
                <h3>Activity forecast</h3>
                <p>Find busy hours and see when the chat is most active.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Explore the demo with sample data", type="primary"):
        st.session_state["chatlens_demo_mode"] = True
        st.rerun()
    st.sidebar.markdown(
        '<div class="sidebar-footer">Built by Sandesh Kumar</div>',
        unsafe_allow_html=True,
    )
    if landing_upload is not None:
        st.session_state["chatlens_chat_bytes"] = landing_upload.getvalue()
        st.session_state["chatlens_chat_filename"] = landing_upload.name
        st.session_state["chatlens_demo_mode"] = False
        st.rerun()
    st.stop()

st.sidebar.markdown(
    '<div class="sidebar-footer">Built by Sandesh Kumar</div>',
    unsafe_allow_html=True,
)

is_demo = demo_mode
if demo_mode:
    demo_data = extras.demo_dataframe()
    chat_bytes = "\n".join(
        f"{row.message_date} - {row.user}: {row.message}"
        for row in demo_data.itertuples(index=False)
    ).encode("utf-8")
    filename = "Sample demo data"
    demo_mode = False

if not demo_mode:
    try:
        with st.spinner("Preparing your chat..."):
            data = chat_bytes.decode("utf-8")
            df = extras.add_calendar_day(preprocessor.preprocess(data))
    except UnicodeDecodeError:
        st.error("Could not read this export as UTF-8. Please upload a WhatsApp .txt export.")
        st.stop()
    except ValueError as error:
        st.error(f"Could not analyze this WhatsApp export: {error}")
        st.stop()

    # user list for the dropdown
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    pages.file_chip(filename, is_demo)
    st.title("Your chat is ready")
    st.caption(
        f"{len(df):,} messages loaded. Choose a participant, then start the analysis."
    )
    selected_user = pages.user_selectors(user_list)
    selected_page = pages.navigation()

    if selected_page != "Existing analysis":
        pages.render_page(selected_page, df, selected_user)
        st.stop()

    if st.button("Show Analysis"):

        st.header("🧾 Chat Summary")
        st.info(helper.chat_summary(selected_user, df))

        # ---------- 1. Top statistics ----------
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
        st.header("📌 Quick Stats")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💬 Messages", num_messages)
        c2.metric("✍️ Words", words)
        c3.metric("📷 Media Shared", num_media)
        c4.metric("🔗 Links Shared", num_links)

        # ---------- 2. Monthly timeline ----------
        st.header("📅 Monthly Messages")
        timeline = helper.monthly_timeline(selected_user, df)
        if timeline.empty:
            st.info("No participant messages are available for this timeline.")
        else:
            fig, ax = plt.subplots(figsize=(11, 4))
            sns.lineplot(
                data=timeline,
                x='time',
                y='message',
                marker='o',
                linewidth=2.5,
                color=sns.color_palette('deep')[2],
                ax=ax,
            )
            ax.set_xlabel("Month")
            ax.set_ylabel("Messages")
            ax.tick_params(axis='x', labelrotation=45)
            fig.tight_layout()
            st.pyplot(fig)
            busiest_month = timeline.loc[timeline['message'].idxmax()]
            quietest_month = timeline.loc[timeline['message'].idxmin()]
            col1, col2 = st.columns(2)
            col1.metric(
                "Most active month",
                busiest_month['time'],
                f"{int(busiest_month['message']):,} messages",
            )
            col2.metric(
                "Least active month",
                quietest_month['time'],
                f"{int(quietest_month['message']):,} messages",
            )
            st.caption("Monthly message counts (months with participant messages)")
            st.dataframe(
                timeline[['time', 'message']].rename(
                    columns={'time': 'month', 'message': 'messages'}
                ),
                use_container_width=True,
                hide_index=True,
            )

        st.subheader("📆 Messages by Year")
        yearly = helper.yearly_timeline(selected_user, df)
        if yearly.empty:
            st.info("No participant messages are available for this timeline.")
        else:
            yearly_chart = yearly.assign(year=yearly['year'].astype(str))
            fig, ax = plt.subplots(figsize=(9, 4))
            sns.barplot(
                data=yearly_chart,
                x='year',
                y='message',
                color=sns.color_palette('deep')[0],
                ax=ax,
            )
            ax.set_xlabel("Year")
            ax.set_ylabel("Messages")
            ax.bar_label(ax.containers[0], fmt='%.0f', padding=3)
            fig.tight_layout()
            st.pyplot(fig)
            st.dataframe(
                yearly.rename(columns={'message': 'messages'}),
                use_container_width=True,
                hide_index=True,
            )

        # ---------- 3. Daily timeline ----------
        st.header("📈 Daily Messages")
        daily = helper.daily_timeline(selected_user, df)
        if daily.empty:
            st.info("No participant messages are available for this timeline.")
        else:
            fig, ax = plt.subplots(figsize=(11, 4))
            sns.lineplot(
                data=daily,
                x='only_date',
                y='message',
                linewidth=1.8,
                color=sns.color_palette('deep')[1],
                ax=ax,
            )
            ax.set_xlabel("Date")
            ax.set_ylabel("Messages")
            ax.tick_params(axis='x', labelrotation=45)
            fig.tight_layout()
            st.pyplot(fig)

        # ---------- 4. Activity map ----------
        st.header("🔥 Activity Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📆 Busiest Day")
            busy_day = helper.week_activity(selected_user, df)
            if busy_day.empty:
                st.info("No participant activity is available for this chart.")
            else:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(
                    x=busy_day.index,
                    y=busy_day.values,
                    color=sns.color_palette('deep')[4],
                    ax=ax,
                )
                ax.set_xlabel("Weekday")
                ax.set_ylabel("Messages")
                ax.tick_params(axis='x', labelrotation=30)
                fig.tight_layout()
                st.pyplot(fig)
        with col2:
            st.subheader("🗓️ Most Active Month")
            busy_month = helper.month_activity(selected_user, df)
            if busy_month.empty:
                st.info("No participant activity is available for this chart.")
            else:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(
                    x=busy_month.index,
                    y=busy_month.values,
                    color=sns.color_palette('deep')[1],
                    ax=ax,
                )
                ax.set_xlabel("Month")
                ax.set_ylabel("Messages")
                ax.tick_params(axis='x', labelrotation=30)
                fig.tight_layout()
                st.pyplot(fig)

        st.subheader("⏰ Messages by Hour")
        hours = helper.hour_activity(selected_user, df)
        if hours.empty:
            st.info("No participant activity is available for this chart.")
        else:
            fig, ax = plt.subplots(figsize=(11, 4))
            sns.barplot(
                x=hours.index.astype(str),
                y=hours.values,
                color=sns.color_palette('deep')[2],
                ax=ax,
            )
            ax.set_xlabel("Hour of day")
            ax.set_ylabel("Messages")
            ax.bar_label(ax.containers[0], fmt='%.0f', padding=2)
            fig.tight_layout()
            st.pyplot(fig)

        # ---------- 5. Busiest users (only for Overall) ----------
        if selected_user == 'Overall':
            st.header("🏆 Most Active Users")
            performance = helper.participant_performance(df)
            if performance.empty:
                st.info("No participant messages are available for group performance.")
            else:
                st.subheader("👥 Group Member Performance")
                st.caption(
                    "Compare message and word counts, shared media and links, "
                    "active days, and each member's share of participant messages."
                )
                st.dataframe(
                    performance.rename(
                        columns={
                            'user': 'participant',
                            'messages': 'messages',
                            'message_share_percent': 'message share (%)',
                            'words': 'words',
                            'media': 'media shared',
                            'links': 'links shared',
                            'active_days': 'active days',
                            'avg_messages_per_active_day': 'messages per active day',
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

            x, percent_df = helper.most_busy_users(df)
            if x.empty:
                st.info("No participant messages are available for the charts.")
            else:
                top_users = x.sort_values().rename_axis('user').reset_index(
                    name='messages'
                )
                fig, ax = plt.subplots(
                    figsize=(10, max(4, 0.42 * len(top_users) + 1))
                )
                sns.barplot(
                    data=top_users,
                    x='messages',
                    y='user',
                    color=sns.color_palette('deep')[3],
                    ax=ax,
                )
                ax.set_title("Top participants by message count")
                ax.set_xlabel("Messages")
                ax.set_ylabel("")
                ax.bar_label(ax.containers[0], fmt='%.0f', padding=4)
                fig.tight_layout()
                st.pyplot(fig)

            user_counts = df.loc[
                df['user'] != 'group_notification', 'user'
            ].value_counts()
            if user_counts.empty:
                st.info("No participant message shares are available to chart.")
            else:
                shares = user_counts / user_counts.sum() * 100
                visible_labels = [
                    user if percent >= 3 else ''
                    for user, percent in shares.items()
                ]
                fig, ax = plt.subplots(figsize=(10, 7))
                ax.pie(
                    user_counts.values,
                    labels=visible_labels,
                    startangle=90,
                    autopct=lambda percent: (
                        f'{percent:.1f}%' if percent >= 3 else ''
                    ),
                    labeldistance=1.08,
                    pctdistance=0.68,
                    colors=sns.color_palette('pastel', n_colors=len(user_counts)),
                    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
                )
                ax.set_title("Message share by participant")
                ax.axis('equal')
                fig.tight_layout()
                st.pyplot(fig)

            st.caption(
                "To prevent overlap, names and percentages are shown only for "
                "slices of 3% or more; the table includes every participant."
            )
            st.caption("📋 Message share for all participants")
            st.dataframe(percent_df)

        # ---------- 6. Emoji insights ----------
        st.header("😀 Emoji Insights")
        emoji_df = helper.most_common_emojis(selected_user, df)
        if emoji_df.empty:
            st.info("No emojis found in messages for this selection.")
        else:
            top_emojis = emoji_df.head(5)
            emoji_columns = st.columns(len(top_emojis))
            for column, (_, row) in zip(emoji_columns, top_emojis.iterrows()):
                column.metric(str(row['emoji']), f"{int(row['count']):,}")
            st.caption("📊 Complete emoji count for this selection")
            st.dataframe(emoji_df, use_container_width=True, hide_index=True)

        if selected_user == 'Overall':
            st.subheader("😀 Emoji counts by participant")
            participant_emojis = helper.participant_emoji_counts(df)
            if participant_emojis.empty:
                st.info("No emojis found in participant messages.")
            else:
                st.dataframe(
                    participant_emojis.rename(
                        columns={
                            'user': 'participant',
                            'emoji': 'emoji',
                            'count': 'times sent',
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

        # ---------- 7. Word cloud ----------
        st.header("☁️ Word Cloud")
        wc = helper.create_wordcloud(selected_user, df)
        if wc is None:
            st.info(
                "No plottable words for this selection. The messages may contain "
                "only media, emojis, or words the word cloud filters out."
            )
        else:
            fig, ax = plt.subplots()
            ax.imshow(wc)
            ax.axis('off')
            st.pyplot(fig)

        # ---------- 8. Most common words ----------
        st.header("🔤 Most Common Words")
        common_df = helper.most_common_words(selected_user, df)
        st.dataframe(common_df)