import requests, queue, time, logging, posixpath
from bs4 import BeautifulSoup
from pybloom_live import BloomFilter
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from urllib.parse import urlunparse, urlencode, parse_qs, urlparse, urljoin

# Set up logging
logging.basicConfig(filename='j-archive-game-ids.log', level=logging.INFO)

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.pages_to_crawl = queue.Queue()
        self.pages_to_crawl.put(self.base_url)
        self.pages_crawled = BloomFilter(capacity=1000000, error_rate=0.1)  # Using a Bloom filter here
        self.session = requests.Session()
        self.unsecure_url = 'http://'
        self.request_interval = 1.0
        self.min_request_interval = 0.5
        self.max_request_interval = 5.0
        self.max_retries = 3

    def get_page_content(self, url):
        try:
            # Get page content
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                if 'text/html' in response.headers['Content-Type']:
                    return BeautifulSoup(response.text, 'html.parser')
                else:
                    logging.info(f"Unhandled content type at {response.url}")
            elif response.status_code == 404:
                logging.info(f"404 error at {response.url}")
            else:
                logging.info(f"{response.status_code} error at {response.url}")
        except RequestException as e:
            logging.error(f'Failed to crawl "{url}": {str(e)}')
        return None

    def normalize_url(self, url):
        # Parse the url
        parts = urlparse(url)

        # Normalize path by removing duplicate slashes, "." and ".."
        path = parts.path
        if '//' in path or '/./' in path or '/..' in path:
            path = posixpath.normpath(path)

        # Normalize query by sorting it
        query = parts.query
        if query:
            query_dict = parse_qs(query)
            sorted_query = sorted((k, sorted(v)) for k, v in query_dict.items())
            query = urlencode(sorted_query, doseq=True)

        # Recreate the URL
        normalized_url = urlunparse(
            (parts.scheme, parts.netloc, path, parts.params, query, parts.fragment)
        )

        return normalized_url

    def extract_links(self, url, soup):
        # Extract links from the page
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            
            # Converts a relative link to an absolute link
            if not bool(urlparse(link_url).netloc):
                link_url = urljoin(url, link_url)

            if link_url not in self.pages_crawled:
                self.pages_to_crawl.put(link_url) # Queue link to be crawled

    def same_domain(self, url1, url2):
        """ Enqueue the same domain """
        return urlparse(url1).netloc == urlparse(url2).netloc
 
    def should_crawl(self, url):
        url = self.normalize_url(url)
        if "search.php" in url:
            print(f"Skipping disallowed URL: {url}") # Respect robots.txt
            return False
        if url in self.pages_crawled:
            print(f'Already crawled "{url}"')
            return False
        if url.startswith("https://www.j-archive.com/") and not url.startswith("https://www.j-archive.com/showgame.php?game_id="):
            return False
        if url.startswith(self.unsecure_url):
            print(f'Encountered unsecure URL, skipping: "{url}"')
            return False
        if not self.same_domain(self.base_url, url):
            return False
        return True    
 
    def crawl(self, url):
        if not self.should_crawl(url):
            return

        soup = self.get_page_content(url)
        if soup is not None:
            self.extract_links(url, soup)

            if "showgame" in url:
                print(f'Crawled desired URL: {url}')
                logging.info(f'{url}')
            else:
                print(f'Crawled: {url}')
            
            # Mark the URL as crawled
            self.pages_crawled.add(url)
            
        # Respect robots.txt
        #print("Waiting 20 seconds...") # Uncomment this
        #time.sleep(20) # Uncomment this

    def start_crawling(self):
        futures = set()
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                try:
                    url = self.pages_to_crawl.get(timeout=3)
                except queue.Empty:
                    break
                else:
                    future = executor.submit(self.crawl, url)
                    futures.add(future)
        wait(futures)  # Wait for all threads to complete

def main():
    start_time = time.time() # Start program execution timer
    base_url = 'https://www.j-archive.com'
    crawler = Crawler(base_url)
    crawler.start_crawling()
    
    # Program execution time
    execution_time = (time.time() - start_time) / 60
    print((f"Program executed in {execution_time:.2f} minutes."))
    execution_time = execution_time / 60
    print((f"Program executed in {execution_time:.2f} hours."))

if __name__ == "__main__":
    main()
