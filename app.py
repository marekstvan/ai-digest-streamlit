
import streamlit as st
import datetime

CONFIG_FILE = "config.txt"
DEFAULT_CONFIG = {
    "sources": "www.zive.cz;www.cnews.cz;www.root.cz;www.pctuning.cz;www.seznam.cz;www.seznamzpravy.cz;www.novinky.cz;www.idnes.cz;www.aktualne.cz;www.hn.cz;www.denik.cz;www.ceskatelevize.cz;www.nova.cz;www.iprima.cz",
    "keywords": "pojišťovnictví;pojišťovna;pojišťovny",
    "blacklist": "zdravotní pojištění;sociální pojištění",
    "date_from": str(datetime.date.today().replace(year=datetime.date.today().year - 1)),
    "date_to": str(datetime.date.today())
}

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        config = {}
        for line in lines:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key] = value
        return config
    except FileNotFoundError:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

def mock_fetch_articles(config):
    # Simulate fetching articles based on keywords and blacklist
    articles = []
    for i in range(1, 51):
        title = f"Článek {i}: Vývoj v pojišťovnictví"
        url = f"https://example.com/article{i}"
        if any(kw in title for kw in config["keywords"].split(";")) and not any(bl in title for bl in config["blacklist"].split(";")):
            articles.append({"title": title, "url": url})
    return articles

# Streamlit layout
st.set_page_config(layout="wide")
st.markdown("<style>div.block-container{max-width:1280px !important;}</style>", unsafe_allow_html=True)
st.title("📰 Můj AI Digest")

config = load_config()

with st.form("config_form"):
    sources = st.text_area("Zdroje (oddělené středníkem)", config.get("sources", ""))
    keywords = st.text_input("Klíčová slova (oddělená středníkem)", config.get("keywords", ""))
    blacklist = st.text_input("Blacklist slov (oddělený středníkem)", config.get("blacklist", ""))
    date_from = st.date_input("Datum od", datetime.date.fromisoformat(config.get("date_from", DEFAULT_CONFIG["date_from"])))
    date_to = st.date_input("Datum do", datetime.date.fromisoformat(config.get("date_to", DEFAULT_CONFIG["date_to"])))
    submitted = st.form_submit_button("💾 Uložit konfiguraci")

    if submitted:
        config["sources"] = sources
        config["keywords"] = keywords
        config["blacklist"] = blacklist
        config["date_from"] = str(date_from)
        config["date_to"] = str(date_to)
        save_config(config)
        st.success("Konfigurace byla uložena.")

if st.button("🔄 Načíst výchozí hodnoty"):
    config = DEFAULT_CONFIG.copy()
    save_config(config)
    st.experimental_rerun()

if st.button("🌐 Načíst články"):
    config = load_config()
    articles = mock_fetch_articles(config)
    st.session_state["articles"] = articles
    st.session_state["page"] = 1

# Pagination
articles = st.session_state.get("articles", [])
page = st.session_state.get("page", 1)
articles_per_page = 10
total_pages = (len(articles) - 1) // articles_per_page + 1

if articles:
    start = (page - 1) * articles_per_page
    end = start + articles_per_page
    for article in articles[start:end]:
        st.markdown(f"**[{article['title']}]({article['url']})**")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if page > 1 and st.button("⬅️ Předchozí"):
            st.session_state["page"] -= 1
            st.experimental_rerun()
    with col3:
        if page < total_pages and st.button("➡️ Další"):
            st.session_state["page"] += 1
            st.experimental_rerun()
    with col2:
        st.markdown(f"<p style='text-align:center;'>Stránka {page} z {total_pages}</p>", unsafe_allow_html=True)
