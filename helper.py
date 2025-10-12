from urlextract import URLExtract
from wordcloud import WordCloud
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
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['message'] != '<Media omitted>']
    temp = temp[temp['user'] != 'Meta AI']
    text = temp['message'].str.cat(sep=" ")
    stopwords = {'media', 'omitted', 'meta', 'ai'}
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white',
        stopwords=stopwords).generate(text)
    return wc
