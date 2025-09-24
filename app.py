import streamlit as st
import datetime

# Constants
PAGE_WIDTH = 1280
ARTICLES_PER_PAGE = 10

# Default configuration
default_config = {
    "sources": ["https://www.rozhlas.cz", "https://www.novinky.cz", "https://www.seznamzpravy.cz"],
    "keywords": ["pojištění", "pojistka", "riziko", "škoda", "úraz", "zabezpečení", "odpovědnost"],
    "blacklist": ["sport", "celebrita", "recept", "bulvár"],
    "date_from": (datetime.date.today() - datetime.timedelta(days=365)).isoformat(),
    "date_to": datetime.date.today().isoformat()
}

# Session state initialization
if "config" not in st.session_state:
    st.session_state.config = default_config.copy()

# Layout settings
st.set_page_config(layout="wide")
st.markdown("<style>.reportview-container .main { max-width: 1280px; margin: auto; }</style>", unsafe_allow_html=True)

st.title("Můj AI Digest")

# Configuration editor
st.subheader("Konfigurace")
sources = st.text_area("Seznam zdrojů (oddělené čárkou)", ", ".join(st.session_state.config["sources"]))
keywords = st.text_area("Klíčová slova (oddělená čárkou)", ", ".join(st.session_state.config["keywords"]))
blacklist = st.text_area("Blacklist slov (oddělený čárkou)", ", ".join(st.session_state.config["blacklist"]))
date_from = st.date_input("Nejstarší datum článku", datetime.date.fromisoformat(st.session_state.config["date_from"]))
date_to = st.date_input("Nejnovější datum článku", datetime.date.fromisoformat(st.session_state.config["date_to"]))

# Buttons to load default or updated config
col1, col2 = st.columns(2)
with col1:
    if st.button("Načíst výchozí konfiguraci"):
        st.session_state.config = default_config.copy()
        st.experimental_rerun()
with col2:
    if st.button("Načíst upravenou konfiguraci"):
        st.session_state.config = {
            "sources": [s.strip() for s in sources.split(",")],
            "keywords": [k.strip() for k in keywords.split(",")],
            "blacklist": [b.strip() for b in blacklist.split(",")],
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat()
        }

# Placeholder for article loading and filtering
st.subheader("Výpis článků")
st.info("Zde budou zobrazeny články podle zadané konfigurace. Funkce načítání a filtrování článků zatím není implementována.")
