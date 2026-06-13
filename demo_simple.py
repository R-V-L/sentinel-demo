# Celda 1
!pip install requests beautifulsoup4 pandas

# Celda 2
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE = "https://rivazql.pythonanywhere.com/simple"
MAX_PAGES = 1

productos = []
page = 1

while True:
    resp = requests.get(f"{BASE}/?page={page}")
    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select("a[href*='/simple/product/']")

    if not cards:
        break

    for card in cards:
        productos.append({
            "nombre": card.select_one("h3").text.strip(),
            "precio": card.select_one("p.text-xl").text.strip(),
            "marca":  card.select_one("span.text-xs").text.strip(),
            "stock":  "En stock" in card.select_one("span.rounded-full").text,
        })

    if MAX_PAGES and page >= MAX_PAGES:
        break

    page += 1

df = pd.DataFrame(productos)
print(f"Extraídos: {len(df)} productos")
df.head(10)
