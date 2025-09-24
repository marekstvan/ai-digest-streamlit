import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import math

# Title of the app
st.title("Můj AI Digest")

# Input fields
urls_input = st.text_area("Zadejte URL adresy (každá na nový řádek):")
keywords_input = st.text_input("Zadejte klíčová slova (oddělená čárkou):")
blacklist_input = st.text_input("Zadejte blacklist slova (oddělená čárkou):")

# Pagination settings
items_per_page = 5
page = st.number_input("Stránka", min_value=1, value=1)

# Process inputs
urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
keywords = [kw.strip().lower() for kw in keywords_input.split(",") if kw.strip()]
blacklist = [bl.strip().lower() for bl in blacklist_input.split(",") if bl.strip()]

def fetch_and_filter(url, keywords, blacklist):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "Bez názvu"
        text = soup.get_text().lower()
        if any(kw in text for kw in keywords) and not any(bl in text for bl in blacklist):
            img_tag = soup.find("img")
            img_url = urljoin(url, img_tag['src']) if img_tag and img_tag.get('src') else None
            perex = ' '.join(text.split()[:50]) + "..."
            return {"url": url, "title": title, "img": img_url, "perex": perex}
    except Exception:
        return None
    return None

# Collect results
results = []
for url in urls:
    result = fetch_and_filter(url, keywords, blacklist)
    if result:
        results.append(result)

# Pagination logic
total_pages = math.ceil(len(results) / items_per_page)
start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_results = results[start_idx:end_idx]

# Display results
for res in paginated_results:
    st.subheader(res["title"])
    if res["img"]:
        st.image(res["img"], use_column_width=True)
    st.write(res["perex"])
    st.markdown(f"[Otevřít článek]({res['url']})")

# Display page info
st.write(f"Stránka {page} z {total_pages}")
