import streamlit as st
from datetime import datetime, timedelta
from utils.article_scraper import fetch_articles

# Nastavení stylu stránky
st.set_page_config(page_title="Můj AI Digest", layout="wide")
st.markdown(
    """
    <style>
    body {
        font-family: Helvetica, sans-serif;
        background-color: white;
    }
    .title {
        text-align: center;
        font-weight: bold;
        font-size: 36px;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 2em;
    }
    .source-label {
        background-color: red;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 4px;
    }
    .article-title {
        font-size: 20px;
        font-weight: bold;
    }
    .article-perex {
        font-weight: 600;
    }
    .article-url {
        font-size: 12px;
        font-style: italic;
        color: blue;
    }
    hr {
        margin-top: 2em;
        margin-bottom: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Nadpis a popis
st.markdown('<div class="title">Můj AI Digest</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Aplikace pro výběr relevantních článků z vybraných zdrojů podle klíčových slov</div>', unsafe_allow_html=True)

# Výchozí hodnoty
default_sources = "www.zive.cz ; www.cnews.cz ; www.root.cz ; www.pctuning.cz ; www.seznam.cz ; www.seznamzpravy.cz ; www.novinky.cz ; www.idnes.cz ; www.aktualne.cz ; www.hn.cz ; www.denik.cz ; www.ceskatelevize.cz ; www.nova.cz ; www.iprima.cz"
default_keywords = "pojišťovnictví ; pojišťovna ; pojišťovny"
default_blacklist = "zdravotní pojištění ; sociální pojištění"
today = datetime.today().date()
year_ago = today - timedelta(days=365)

# Vstupní pole
sources_input = st.text_input("Zdroje", value=default_sources)
keywords_input = st.text_input("Klíčová slova", value=default_keywords)
blacklist_input = st.text_input("Blacklist slova", value=default_blacklist)
date_to = st.date_input("Datum nejnovějšího článku", value=today)
date_from = st.date_input("Datum nejstaršího článku", value=year_ago)

# Tlačítko pro načtení článků
if st.button("Načíst články"):
    st.markdown("<hr>", unsafe_allow_html=True)

    sources = [s.strip() for s in sources_input.split(";")]
    keywords = [k.strip() for k in keywords_input.split(";")]
    blacklist = [b.strip() for b in blacklist_input.split(";")]

    articles = fetch_articles(sources, keywords, blacklist, date_from, date_to)

    # Stránkování
    page_size = 10
    page = st.session_state.get("page", 0)
    total_pages = (len(articles) + page_size - 1) // page_size

    start_idx = page * page_size
    end_idx = start_idx + page_size
    for article in articles[start_idx:end_idx]:
        col1, col2 = st.columns([1, 4])
        with col1:
            if article["image"]:
                st.image(article["image"], use_column_width=True)
            else:
                st.markdown(f'<div class="source-label">{article["source"]}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="source-label">{article["source"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="article-title">{article["title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="article-perex">{article["perex"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="article-url">{article["url"]}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Navigace
    col_prev, col_next = st.columns([1, 1])
    if col_prev.button("← Předchozí"):
        if page > 0:
            st.session_state.page = page - 1
    if col_next.button("Další →"):
        if page < total_pages - 1:
            st.session_state.page = page + 1
