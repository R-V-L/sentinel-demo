# Celda 1
!pip install requests pandas beautifulsoup4

# Celda 2
import requests
from bs4 import BeautifulSoup

BASE = "https://rivazql.pythonanywhere.com/dynamic"
resp = requests.get(f"{BASE}/")
soup = BeautifulSoup(resp.text, "html.parser")
cards = soup.select("a[href*='/dynamic/product/']")
print(f"Productos en el HTML: {len(cards)}")

# Celda 3
import pandas as pd

resp = requests.get(f"{BASE}/api/products")
data = resp.json()
df = pd.DataFrame(data)

print(f"Productos en la API: {len(df)}")
df.head(10)
