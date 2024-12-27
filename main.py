import asyncio
from crawler.async_runner import AsyncCrawler


def load_domains(file_path):
    """Load domains from a file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


async def main():
    domains = load_domains('data/domains.txt')
    crawler = AsyncCrawler(domains)
    await crawler.run()

    # Save output to JSON
    import json
    with open('data/output.json', 'w') as f:
        json.dump(crawler.product_urls, f, indent=4)

    print("Crawling complete! Results saved in data/output.json")


if __name__ == "__main__":
    asyncio.run(main())