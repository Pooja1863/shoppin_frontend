import requests
from bs4 import BeautifulSoup


class Crawler:
    def _init_(self, domain):
        self.domain = domain
        self.visited = set()
        self.product_urls = set()

    def is_product_url(self, url):
        """Check if the URL points to a product page."""
        return any(part in url for part in ['/product/', '/item/', '/p/'])

    def crawl(self, url):
        """Recursively crawl URLs to find product links."""
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = link['href']
                if self.is_product_url(full_url):
                    self.product_urls.add(full_url)
                elif full_url.startswith(f"http://{self.domain}"):
                    self.crawl(full_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def get_product_urls(self):
        return list(self.product_urls)