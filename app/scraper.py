import requests
from bs4 import BeautifulSoup
from app.utils import save_image_locally, retry
from db.db_manager import DBManager
from cache.cache_manager import CacheManager

class Scraper:
    def __init__(self, request):
        self.pages_limit = request.pages_limit
        self.proxy = {"http": request.proxy, "https": request.proxy} if request.proxy else None
        self.db_manager = DBManager()
        self.cache_manager = CacheManager()

    @retry
    def fetch_page(self, url):
        response = requests.get(url,proxies=self.proxy)
        response.raise_for_status()

        return response.text

    def parse_product(self, product_html):
        soup = BeautifulSoup(product_html, 'html.parser')

        # Extract title
        title_tag = soup.select_one("h2.woo-loop-product__title a")
        title = title_tag.text.strip() if title_tag else "N/A"
         # Extract current price
        current_price_tag = soup.select_one("span.price span.woocommerce-Price-amount bdi")
        if current_price_tag:
            try:
                current_price = float(current_price_tag.text.replace("₹", "").replace(",", "").strip())
            except ValueError:
                current_price = 0.0
        else:
            current_price = 0.0

        # Extract original price

        # Extract image URL
        img_tag = soup.select_one("div.mf-product-thumbnail img")
        img_url = img_tag["src"] if img_tag else None
        img_path = save_image_locally(img_url) if img_url else "N/A"

        return {
            "product_title": title,
            "current_price": current_price,
            "path_to_image": img_path
        }

    def run(self):
        base_url = "https://dentalstall.com/shop/"
        page = 1
        scraped_data = []

        while not self.pages_limit or page <= self.pages_limit:
            url = f"{base_url}/page/{page}/"
            html_content = self.fetch_page(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            products = soup.select("div.product-inner.clearfix")

            for product in products:
                parsed_product = self.parse_product(str(product))

                if not self.cache_manager.is_price_changed(parsed_product):
                    continue

                scraped_data.append(parsed_product)
                self.db_manager.save_product(parsed_product)

            page += 1

        print(f"Scraped {len(scraped_data)} products")
        return scraped_data
