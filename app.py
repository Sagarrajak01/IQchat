import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import emoji 
from matplotlib import rcParams
import seaborn as sns
import pandas as pd

st.set_page_config(page_title="IQchat - WhatsApp Analyzer", layout="wide")

# CSS
def load_css(file_path):
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ CSS file not found. The app will still run, but without custom styling.")

load_css("style.css")

# Header and Instructions
st.markdown("""
<div class='header'>
    <h1>💬 IQchat - WhatsApp Chat Analyzer</h1>
    <p>AI-powered insights by Sagar Rajak</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='howto-box'>
<ol class='howto-list'>
<li><b>Export your WhatsApp chat</b> (without media)<br>
→ Open chat → Tap <b>⋮</b> → <i>More</i> → <i>Export Chat</i> → <i>Without Media</i><br>
📄 A <code>.zip</code> file will be generated. Unzip it</li>
<li><b>Upload your exported txt file</b> below.<br>
📦 Supports <code>.txt</code> file</li>
<li><b>Wait a few seconds</b> — IQchat will analyze your chat and show:<br>
• Total messages, words, and links<br>
• Most active users<br>
• Word cloud<br>
• Emoji analysis with colorful charts 🎨</li>
<li><b>Privacy First 🔒</b> — No data is stored or sent. Everything runs in your browser.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# File Uploader
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp txt file", type=["txt"])

if uploaded_file is not None:
    try:
        # Read and decode the file data
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode('utf-8', errors='ignore')
        
        # Preprocess the data
        df = preprocessor.preprocess(data)

        if df is None or df.empty or 'user' not in df.columns:
            st.error("Could not read valid chat data from file. Make sure you exported correctly.")
            st.stop()

        # Prepare user list for selection
        user_list = df['user'].dropna().unique().tolist()
        for unwanted in ['group_notification', 'Meta AI']:
            if unwanted in user_list:
                user_list.remove(unwanted)
        user_list.sort()
        user_list.insert(0, "Overall")

        # Sidebar selection
        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        # Analysis button
        if st.sidebar.button("Analyze"):
            st.title("Top Statistics")
            
            # 1. Fetch Top Statistics
            try:
                num_messages, words, num_media_msg, links = helper.fetch_stats(selected_user, df)
            except Exception as e:
                st.error(f"Error fetching stats: {e}")
                st.stop()

            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Total Messages", num_messages)
            with col2: st.metric("Total Words", words)
            with col3: st.metric("Media Messages", num_media_msg)
            with col4: st.metric("Links", links)

            # 2. Monthly Timeline
            st.title("Monthly Timeline")
            try:
                timeline = helper.monthly_timeline(selected_user, df)
                if not timeline.empty:
                    fig, ax = plt.subplots()
                    ax.plot(timeline['time'], timeline['message'], color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                else:
                    st.info("No timeline data available.")
            except Exception as e:
                st.warning(f"Could not plot timeline: {e}")

            # 3. Daily Timeline
            st.title("Daily Timeline")
            try:
                daily_timeline = helper.daily_timeline(selected_user, df)
                if not daily_timeline.empty:
                    fig, ax = plt.subplots()
                    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                else:
                    st.info("No daily activity data found.")
            except Exception as e:
                st.warning(f"Could not plot daily timeline: {e}")

            # 4. Activity Map (Most Busy Day/Month)
            st.title('Activity Map')
            col1, col2 = st.columns(2)
            with col1:
                st.header("Most Busy Day")
                try:
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index, busy_day.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                except Exception:
                    st.info("No data for busy day chart.")

            with col2:
                st.header("Most Busy Month")
                try:
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values, color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                except Exception:
                    st.info("No data for busy month chart.")

            # 5. Weekly Activity Heatmap
            st.title("Weekly Activity Map")
            try:
                user_heatmap = helper.activity_heatmap(selected_user, df)
                if user_heatmap is None or user_heatmap.empty:
                    st.warning("No activity data available for this user.")
                else:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.heatmap(
                        user_heatmap,
                        cmap="YlGnBu",
                        linewidths=0.5,
                        linecolor='gray',
                        annot=True,
                        fmt=".0f",
                        cbar_kws={'label': 'Message Count'}
                    )
                    ax.set_xlabel("Period of Day")
                    ax.set_ylabel("Day of Week")
                    plt.xticks(rotation=45, ha='right')
                    plt.yticks(rotation=0)
                    st.pyplot(fig)
            except Exception as e:
                st.warning(f"Error generating heatmap: {e}")

            # 6. Most Busy User (Overall Chat)
            if selected_user == "Overall":
                st.title("Most Busy User")
                try:
                    x, new_df = helper.most_busy_users(df)
                    
                    if not new_df.empty:
                        col1, col2 = st.columns(2)
                    
                        with col1:
                            st.subheader("Top 5 Users (Message Count)")
                            fig, ax = plt.subplots(figsize=(6, 4)) 
                            ax.bar(x.index, x.values)
                            plt.xticks(rotation=90)
                            st.pyplot(fig)
                            plt.close(fig)

                        with col2:
                            st.subheader("Message Share (%)")
                            df_display = new_df.head(10).copy()
                            df_display.index = pd.RangeIndex(1, len(df_display) + 1)
                            df_display.index.name = "Rank" 
                            
                            st.dataframe(
                                df_display
                                    .style
                                    .format({'percent': "{:.2f}%"}) 
                                    .set_properties(**{'border': '1px solid #E0E0E0', 
                                                    'padding': '8px'}),
                                use_container_width=True, 
                                height=350
                            )
                    else:
                        st.info("No busy user data found.")
                except Exception as e:
                    st.warning(f"Error fetching busy users: {e}")
        
            # 7. Word Cloud
            st.title("Most Common Messages")
            try:
                df_wc = helper.create_word_cloud(selected_user, df)
                if df_wc is not None:
                    fig, ax = plt.subplots()
                    plt.imshow(df_wc)
                    plt.axis("off")
                    st.pyplot(fig)
                else:
                    st.info("No valid messages for word cloud.")
            except Exception as e:
                st.warning(f"Word cloud error: {e}")

            # 8. Most Common Words (Bar Chart)
            st.title("Most Common Words")
            try:
                most_common_df = helper.most_common_words(selected_user, df)
                if not most_common_df.empty:
                    fig, ax = plt.subplots()
                    ax.barh(most_common_df[0], most_common_df[1])
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                else:
                    st.info("No common words found.")
            except Exception as e:
                st.warning(f"Error plotting common words: {e}")

            # 9. Emoji Analysis
            st.title("Emoji Analysis")
            try:
                rcParams['font.family'] = 'Segoe UI Emoji'
                emoji_df = helper.emoji_helper(selected_user, df).head(10)
                if emoji_df.empty:
                    st.info("No emoji data available.")
                else:
                    col_left1, col_left2 = st.columns(2)
                    half = len(emoji_df) // 2 + len(emoji_df) % 2
                    
                    # Display emojis and counts
                    with col_left1:
                        for i, row in emoji_df.iloc[:half].iterrows():
                            st.markdown(f"<span style='font-size:20px'>{row[0]}</span> {row[1]}", unsafe_allow_html=True)
                    with col_left2:
                        for i, row in emoji_df.iloc[half:].iterrows():
                            st.markdown(f"<span style='font-size:20px'>{row[0]}</span> {row[1]}", unsafe_allow_html=True)
                    
                    # Display Pie Chart
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df[1], labels=emoji_df[0],
                            startangle=90, autopct='%1.1f%%',
                            wedgeprops={'edgecolor': 'white'})
                    st.pyplot(fig)
            except Exception as e:
                st.warning(f"Emoji analysis failed: {e}")
    
    except Exception as e:
        st.error(f"Unexpected error while processing file: {e}")