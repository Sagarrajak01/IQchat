# 💬 WhatsApp Chat Analyzer

A Streamlit web app that analyzes WhatsApp chat exports to generate insights such as message count, word frequency, media usage, active users, and word clouds.

---

## 🚀 Features

* View overall or per-user chat statistics
* Generate a word cloud for message content
* Identify the most active users
* Analyze text vs media messages
* Detect shared links automatically
* Emoji analysis with colorful visual charts 🎨

---

## 🧩 Tech Stack

* **Python 3.10+**
* **Streamlit** for web UI
* **Pandas** for data processing
* **Matplotlib** for visualizations
* **WordCloud** for text visualization
* **URLEXtract** for link extraction

---

## ⚙️ Setup Instructions

```bash
# 1. Clone this repo
git clone https://github.com/Sagarrajak01/Whatsapp-chat-analysis.git
cd Whatsapp-chat-analysis

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # (on Windows)
source .venv/bin/activate  # (on macOS/Linux)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py

🗂️ Project Structure

📁 Whatsapp-chat-analysis/
├── app.py
├── helper.py
├── preprocessor.py
├── requirements.txt
├── README.md
└── .gitignore


📊 Example Output
Total messages and words
Most active users
Word cloud of frequently used words
Number of links and media messages
Emoji analysis showing most used emojis with pie chart and counts 🧠

🧠 Future Improvements

Sentiment analysis per user
Chat timeline visualization
Enhanced emoji color analytics
User interaction graph using NetworkX