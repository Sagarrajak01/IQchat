import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt

st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Stats Area
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.remove('Meta AI')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Analyze"):

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

