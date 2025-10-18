from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_msg = df.shape[0] #Total Msg
    words = []
    for message in df['message']: #Words
        words.extend(message.split())

    num_media_msg = df[df['message'] == '<Media omitted>'].shape[0] #Media

    links = [] #Links
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_msg, len(words), num_media_msg, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'user': 'Name', 'count': 'percent'})
    return x, df

# Word-Cloud
def create_word_cloud(selected_user, df):
    f = open('stop_word.txt', 'r')
    stopwords = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words) 
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_word.txt', 'r')
    stopwords = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    words = []
    
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_counts = Counter(emojis)
    
    supported_emojis = []
    for e in emoji_counts:
        try:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, e, fontsize=12)
            fig.canvas.draw()
            plt.close(fig)
            supported_emojis.append(e)
        except Exception:
            continue

    filtered_counts = {e: emoji_counts[e] for e in supported_emojis}
    return pd.DataFrame(Counter(filtered_counts).most_common(len(filtered_counts)))    

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_time = df.groupby('only_date').count()['message'].reset_index()
    return daily_time

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
    
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='peroid', values='message', aggfunc='count').fillna(0)
    return user_heatmap
