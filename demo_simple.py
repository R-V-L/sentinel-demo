# Celda 1
!pip install requests beautifulsoup4 pandas

# Celda 2
import requests
import pandas as pd
import math
from bs4 import BeautifulSoup

BASE = "https://rivazql.pythonanywhere.com/simple"

resp = requests.get(f"{BASE}/")
soup = BeautifulSoup(resp.text, "html.parser")

total_text = soup.find("span", class_="text-gray-500").text
total_productos = int(total_text.split()[-2])
total_paginas = math.ceil(total_productos / 12)

productos = []
for page in range(1, total_paginas + 1):
    resp = requests.get(f"{BASE}/?page={page}")
    soup = BeautifulSoup(resp.text, "html.parser")
    for card in soup.select("a[href*='/simple/product/']"):
        productos.append({
            "nombre": card.select_one("h3").text.strip(),
            "precio": card.select_one("p.text-xl").text.strip(),
            "marca":  card.select_one("span.text-xs").text.strip(),
            "stock":  "En stock" in card.select_one("span.rounded-full").text,
        })

df = pd.DataFrame(productos)
print(f"Total extraídos: {len(df)} productos")
df
