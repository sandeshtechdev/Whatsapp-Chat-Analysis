from collections import Counter
import re

import pandas as pd
import regex as unicode_regex
from wordcloud import WordCloud

EMOJI_PATTERN = unicode_regex.compile(
    r"(?:\p{Extended_Pictographic}\uFE0F?(?:\p{Emoji_Modifier})?"
    r"(?:\u200D\p{Extended_Pictographic}\uFE0F?(?:\p{Emoji_Modifier})?)*)"
    r"|(?:\p{Regional_Indicator}{2})"
    r"|(?:[#*0-9]\uFE0F?\u20E3)"
)


def _participant_messages(selected_user, df):
    messages = df[df['user'] != 'group_notification']
    if selected_user != 'Overall':
        messages = messages[messages['user'] == selected_user]
    return messages


def fetch_stats(selected_user, df):
    df = _participant_messages(selected_user, df)

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media = df[df['message'] == '<Media omitted>'].shape[0]
    links = []
    for message in df['message']:
        links.extend(re.findall(r'http[s]?://\S+', message))

    return num_messages, len(words), num_media, len(links)


def most_busy_users(df):
    messages = df[df['user'] != 'group_notification']
    user_counts = messages['user'].value_counts()
    x = user_counts.head()
    percent = (user_counts / messages.shape[0] * 100).round(2)
    percent = percent.reset_index()
    percent.columns = ['user', 'percent']
    return x, percent


def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    messages = df.loc[df['user'] != 'group_notification', 'message'].dropna()
    emoji_counts = Counter(
        emoji for message in messages for emoji in EMOJI_PATTERN.findall(message)
    )
    return pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])


def chat_summary(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    messages = df[df['user'] != 'group_notification']
    if messages.empty:
        return "No participant messages were found to summarize."

    start_date = messages['date'].min().strftime('%b %d, %Y')
    end_date = messages['date'].max().strftime('%b %d, %Y')
    active_days = messages['only_date'].nunique()
    day_counts = messages['day_name'].value_counts()
    busiest_days = day_counts[day_counts == day_counts.max()].index.tolist()
    busiest_day_text = ' and '.join(busiest_days)
    busiest_day_label = 'weekday' if len(busiest_days) == 1 else 'weekdays'
    busiest_day_verb = 'was' if len(busiest_days) == 1 else 'were'
    summary = (
        f"From **{start_date}** to **{end_date}**, there were "
        f"**{len(messages):,} messages** across **{active_days:,} active days**. "
        f"The busiest {busiest_day_label} {busiest_day_verb} "
        f"**{busiest_day_text}**."
    )

    if selected_user == 'Overall':
        user_counts = messages['user'].value_counts()
        top_users = user_counts[user_counts == user_counts.max()].index.tolist()
        top_user_text = ', '.join(f"**{user}**" for user in top_users)
        top_user_count = int(user_counts.max())
        summary += (
            f" {top_user_text} sent the most messages "
            f"(**{top_user_count:,} each**)."
        )

    emojis = most_common_emojis(selected_user, df)
    if not emojis.empty:
        top_emoji_count = emojis.iloc[0]['count']
        top_emojis = emojis[emojis['count'] == top_emoji_count]['emoji'].tolist()
        emoji_text = ' '.join(top_emojis)
        emoji_label = 'emoji' if len(top_emojis) == 1 else 'emojis'
        emoji_verb = 'was' if len(top_emojis) == 1 else 'were'
        summary += f" The most-used {emoji_label} {emoji_verb} **{emoji_text}**."

    return summary


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]
    text = temp['message'].str.cat(sep=' ')
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    frequencies = wc.process_text(text)
    if not frequencies:
        return None
    return wc.generate_from_frequencies(frequencies)


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if len(word) > 2:
                words.append(word)

    return pd.DataFrame(pd.Series(words).value_counts().head(20)).reset_index().rename(
        columns={'index': 'word', 'count': 'count', 0: 'count'})


def monthly_timeline(selected_user, df):
    messages = _participant_messages(selected_user, df)
    timeline = (
        messages.groupby(['year', 'month_num', 'month'])
        .size()
        .reset_index(name='message')
    )
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline


def yearly_timeline(selected_user, df):
    messages = _participant_messages(selected_user, df)
    return messages.groupby('year').size().reset_index(name='message')


def participant_performance(df):
    columns = [
        'user',
        'messages',
        'message_share_percent',
        'words',
        'media',
        'links',
        'active_days',
        'avg_messages_per_active_day',
    ]
    messages = df[df['user'] != 'group_notification'].copy()
    if messages.empty:
        return pd.DataFrame(columns=columns)

    word_messages = messages['message'].fillna('').where(
        messages['message'] != '<Media omitted>',
        '',
    )
    messages['words'] = word_messages.str.split().str.len()
    messages['media'] = messages['message'].eq('<Media omitted>').astype(int)
    messages['links'] = messages['message'].fillna('').map(
        lambda message: len(re.findall(r'http[s]?://\S+', message))
    )

    performance = (
        messages.groupby('user')
        .agg(
            messages=('message', 'size'),
            words=('words', 'sum'),
            media=('media', 'sum'),
            links=('links', 'sum'),
            active_days=('only_date', 'nunique'),
        )
        .reset_index()
    )
    total_messages = performance['messages'].sum()
    performance['message_share_percent'] = (
        performance['messages'] / total_messages * 100
    ).round(2)
    performance['avg_messages_per_active_day'] = (
        performance['messages'] / performance['active_days']
    ).round(2)
    return performance[columns].sort_values(
        'messages', ascending=False, ignore_index=True
    )


def daily_timeline(selected_user, df):
    messages = _participant_messages(selected_user, df)
    return messages.groupby('only_date').size().reset_index(name='message')


def week_activity(selected_user, df):
    messages = _participant_messages(selected_user, df)
    return messages['day_name'].value_counts()


def month_activity(selected_user, df):
    messages = _participant_messages(selected_user, df)
    return messages['month'].value_counts()


def hour_activity(selected_user, df):
    messages = _participant_messages(selected_user, df)
    return messages['hour'].value_counts().sort_index()
