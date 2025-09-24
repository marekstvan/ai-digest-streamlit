import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_articles(sources, keywords, blacklist, date_from, date_to):
    # Mockovací funkce pro demonstraci
    # V reálné verzi by se zde parsovaly RSS feedy nebo HTML stránky
    articles = []
    for source in sources:
        for i in range(3):  # simulace 3 článků na zdroj
            title = f"Ukázkový článek {i+1} ze {source}"
            perex = "Toto je ukázkový perex článku, který se týká pojišťovnictví."
            url = f"https://{source}/clanek/{i+1}"
            image = None  # nebo URL obrázku
            date = datetime.today().date()

            if date_from <= date <= date_to:
                if any(kw.lower() in title.lower() or kw.lower() in perex.lower() for kw in keywords):
                    if not any(bl.lower() in title.lower() or bl.lower() in perex.lower() for bl in blacklist):
                        articles.append({
                            "source": source,
                            "title": title,
                            "perex": perex,
                            "url": url,
                            "image": image
                        })
    return articles
