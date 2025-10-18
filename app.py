import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import emoji
from matplotlib import rcParams
import seaborn as sns 

st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Stats Area
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    for unwanted in ['group_notification', 'Meta AI']:
        if unwanted in user_list:
            user_list.remove(unwanted)
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Analyze"):
        st.title("Top Statistics")
        num_messages, words, num_media_msg, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 =  st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Messages")
            st.title(num_media_msg)

        with col4:
            st.header("Total Links")
            st.title(links)
            
        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        # Busy user in the Group
        if selected_user == "Overall":
            st.title("Most Busy User")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("Most Common Messages")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)
        
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        
        st.title("Most Common Words")
        st.pyplot(fig)
        
        #  Emoji Analysis
        rcParams['font.family'] = 'Segoe UI Emoji'  # Windows

        emoji_df = helper.emoji_helper(selected_user, df).head(10)
        st.title("Emoji Analysis")

        col_left1, col_left2 = st.columns(2)
        half = len(emoji_df) // 2 + len(emoji_df) % 2

        with col_left1:
            for i, row in emoji_df.iloc[:half].iterrows():
                st.markdown(f"<span style='font-size:20px'>{row[0]}</span> {row[1]}", unsafe_allow_html=True)

        with col_left2:
            for i, row in emoji_df.iloc[half:].iterrows():
                st.markdown(f"<span style='font-size:20px'>{row[0]}</span> {row[1]}", unsafe_allow_html=True)

        col_right = st.columns(1)
        with col_right[0]:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], startangle=90, autopct='%1.1f%%', wedgeprops={'edgecolor':'white'})
            st.pyplot(fig)
                                