import streamlit as st
import requests
from bs4 import BeautifulSoup
import configparser

config = configparser.ConfigParser()
config.read("config.txt", encoding="utf-8")

sources = config.get("Sources", "urls").split(",")
keywords = config.get("Keywords", "include").split(",")
blacklist = config.get("Blacklist", "exclude").split(",")
layout_width = config.get("Layout", "width")
articles_per_page = config.getint("Layout", "articles_per_page")

st.set_page_config(layout="wide")
st.markdown(f"<style>.reportview-container .main {{ max-width: {layout_width}; margin: auto; }}</style>", unsafe_allow_html=True)
st.title("Můj AI Digest")

def fetch_articles():
    articles = []
    for url in sources:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all("a", href=True):
                text = link.get_text().strip()
                href = link["href"]
                if any(kw.lower() in text.lower() for kw in keywords) and not any(bl.lower() in text.lower() for bl in blacklist):
                    articles.append({"title": text, "url": href})
        except Exception as e:
            st.error(f"Chyba při načítání z {url}: {e}")
    return articles

all_articles = fetch_articles()
total_pages = (len(all_articles) + articles_per_page - 1) // articles_per_page
page = st.sidebar.slider("Stránka", 1, total_pages, 1)

start = (page - 1) * articles_per_page
end = start + articles_per_page
for article in all_articles[start:end]:
    st.subheader(article["title"])
    st.markdown(f"[Otevřít článek]({article['url']})")
