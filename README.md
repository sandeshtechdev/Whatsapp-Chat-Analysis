# ChatLens

A dark-themed Streamlit app for exploring an exported WhatsApp chat. Upload a
`.txt` export, choose **Overall** or a participant, and select **Show Analysis**.
The landing page follows the ChatLens design and keeps uploaded chat data in
memory for the current session. Uploads are limited to 200 MB per file; split
larger exports before uploading.

## Features

- Message, word, media, and link counts
- Chat summary with date range, active days, busiest weekdays, top participant,
  and most-used emoji
- Monthly and yearly message timelines with the busiest and quietest active
  month summaries
- Daily, weekday, month, and hour activity charts
- Group-member performance table with message share, words, media, links,
  active days, and average messages per active day
- Participant message-share pie chart with labels on larger slices and a
  complete participant-share table
- Per-participant emoji breakdown with the emoji and number of times sent
- Emoji counts, word cloud, and common-word table
- Overview cards with month-over-month changes, VADER sentiment, member
  activity, and weekday totals
- People awards, day/hour heatmap, busiest month, top words, and top emojis
- Seven-day moving-average forecast, backtested confidence, mood outlook,
  reply likelihood, and fastest reply hours
- Sample demo mode with Danish, Mehwish, Usman, and Hira
- Original **Show Analysis** charts remain available under **Existing analysis**

## Requirements

- Python 3.9 or later
- Packages listed in [`requirements.txt`](requirements.txt)

The app uses Streamlit for the interface, pandas for parsing and analysis,
Matplotlib and Seaborn for charts and styling, `regex` for Unicode emoji
matching, WordCloud for word-clouds, and VADER for sentiment analysis.

## Install and run

From this directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the app:

```bash
python -m streamlit run app.py
```

Streamlit opens the local app in a browser. Upload a WhatsApp `.txt` export from
the landing page, choose a participant on the main page, and click
**Show Analysis**.

## Project files

- `app.py` builds the Streamlit dashboard.
- `preprocessor.py` recognizes WhatsApp message timestamps, extracts senders and
  messages, and derives date/time fields.
- `helper.py` calculates statistics and prepares summaries, charts, emoji
  counts, word clouds, and common words.
- `theme.py`, `pages.py`, `extras.py`, and `ml.py` provide the new theme,
  dashboard pages, derived chat metrics, and sentiment/forecast calculations.
- `requirements.txt` lists the app's Python dependencies.

`start.ipynb` is an earlier parsing experiment and is intentionally not part of
the app setup.

## Chat privacy

Chat exports can contain private conversations. The `Datacollect/` folder and
the notebook are excluded from Git. Do not commit chat exports or other private
data. If deploying the app to a hosted service, review that service's privacy
and data-retention policies before uploading a chat.
