import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for item in soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        name = item.find("h3").find("a")["title"]
        price_raw = item.find("p", class_="price_color").get_text(strip=True)
        price = float(
            price_raw.replace("Â", "").replace(",", "").replace("£", "")
        )

        products.append({
            "product_name": name,
            "price": price
        })
    return products

def save_timestamped_csv(data):
    date_str = datetime.now().strftime("%Y_%m_%d")
    filename = f"prices_{date_str}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return filename

def generate_summary(data):
    prices = [item["price"] for item in data]

    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)

    summary = (
        f"\nOn the latest scrape ->"
        f"\n* {len(prices)} products were tracked."
        f"\n* The average price across products is £{avg_price:.2f}."
        f"\n* Prices ranged from £{min_price:.2f} to £{max_price:.2f}."
        f"\nThis snapshot provides a baseline for monitoring future price changes."
    )
    return summary

# ---- Test URL ----
URL = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

html = fetch_html(URL)
products = parse_products(html)
csv_file = save_timestamped_csv(products)
insights = generate_summary(products)

print("\nData saved to {csv_file}")
print("\nINSIGHTS:")
print(insights)