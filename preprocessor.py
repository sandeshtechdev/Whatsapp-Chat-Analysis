import re

import pandas as pd


MESSAGE_PATTERN = re.compile(
    r"^\[?(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})(?:,\s*|\s+)"
    r"(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)"
    r"\]?\s*(?:-\s*)?(.*)$"
)
DATE_FORMATS = (
    "%d/%m/%Y, %I:%M:%S %p",
    "%d/%m/%y, %I:%M:%S %p",
    "%d/%m/%Y, %H:%M:%S",
    "%d/%m/%y, %H:%M:%S",
    "%d/%m/%Y, %I:%M %p",
    "%d/%m/%y, %I:%M %p",
    "%d/%m/%Y, %H:%M",
    "%d/%m/%y, %H:%M",
    "%m/%d/%Y, %I:%M:%S %p",
    "%m/%d/%y, %I:%M:%S %p",
    "%m/%d/%Y, %H:%M:%S",
    "%m/%d/%y, %H:%M:%S",
    "%m/%d/%Y, %I:%M %p",
    "%m/%d/%y, %I:%M %p",
    "%m/%d/%Y, %H:%M",
    "%m/%d/%y, %H:%M",
    "%Y-%m-%d, %I:%M:%S %p",
    "%Y-%m-%d, %I:%M %p",
    "%Y-%m-%d, %H:%M:%S",
    "%Y-%m-%d, %H:%M",
)


def preprocess(data):
    data = (
        data.replace("\ufeff", "")
        .replace("\u202f", " ")
        .replace("\u00a0", " ")
        .replace("\u200e", "")
    )
    records = []

    for line in data.splitlines():
        match = MESSAGE_PATTERN.match(line)
        if match:
            date_text, time_text, content = match.groups()
            message_date = f"{date_text}, {time_text}"
            message_date = re.sub(
                r"(\d{1,2}:\d{2}(?::\d{2})?)\s*([APap][Mm])",
                r"\1 \2",
                message_date,
            )
            user, separator, message = content.partition(": ")
            if separator:
                user = user.strip()
            else:
                user, message = "group_notification", content
            records.append(
                {
                    "user": user,
                    "message": message,
                    "message_date": message_date,
                    "user_message": content,
                }
            )
        elif records:
            records[-1]["message"] += f"\n{line}"
            records[-1]["user_message"] += f"\n{line}"

    if not records:
        raise ValueError(
            "No WhatsApp messages were recognized. The uploaded file may use an "
            "unsupported export format or contain no messages."
        )

    columns = [
        "user",
        "message",
        "date",
        "message_date",
        "user_message",
        "year",
        "month_num",
        "month",
        "only_date",
        "day_name",
        "hour",
    ]
    df = pd.DataFrame(
        records,
        columns=["user", "message", "message_date", "user_message"],
    )
    parsed = False
    for date_format in DATE_FORMATS:
        try:
            df["date"] = pd.to_datetime(df["message_date"], format=date_format)
            parsed = True
            break
        except ValueError:
            continue
    if not parsed:
        raise ValueError(
            "Date format not matched. Example dates: "
            f"{df['message_date'].head(3).tolist()}"
        )

    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["only_date"] = df["date"].dt.date
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    return df[columns]
