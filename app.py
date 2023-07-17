import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sb
st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    df= preprocessor.preprocess(data)
    st.dataframe(df)
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    choice = st.sidebar.selectbox('Show analysis wrt', user_list)
    if st.sidebar.button("Show Analysis"):
        # statistics
        num_messages, words, total_media, total_links = helper.fetch_stats(choice, df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(total_media)
        with col4:
            st.header('Links Shared')
            st.title(total_links)
        # timeline
        st.title("Monthy Timeline")
        timeline = helper.monthly_timeline(choice, df)
        fig, ax= plt.subplots()
        ax.plot(timeline['time'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        dailytimeline = helper.daily_timeline(choice, df)
        fig, ax = plt.subplots()
        ax.plot(dailytimeline['only_date'], dailytimeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(choice, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(choice, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(choice, df)
        fig, ax = plt.subplots()
        ax = sb.heatmap(user_heatmap)
        st.pyplot(fig)

    # finding busiet users
    if choice=='Overall':
        st.title('Most Busy Users')
        x,y=helper.busy_users(df)
        fig, ax= plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(y)

        # WordClouds
    df_wc = helper.display_wordcloud(choice, df)
    fig, ax= plt.subplots()
    ax.imshow(df_wc)
    st.title('WordCloud')
    st.pyplot(fig)

    df_common = helper.most_common_words(choice, df)
    fig,ax = plt.subplots()
    ax.barh(df_common[0], df_common[1])
    plt.xticks(rotation='vertical')
    st.title('Most common words')
    st.pyplot(fig)
    # st.dataframe(df_common)

    emoji_df= helper.emoji_helper(choice, df)
    st.title('Emoji Analysis')
    col1, col2= st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%.2f")
        st.pyplot(fig)




