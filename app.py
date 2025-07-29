import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns

import preprocessor
import helper

st.sidebar.title('WhatsApp-Chat-Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    sender = df['Sender'].unique().tolist()
    sender.remove('System')
    sender.sort()
    sender.insert(0,'Group Members')
    selected_user = st.sidebar.selectbox("Show Analysis",sender)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_msg, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

    # Monthly Timeline
    st.header("Monthly TimeLine")
    timeline_df = helper.monthly_timeline(selected_user,df)
    fig, ax = plt.subplots()
    ax.plot(timeline_df['time'],timeline_df['Message'],color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Daily Timeline
    st.header("Daily TimeLine")
    daily_timeline_df = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline_df['date'], daily_timeline_df['Message'], color='pink')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Activity Map
    st.title('Week Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.most_busy_day(selected_user, df,)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most busy Month")
        busy_month = helper.most_busy_month(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    #finding the busiest user of the group (Group Level)
    if selected_user == 'Group Members':
        st.title("Most Busy Users")
        x, new_df = helper.most_busy_users(df)
        fig , ax = plt.subplots()

        col1, col2 = st.columns(2)
        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # Creating WordCloud
    st.header("WordCloud")
    df_wc = helper.create_wordcloud(selected_user,df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # Most common words
    st.header("Common words used")
    common_words_df = helper.most_common_words(selected_user,df)
    fig, ax = plt.subplots()
    ax.barh(common_words_df[0], common_words_df[1],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Emoji Analysis
    st.header("Emojis count")
    emoji_df = helper.emoji_count(selected_user,df)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        top_emojis = emoji_df.head(10)
        fig, ax = plt.subplots()
        ax.bar(top_emojis['Emoji'], top_emojis['Count'], color='skyblue')
        st.pyplot(fig)

    # active time Heatmap
    st.header("Active time Heatmap")
    heatmap = helper.activity_heatmap(selected_user,df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(heatmap, cmap='YlGnBu')
    st.pyplot(fig)

