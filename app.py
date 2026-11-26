
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
sns.set_theme(style='whitegrid', palette='deep', context='notebook')
st.title("📊 WhatsApp Chat Analyzer")

sidebar_file = st.sidebar.file_uploader("📂 Upload a WhatsApp chat", type=["txt"])

if sidebar_file is None:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #25D36618, #128C7E18);
            border: 2px dashed #25D366;
            border-radius: 16px;
            padding: 28px 24px;
            margin: 12px 0 20px 0;
            text-align: center;
        ">
            <h2 style="margin: 0 0 8px 0;">📂 Upload Your WhatsApp Chat (.txt)</h2>
            <p style="margin: 0; font-size: 16px; opacity: 0.85;">
                Drag and drop your exported WhatsApp chat file below, or click <b>Browse files</b> to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    main_file = st.file_uploader(
        "Choose a WhatsApp chat .txt file",
        type=["txt"],
        label_visibility="collapsed",
        key="main_uploader",
    )
    with st.expander("ℹ️ How to export a WhatsApp chat (.txt)", expanded=False):
        st.markdown(
            """
            1. Open **WhatsApp** on your phone and go to the chat or group you want to analyze.
            2. Tap **⋮ (More)** → **Export chat** (or tap the contact/group name → **Export Chat** on iOS).
            3. Choose **Without Media** to get a `.txt` file.
            4. Upload that `.txt` file above, then click **✨ Show Analysis** in the sidebar.
            """
        )
else:
    main_file = None

uploaded_file = sidebar_file or main_file

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    try:
        df = preprocessor.preprocess(data)
    except ValueError as error:
        st.error(f"Could not analyze this WhatsApp export: {error}")
        st.stop()

    # user list for the dropdown
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("👤 Choose a user", user_list)

    if st.sidebar.button("✨ Show Analysis"):

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