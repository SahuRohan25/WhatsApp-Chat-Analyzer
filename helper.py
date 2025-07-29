from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import emoji
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]

    #fetching total no.of sentences/messages
    num_messages = df.shape[0]

    # fetching total no.of words
    words = []
    for messages in df['Message']:
        words.extend(messages.split())

    # fetching total no.of media shared
    num_media_msg = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # fetching total no.of links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)

# Monthly Timeline
def monthly_timeline(selected_user,df):
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]
    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

# Daily Timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]
    df['date'] = df['DateTime'].dt.date
    daily_timeline_df = df.groupby('date').count()['Message'].reset_index()
    return daily_timeline_df

# most_busy_day
def most_busy_day(selected_user, df):
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]
    return df['day_name'].value_counts()

# most_busy_month
def most_busy_month(selected_user, df):
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]
    return df['Month'].value_counts()



# Most Active users stats
def most_busy_users(df):
    x = df['Sender'].value_counts().head()
    df = round((x / df.shape[0]) * 100, 2).reset_index().rename(columns={'count': 'Percentage'})
    return x, df

# Creating Wordcloud of Messages
f = open('stop_hinglish.txt', 'r')
def create_wordcloud(selected_user,df):
    stop_words = f.read()
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]
    temp = df[df['Sender'] != 'System']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(height=800, width=800, background_color='white', min_font_size=10)
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep = " "))
    return df_wc

# Most_common_words
def most_common_words(selected_user,df):
    stop_words = f.read()

    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]
    temp = df[df['Sender'] != 'System']
    temp = temp[temp['Message'] != '<Media omitted>\n']
    words = []
    for messages in temp['Message']:
        for w in messages.lower().split():
            w = w.translate(str.maketrans('', '', string.punctuation))
            if w not in stop_words:
                words.append(w)

    common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return common_words_df

# Emoji Analysis
def emoji_count(selected_user,df):
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emoji', 'Count'])
    return emoji_df

# Activity Heatmap
def activity_heatmap(selected_user,df):
    if selected_user != 'Group Members':
        df = df[df['Sender'] == selected_user]
    heatmap = df.pivot_table(index='day_name', columns='Period', values='Message', aggfunc='count').fillna(0)
    return heatmap
