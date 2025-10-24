from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import emoji
import os

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_msg = df.shape[0]
    words = [word for message in df['message'] for word in message.split()]
    num_media_msg = df[df['message'].str.strip() == '<Media omitted>'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_msg, len(words), num_media_msg, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index()
    df.columns = ['Name', 'percent']
    return x, df

def create_word_cloud(selected_user, df):
    try:
        with open('stop_word.txt', 'r') as f:
            stopwords = set(f.read().split())
    except FileNotFoundError:
        stopwords = set(['is', 'and', 'the', 'a', 'to', 'in', 'of', 'for'])

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') &
              (~df['message'].str.contains('<Media omitted>', na=False))].copy()

    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stopwords])

    temp['message'] = temp['message'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(temp['message'].str.cat(sep=" "))

def most_common_words(selected_user, df):
    try:
        with open('stop_word.txt', 'r') as f:
            stopwords = set(f.read().split())
    except FileNotFoundError:
        stopwords = set(['is', 'and', 'the', 'a', 'to', 'in', 'of', 'for'])

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') &
              (~df['message'].str.contains('<Media omitted>', na=False))].copy()

    words = [word for message in temp['message'] for word in message.lower().split() if word not in stopwords]
    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = [c for message in df['message'] for c in message if c in emoji.EMOJI_DATA]
    emoji_counts = Counter(emojis)
    return pd.DataFrame(emoji_counts.most_common(len(emoji_counts)))

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline.apply(lambda x: f"{x['month']}-{x['year']}", axis=1)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.groupby('only_date').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if df.empty or not {'user', 'day_name'}.issubset(df.columns):
        return pd.DataFrame()
    if 'peroid' in df.columns:
        df.rename(columns={'peroid': 'period'}, inplace=True)
    elif 'period' not in df.columns:
        return pd.DataFrame()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    if df.empty:
        return pd.DataFrame()

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    user_heatmap = user_heatmap.reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        fill_value=0
    )
    return user_heatmap