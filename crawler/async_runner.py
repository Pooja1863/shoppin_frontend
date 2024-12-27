import asyncio
import aiohttp
from bs4 import BeautifulSoup


class AsyncCrawler:
    def _init_(self, domains):
        self.domains = domains
        self.product_urls = {}

    def is_product_url(self, url):
        """Check if the URL matches a product pattern."""
        return any(part in url for part in ['/product/', '/item/', '/p/'])

    async def fetch(self, session, url):
        """Fetch the content of a URL."""
        try:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return ''
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ''

    async def crawl_domain(self, domain):
        """Crawl a single domain asynchronously."""
        product_urls = set()
        visited = set()
        queue = [f"http://{domain}"]

        async with aiohttp.ClientSession() as session:
            while queue:
                url = queue.pop(0)
                if url in visited:
                    continue
                visited.add(url)
                html = await self.fetch(session, url)
                if not html:
                    continue

                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_url = link['href']
                    if self.is_product_url(full_url):
                        product_urls.add(full_url)
                    elif full_url.startswith(f"http://{domain}") and full_url not in visited:
                        queue.append(full_url)

        self.product_urls[domain] = list(product_urls)

    async def run(self):
        """Run the crawler across all domains."""
        tasks = [self.crawl_domain(domain) for domain in self.domains]
        await asyncio.gather(*tasks)