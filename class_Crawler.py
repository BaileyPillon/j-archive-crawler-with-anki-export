import requests, time, logging
from bs4 import BeautifulSoup, ParserRejectedMarkup
from urllib.parse import urljoin, urlparse
from queue import Queue
from pybloom_live import BloomFilter
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()
first_iter = True
max_retries = 10

class Crawler():
    def __init__(self):
        self.base_url = "https://www.j-archive.com"
        self.pages_to_crawl = Queue()
        self.pages_to_crawl.put(self.base_url)
        self.pages_crawled = BloomFilter(capacity=1000000, error_rate=0.01)
        self.unsecure_url = "http://"

    def same_domain(self, url1, url2):
        return urlparse(url1).netloc == urlparse(url2).netloc

    def filter_url(self, url):
        return url.startswith("https://www.j-archive.com/showgame.php?game_id=")

    def crawl(self, url):
        first_iter = True
        while not crawler.pages_to_crawl.empty() or first_iter == True:
            first_iter = False
            if "search.php" in url:
                print(f"Skipping disallowed URL: {url}")
                continue
            if url in self.pages_crawled:
                print(f'Already crawled "{url}"')
                continue
            if url.startswith(self.unsecure_url):
                print(f'Encountered unsecure URL, skipping: "{url}"')
                continue
        try:
            response = session.get(url, timeout=5)                
            if "text/html" in response.headers["content-type"]:
                try:
                    soup = BeautifulSoup(response.text, 'html.parser')
                except ParserRejectedMarkup:
                    logging.error(f'Failed to parse "{url}"')
                    return
            if self.filter_url(url):
                self.pages_crawled.add(url)
                print(f'Successfully crawled and wrote "{url}".')
                logging.info(f'Crawled: {url}')
    
            # Enqueue same-domain URLs (ie, ensure crawler does not leave https://www.j-archive.com)
            for link in soup.find_all('a', href=True):
                url = urljoin(url, link['href'])
                if self.same_domain(url, self.base_url) and url not in self.pages_crawled and self.filter_url(url):
                    self.pages_to_crawl.put(url)
                    
        except requests.exceptions.RequestException as e:
            logging.error(f'Failed to crawl "{url}": {str(e)}')
            time.sleep(3)

if __name__ == "__main__":
    crawler = Crawler()
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
       while not crawler.pages_to_crawl.empty() or first_iter == True:
           url = crawler.pages_to_crawl.get()
           executor.submit(crawler.crawl, url)

    execution_time = (time.time() - start_time) / 60
    logging.info(f"Program executed in {execution_time:.2f} minutes.")
    execution_time = execution_time / 60
    logging.info(f"Program executed in {execution_time:.2f} hours.")
