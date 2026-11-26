from __future__ import annotations

from collections import Counter
import re
import pandas as pd
import streamlit as st

import helper


ROMAN_URDU_STOPWORDS = {
    "aap", "ab", "agar", "aur", "bhi", "bohat", "hai", "hain", "ho", "hoon",
    "hum", "is", "ka", "ke", "ki", "ko", "kya", "kyun", "main", "mein",
    "mera", "mere", "meri", "mujhe", "na", "nahi", "ne", "or", "par", "pe",
    "raha", "rahe", "rahi", "se", "tha", "the", "thi", "to", "tum", "un",
    "us", "wo", "woh", "ya", "ye", "yeh",
}


def add_calendar_day(df: pd.DataFrame) -> pd.DataFrame:
    """Add the numeric day field required by new calendar views."""
    if "day" in df.columns:
        return df
    result = df.copy()
    result["day"] = result["date"].dt.day
    return result


@st.cache_data(show_spinner=False)
def demo_dataframe() -> pd.DataFrame:
    """Create repeatable sample messages for the no-upload demo."""
    names = ["Danish", "Mehwish", "Usman", "Hira"]
    texts = [
        "That sounds great, thanks! 😊",
        "I am happy with this plan.",
        "I will share the details soon.",
        "This is worrying, can we check again?",
        "Good idea, everyone is welcome!",
        "What time should we meet?",
        "The photos look lovely ❤️",
        "I am not sure this will work.",
    ]
    hours = [8, 10, 15, 20]
    today = pd.Timestamp.now().normalize()
    first_day = today - pd.Timedelta(days=89)
    rows = []

    for day_offset in range(90):
        day = first_day + pd.Timedelta(days=day_offset)
        count = 4 if day.dayofweek >= 5 else 3
        for message_number in range(count):
            user = names[(day_offset + message_number) % len(names)]
            timestamp = day + pd.Timedelta(
                hours=hours[message_number],
                minutes=(day_offset * 7 + message_number * 11) % 60,
            )
            text = texts[(day_offset + message_number) % len(texts)]
            rows.append(
                {
                    "user": user,
                    "message": text,
                    "date": timestamp,
                    "message_date": timestamp.strftime("%d/%m/%y, %H:%M"),
                    "user_message": f"{user}: {text}",
                    "year": timestamp.year,
                    "month_num": timestamp.month,
                    "month": timestamp.month_name(),
                    "day": timestamp.day,
                    "only_date": timestamp.date(),
                    "day_name": timestamp.day_name(),
                    "hour": timestamp.hour,
                }
            )
    return pd.DataFrame(rows)


def participant_messages(df: pd.DataFrame, selected_user: str = "Overall") -> pd.DataFrame:
    messages = df.loc[df["user"] != "group_notification"].copy()
    if selected_user != "Overall":
        messages = messages.loc[messages["user"] == selected_user]
    return messages


def monthly_stat_comparison(
    df: pd.DataFrame, selected_user: str
) -> tuple[str, str, dict[str, tuple[int, str | None]]]:
    """Compare the latest calendar month with the month before it."""
    messages = participant_messages(df, selected_user)
    if messages.empty:
        empty_stats = {
            "Messages": (0, None),
            "Words": (0, None),
            "Media shared": (0, None),
            "Links shared": (0, None),
        }
        return "No messages", "No previous month", empty_stats

    latest = messages["date"].max().to_period("M")
    previous = latest - 1
    current_df = df.loc[df["date"].dt.to_period("M") == latest]
    previous_df = df.loc[df["date"].dt.to_period("M") == previous]
    current_stats = helper.fetch_stats(selected_user, current_df)
    previous_stats = helper.fetch_stats(selected_user, previous_df)
    labels = ["Messages", "Words", "Media shared", "Links shared"]
    result = {}

    for label, current, prior in zip(labels, current_stats, previous_stats):
        delta = f"{(current - prior) / prior * 100:+.0f}%" if prior else None
        result[label] = (int(current), delta)

    return (
        latest.strftime("%B %Y"),
        previous.strftime("%B %Y"),
        result,
    )


@st.cache_data(show_spinner=False, max_entries=8)
def word_frequencies(df: pd.DataFrame, selected_user: str = "Overall") -> dict[str, int]:
    messages = participant_messages(df, selected_user)
    stopwords = ROMAN_URDU_STOPWORDS
    words = []

    for message in messages["message"].fillna(""):
        if message.strip().lower() == "<media omitted>":
            continue
        tokens = re.findall(r"[\w']+", message.lower(), flags=re.UNICODE)
        words.extend(
            word for word in tokens
            if len(word) > 2 and word not in stopwords and not word.isnumeric()
        )

    return dict(Counter(words).most_common())


def activity_heatmap(df: pd.DataFrame, selected_user: str = "Overall") -> pd.DataFrame:
    messages = participant_messages(df, selected_user)
    weekdays = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]
    hours = list(range(24))
    if messages.empty:
        return pd.DataFrame(0, index=weekdays, columns=hours)
    return (
        messages.pivot_table(
            index="day_name",
            columns="hour",
            values="message",
            aggfunc="count",
            fill_value=0,
        )
        .reindex(index=weekdays, columns=hours, fill_value=0)
    )


def member_counts(df: pd.DataFrame) -> pd.Series:
    messages = participant_messages(df)
    return messages["user"].value_counts()


@st.cache_data(show_spinner=False, max_entries=8)
def reply_events(df: pd.DataFrame) -> pd.DataFrame:
    """Treat a sender change within 24 hours as a reply event."""
    messages = participant_messages(df).sort_values("date").reset_index(drop=True)
    columns = ["user", "date", "hour", "delay_minutes"]
    if messages.empty:
        return pd.DataFrame(columns=columns)

    previous_user = messages["user"].shift()
    previous_date = messages["date"].shift()
    delay = (messages["date"] - previous_date).dt.total_seconds() / 60
    replies = messages.loc[
        (messages["user"] != previous_user) & delay.between(0, 24 * 60),
        ["user", "date", "hour"],
    ].copy()
    replies["delay_minutes"] = delay.loc[replies.index]
    return replies[columns].reset_index(drop=True)


def reply_profile(df: pd.DataFrame) -> pd.DataFrame:
    replies = reply_events(df)
    columns = ["user", "replies", "median_minutes", "probability"]
    if replies.empty:
        return pd.DataFrame(columns=columns)

    profile = (
        replies.groupby("user")
        .agg(
            replies=("delay_minutes", "size"),
            median_minutes=("delay_minutes", "median"),
        )
        .reset_index()
    )
    weights = profile["replies"] / (profile["median_minutes"] + 1)
    total_weight = float(weights.sum())
    profile["probability"] = weights / total_weight if total_weight else 0
    return profile.sort_values("probability", ascending=False)[columns]


def quick_reply_hours(df: pd.DataFrame) -> pd.Series:
    replies = reply_events(df)
    if replies.empty:
        return pd.Series(index=range(24), dtype=float, name="median_minutes")
    return (
        replies.groupby("hour")["delay_minutes"]
        .median()
        .reindex(range(24))
        .rename("median_minutes")
    )


def awards(df: pd.DataFrame) -> list[dict[str, str]]:
    messages = participant_messages(df).sort_values("date").copy()
    if messages.empty:
        return [
            {"title": title, "winner": "—", "note": "No participant messages yet."}
            for title in [
                "Night Owl", "Emoji King", "Conversation Starter",
                "Fastest Replier", "Essay Writer",
            ]
        ]

    night = messages.loc[(messages["hour"] >= 22) | (messages["hour"] < 5)]
    night_counts = night["user"].value_counts()
    emoji_counts = helper.participant_emoji_counts(messages)
    if not emoji_counts.empty:
        emoji_totals = emoji_counts.groupby("user")["count"].sum().sort_values(ascending=False)
    else:
        emoji_totals = pd.Series(dtype=int)

    gaps = messages["date"].diff().dt.total_seconds().div(60 * 60)
    starters = messages.loc[gaps.isna() | (gaps >= 4), "user"].value_counts()
    replies = reply_profile(messages)
    essays = (
        messages.loc[messages["message"] != "<Media omitted>"]
        .assign(word_count=lambda frame: frame["message"].fillna("").str.split().str.len())
        .groupby("user")["word_count"]
        .mean()
        .sort_values(ascending=False)
    )

    def top_award(series: pd.Series, title: str, suffix: str) -> dict[str, str]:
        if series.empty or float(series.max()) <= 0:
            return {"title": title, "winner": "—", "note": suffix}
        winner = str(series.index[0])
        return {"title": title, "winner": winner, "note": suffix}

    if replies.empty:
        fastest = {"title": "Fastest Replier", "winner": "—", "note": "No reply pairs found."}
    else:
        fastest_row = replies.sort_values("median_minutes").iloc[0]
        fastest = {
            "title": "Fastest Replier",
            "winner": str(fastest_row["user"]),
            "note": f"Median reply time: {fastest_row['median_minutes']:.0f} minutes.",
        }

    return [
        top_award(night_counts, "Night Owl", "Most messages between 10 pm and 5 am."),
        top_award(emoji_totals, "Emoji King", "Sent the most emojis."),
        top_award(starters, "Conversation Starter", "Most messages after a 4-hour pause."),
        fastest,
        top_award(essays, "Essay Writer", "Highest average words per message."),
    ]
