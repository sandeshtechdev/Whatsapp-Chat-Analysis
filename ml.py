from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def _participants(df: pd.DataFrame, selected_user: str) -> pd.DataFrame:
    messages = df.loc[df["user"] != "group_notification"].copy()
    if selected_user != "Overall":
        messages = messages.loc[messages["user"] == selected_user]
    return messages


@st.cache_data(show_spinner=False, max_entries=8)
def sentiment_analysis(
    df: pd.DataFrame, selected_user: str = "Overall"
) -> tuple[pd.DataFrame, dict[str, int], pd.DataFrame]:
    """Return VADER labels, totals, and average sentiment per participant."""
    messages = _participants(df, selected_user)
    if messages.empty:
        empty = pd.DataFrame(columns=["user", "date", "hour", "compound", "label"])
        return empty, {"Positive": 0, "Neutral": 0, "Negative": 0}, pd.DataFrame()

    analyzer = SentimentIntensityAnalyzer()
    rows = []
    for user, message, date, hour in messages[
        ["user", "message", "date", "hour"]
    ].itertuples(index=False, name=None):
        compound = analyzer.polarity_scores(str(message))["compound"]
        label = "Positive" if compound >= 0.05 else "Negative" if compound <= -0.05 else "Neutral"
        rows.append(
            {
                "user": user,
                "date": date,
                "hour": hour,
                "compound": compound,
                "label": label,
            }
        )

    scored = pd.DataFrame(rows)
    totals = (
        scored["label"]
        .value_counts()
        .reindex(["Positive", "Neutral", "Negative"], fill_value=0)
        .astype(int)
        .to_dict()
    )
    by_user = (
        scored.groupby("user")
        .agg(messages=("compound", "size"), compound=("compound", "mean"))
        .reset_index()
    )
    by_user["sentiment"] = by_user["compound"].map(
        lambda value: (
            "Positive" if value >= 0.05 else "Negative" if value <= -0.05 else "Neutral"
        )
    )
    return scored, totals, by_user.sort_values("compound", ascending=False)


@st.cache_data(show_spinner=False, max_entries=8)
def forecast_messages(df: pd.DataFrame, selected_user: str = "Overall") -> dict:
    """Forecast daily counts with a 7-day moving average and backtest it."""
    messages = _participants(df, selected_user)
    if messages.empty:
        return {
            "actual": pd.Series(dtype=float),
            "forecast": pd.Series(dtype=float),
            "lower": pd.Series(dtype=float),
            "upper": pd.Series(dtype=float),
            "confidence": None,
            "expected": 0,
            "last_week": 0,
            "change_percent": None,
            "peak": None,
            "mood": None,
            "mood_confidence": None,
        }

    daily = messages.assign(day=messages["date"].dt.normalize()).groupby("day").size()
    index = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    actual = daily.reindex(index, fill_value=0).astype(float)

    # A moving average is transparent and works without a long training history.
    average = float(actual.tail(7).mean())
    future_index = pd.date_range(index[-1] + pd.Timedelta(days=1), periods=7, freq="D")
    forecast = pd.Series(np.repeat(average, 7), index=future_index, dtype=float)

    errors = []
    first_test = max(1, len(actual) - 7)
    for position in range(first_test, len(actual)):
        history = actual.iloc[max(0, position - 7) : position]
        if not history.empty:
            errors.append(float(actual.iloc[position] - history.mean()))

    if errors:
        mae = float(np.mean(np.abs(errors)))
        test_mean = float(actual.iloc[first_test:].mean())
        confidence = max(0.0, min(100.0, 100 * (1 - mae / max(test_mean, 1.0))))
        interval = 1.96 * float(np.std(errors))
    else:
        confidence = None
        interval = 0.0

    lower = (forecast - interval).clip(lower=0)
    upper = forecast + interval
    expected = int(round(float(forecast.sum())))
    last_week = int(round(float(actual.tail(7).sum())))
    change_percent = (
        (expected - last_week) / last_week * 100 if last_week else None
    )

    recent = messages.loc[messages["date"] >= messages["date"].max() - pd.Timedelta(days=28)]
    if recent.empty:
        peak = None
    else:
        peak_counts = recent.groupby(["day_name", "hour"]).size()
        peak_day, peak_hour = peak_counts.idxmax()
        peak = (str(peak_day), int(peak_hour))

    scored, _, _ = sentiment_analysis(df, selected_user)
    mood_window = scored.loc[
        scored["date"] >= messages["date"].max() - pd.Timedelta(days=6)
    ]
    if mood_window.empty:
        mood, mood_confidence = None, None
    else:
        distribution = mood_window["label"].value_counts(normalize=True)
        mood = str(distribution.idxmax())
        mood_confidence = float(distribution.max() * 100)

    return {
        "actual": actual.tail(30),
        "forecast": forecast,
        "lower": lower,
        "upper": upper,
        "confidence": confidence,
        "expected": expected,
        "last_week": last_week,
        "change_percent": change_percent,
        "peak": peak,
        "mood": mood,
        "mood_confidence": mood_confidence,
    }
