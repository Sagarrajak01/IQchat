# IQchat

A Streamlit web app to explore and visualize WhatsApp chat data. IQchat helps you gain insights into your chats, including message statistics, media usage, most active users, and emoji trends.

---

## Features

* **Chat Stats:** Overall or per-user statistics including message and word counts.
* **Word Cloud:** Visualize frequently used words.
* **Active Users:** Identify who sends the most messages.
* **Media & Links:** Analyze text vs media messages and automatically detect shared links.
* **Emoji Analysis:** Colorful charts showing emoji usage.

---

## Tech Stack

* **Python 3.10+**
* **Streamlit** for the web interface
* **Pandas** for data manipulation
* **Matplotlib** for visualizations
* **WordCloud** for text visualization
* **URLEXtract** for detecting links

---

## Setup Instructions

```bash
# 1. Clone this repository
git clone https://github.com/Sagarrajak01/Whatsapp-chat-analysis.git
cd Whatsapp-chat-analysis

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## Project Structure

```
Whatsapp-chat-analysis/
├── app.py
├── helper.py
├── preprocessor.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Example Output

* Total messages and words per user or overall
* Most active users
* Word cloud of frequently used words
* Number of media messages and links shared
* Emoji usage with colorful charts

---

## Future Improvements

* Sentiment analysis per user
* Timeline visualization of chat activity
* Enhanced emoji color analytics
* User interaction graph using **NetworkX**

---

## Acknowledgements

This project was developed under the guidance of **Mr. Sushil Kumar, NIT Trichy**. Special thanks for valuable insights and support throughout the project.
