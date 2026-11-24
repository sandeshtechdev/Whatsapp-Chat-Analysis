# import streamlit as st

# st.title("WhatsApp Chat Analyzer")

# # uploader in the sidebar, only .txt files allowed
# uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file", type=["txt"])

# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()        # read file as bytes
#     data = bytes_data.decode("utf-8")            # convert bytes to text
#     st.text(data)


import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📂 Upload a WhatsApp chat", type=["txt"])

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
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ---------- 3. Daily timeline ----------
        st.header("📈 Daily Messages")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ---------- 4. Activity map ----------
        st.header("🔥 Activity Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📆 Busiest Day")
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("🗓️ Most Active Month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.subheader("⏰ Messages by Hour")
        hours = helper.hour_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(hours.index, hours.values, color='teal')
        st.pyplot(fig)

        # ---------- 5. Busiest users (only for Overall) ----------
        if selected_user == 'Overall':
            st.header("🏆 Most Active Users")
            x, percent_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                user_counts = df.loc[
                    df['user'] != 'group_notification', 'user'
                ].value_counts()
                if user_counts.empty:
                    st.info("No participant messages are available for the pie chart.")
                else:
                    fig, ax = plt.subplots()
                    ax.pie(
                        user_counts.values,
                        labels=user_counts.index,
                        autopct='%1.1f%%',
                        startangle=90,
                    )
                    ax.axis('equal')
                    st.pyplot(fig)
            st.caption("📋 Share of messages by user")
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