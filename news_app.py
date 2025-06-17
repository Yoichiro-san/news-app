import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import re

def classify_category(text):
    text = text.lower()
    if any(word in text for word in ["report", "insight", "analysis", "trend", "white paper"]):
        return "I：Insight"
    elif any(word in text for word in ["event", "seminar", "webinar", "book", "publication"]):
        return "M：Marketing"
    elif any(word in text for word in ["service", "product", "solution", "launch", "release"]):
        return "S：Service"
    elif any(word in text for word in ["appointment", "investment", "acquisition", "merger", "restructuring", "personnel", "partnership"]):
        return "C：Company"
    else:
        return "I：Insight"  # デフォルトカテゴリ

def fetch_deloitte_news_april2025():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    query = "deloitte after:2025-04-01 before:2025-04-30"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.select(".dbsr"):
        title = result.select_one("div.JheGif.nDgy9d").text
        link = result.a["href"]
        snippet = result.select_one("div.Y3v8qd").text if result.select_one("div.Y3v8qd") else ""
        full_text = f"{title} {snippet}"
        category = classify_category(full_text)

        # 掲載日（取得できる場合）
        date_elem = result.select_one("span.WG9SHc span")
        published = date_elem.text if date_elem else "N/A"

        results.append({
            "タイトル": title,
            "カテゴリ": category,
            "要約": snippet,
            "出典リンク": link,
            "掲載日": published
        })

    return results

# --- Streamlit アプリ ---
st.title("デロイトのニュース（2025年4月） - カテゴリ付き")

if st.button("ニュースを取得"):
    news_items = fetch_deloitte_news_april2025()
    if news_items:
        df = pd.DataFrame(news_items)
        st.dataframe(df)
    else:
        st.warning("ニュースが取得できませんでした。")
