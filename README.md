# 🛍️ Amazon Review Analyzer

A full-stack application that scrapes and analyzes Amazon product reviews using NLP. It provides average ratings, top keywords, sentiment analysis, and a smart summary — all powered by Python (Flask) and React.

---

## 🚀 Features

- 🔍 **Web Scraping**: Parses Amazon product reviews in real time
- 📊 **Average Rating**: Extracts and calculates numerical review ratings
- 💬 **Top Words**: Shows most common keywords across reviews
- 🧠 **Sentiment Analysis**: Understands customer sentiment using VADER
- ✂️ **Summarization**: Uses HuggingFace Transformers to summarize all reviews
- ⚡ **Responsive Frontend**: Built with React and served via Flask in a monolithic architecture

---

## 🧠 Tech Stack




| Frontend | Backend | NLP / AI | Dev Tools |
|----------|---------|----------|-----------|
| React.js | Flask   | NLTK, HuggingFace Transformers | Python, Vite, BeautifulSoup, Requests |


i used react.js  to build fast, interactive modern user interface.

I used Flaks to process the review data and communnicate with NLP tools.

I used NLTK to extract meaningfull patterns from raw review text.

I used HuggingFace Transformers for  high-quality abstractive summarization of all reviews.

BeautifulSoup & Selenium – Scrapes structured data from Amazon pages reliably, with stealth options for headless Chrome.



---

## Architechture

monolithic architecture where both the frontend and backend are combined into a single deployable unit.


## 🖼️ Screenshots

![alt text](image.png)

---

## 🛠️ Setup Instructions

in terminal:

- **navigate to server:** cd server

- **Install pytho dependencies:** pip install -r requirements.txt

- **Run the Backend:** python server.py

## 🎯 Why This Project Stands Out

-  **Combines real-world web scraping with modern NLP techniques**.
-  **Demonstrates full-stack development skills: React frontend + Flask backend**.
- **Shows ability to handle headless browser automation, data extraction, and intelligent summarization**.

