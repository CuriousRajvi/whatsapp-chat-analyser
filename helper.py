from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(choice, df):
    if choice != 'Overall':
        df = df[df['user'] == choice]
    num_message = df.shape[0]
    words = []
    links = []
    extract = URLExtract()
    for message in df['messages']:
        words.extend(message.split())
        links.extend(extract.find_urls(message))
    # fetch number of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]
    return num_message, len(words), num_media_messages, len(links)

def busy_users(df):
    x= df['user'].value_counts().head()
    y= round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,y

def display_wordcloud(choice, df):
    if choice !='Overall':
        df=df[df['user'] == choice]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    wc= WordCloud(width = 500, height= 500, min_font_size=18, background_color='white')
    df_wc=wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(choice, df):
    if choice!='Overall':
        df= df[df['user']==choice]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = []
    for message in temp['messages']:
        words.extend(message.lower().split())
    result_df = pd.DataFrame(Counter(words).most_common(20))
    return result_df

# emoji analysis
def emoji_helper(choice,df):
    if choice != 'Overall':
        df = df[df['user'] == choice]

    emojis = []
    for message in df['messages']:
        for char in message:
            # Check if the character is an emoji
            if emoji.is_emoji(char):
                # Add the emoji to the list
                emojis.append(char)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(choice, df):
    if choice!='Overall':
        df= df[df['user']==choice]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time']= time
    return timeline

def daily_timeline(choice, df):
    if choice!='Overall':
        df= df[df['user']==choice]
    dailytimeline = df.groupby(['only_date']).count()['messages'].reset_index()
    return dailytimeline


def week_activity_map(choice,df):

    if choice != 'Overall':
        df = df[df['user'] == choice]

    return df['day_name'].value_counts()

def month_activity_map(choice,df):

    if choice != 'Overall':
        df = df[df['user'] == choice]

    return df['month'].value_counts()

def activity_heatmap(choice,df):
    if choice != 'Overall':
        df = df[df['user'] == choice]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap