import requests
from bs4 import BeautifulSoup
#from urllib.parse import urlparse, urljoin
import queue
from pybloom_live import BloomFilter
#from urllib.robotparser import RobotFileParser
import logging
from requests.exceptions import RequestException
import time
from concurrent.futures import ThreadPoolExecutor
import os
from concurrent.futures import wait
from urllib.parse import urlunparse, urlencode, parse_qs, quote, unquote, urlparse, urljoin
import posixpath



# Set up logging
logging.basicConfig(filename='j-archive-game-ids-v18.log', level=logging.INFO)

#session = requests.Session()


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
        self.max_retries = 10
        #self.session.headers.update({'User-Agent': 'My Crawler/1.0'})
        #self.robot_parser = RobotFileParser()
        #self.robot_parser.set_url(urljoin(base_url, 'robots.txt'))
        #self.robot_parser.read()

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

    def handle_response(self, response):
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        elif response.status_code == 404:
            logging.info(f"404 error at {response.url}")
        else:
            logging.info(f"{response.status_code} error at {response.url}")
        return None

    def normalize_url(self, url):
        scheme, netloc, path, params, query, fragment = urlparse(url)

        netloc = netloc.lower()
        path = posixpath.normpath(unquote(path.lower()))

        query_dict = parse_qs(query)
        normalized_query = urlencode(sorted((k, sorted(v)) for k, v in query_dict.items()), doseq=True)

        fragment = ''

        return urlunparse((scheme, netloc, path, params, normalized_query, fragment))


    def extract_links(self, url, soup):
        # Extract links from the page
        for link in soup.find_all('a', href=True):
            link_url = link['href']

            # Ensure the URL is absolute
            if not bool(urlparse(link_url).netloc):
                link_url = urljoin(url, link_url)

            # Add the URL to the queue if it's not already crawled
            if link_url not in self.pages_crawled:
                self.pages_to_crawl.put(link_url)

    def store_data(self, url, response):
        # Save page content to a file
        os.makedirs('data', exist_ok=True)
        with open(f'data/{urlparse(url).path.replace("/", "_")}.html', 'w') as f:
            f.write(response.text)

    def same_domain(self, url1, url2):
        return urlparse(url1).netloc == urlparse(url2).netloc
 
    def should_crawl(self, url):
        if "search.php" in url:
            print(f"Skipping disallowed URL: {url}")
            return False
        if url in self.pages_crawled:
            print(f'Already crawled "{url}"')
            return False
        if url.startswith("https://www.j-archive.com/") and not url.startswith("https://www.j-archive.com/showgame.php?game_id="):
            return False
        if url.startswith("http://"):
            print(f'Encountered unsecure URL, skipping: "{url}"')
            return False
        if not self.same_domain(self.base_url, url):
            return False
        return True    
 
    def crawl(self, url):
        #url = self.normalize_url(url)
        if not self.should_crawl(url):
            return
        #if not self.robot_parser.can_fetch('*', url):
            #logging.info(f"Blocked by robots.txt: {url}")
            #return
        if self.same_domain(self.base_url, url): 
            #logging.info(f'Adding "{url}" to the queue.')
            self.pages_to_crawl.put(url)

        soup = self.get_page_content(url)
        if soup is not None:
            self.extract_links(url, soup)

            # Log if URL contains is a game_id URL
            if "showgame" in url:
                print(f'Crawled desired URL: {url}')
                logging.info(f'Crawled desired URL: {url}')
            else:
                print(f'Crawled: {url}')
                logging.info(f'Crawled: {url}')
            
            # Mark the URL as crawled
            self.pages_crawled.add(url)
            
            #time.sleep(0.5) 

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
    start_time = time.time() # Start timer
    base_url = 'https://www.j-archive.com'
    crawler = Crawler(base_url)
    crawler.start_crawling()
    
    # Program execution time
    execution_time = (time.time() - start_time) / 60
    print((f"Program executed in {execution_time:.2f} minutes."))
    #logging.info(f"Program executed in {execution_time:.2f} minutes.")
    execution_time = execution_time / 60
    print((f"Program executed in {execution_time:.2f} hours."))
    #logging.info(f"Program executed in {execution_time:.2f} hours.")


if __name__ == "__main__":
    main()

