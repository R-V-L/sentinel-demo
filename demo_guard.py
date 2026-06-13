# Celda 1
!pip install requests beautifulsoup4 pandas

# Celda 2
import requests

BASE = "https://rivazql.pythonanywhere.com/guard"
resp = requests.get(f"{BASE}/")
print(f"SIN headers: {resp.status_code}")

# Celda 3
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0.0.0",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "es-MX,es;q=0.9",
}

resp = requests.get(f"{BASE}/", headers=headers)
print(f"CON headers: {resp.status_code}")

# Celda 4
import pandas as pd
from bs4 import BeautifulSoup

MAX_PAGES = 1

productos = []
page = 1

while True:
    resp = requests.get(f"{BASE}/?page={page}", headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select("a[href*='/guard/product/']")

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
