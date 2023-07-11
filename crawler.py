import requests, time, logging, posixpath, concurrent.futures, urllib.request, pickle, datetime
from bs4 import BeautifulSoup, ParserRejectedMarkup
from urllib.parse import urlunparse, urlencode, parse_qs, quote, unquote, urlparse, urljoin
from queue import Queue
from pybloom_live import BloomFilter
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()
first_iter = True

class Crawler():
    def __init__(self):
        self.base_url = "https://www.j-archive.com"
        self.desired_urls = "https://www.j-archive.com/showgame.php?game_id="
        self.pages_to_crawl = Queue()
        self.pages_to_crawl.put(self.base_url)
        self.pages_crawled = BloomFilter(capacity=10000000, error_rate=0.001)
        self.unsecure_url = "http://"
        self.request_interval = 1.0
        self.min_request_interval = 0.5
        self.max_request_interval = 5.0
        self.max_retries = 10
        

    # Persistance        
    def save_state(self):
       with open("pages_to_crawl.pkl", "wb") as file:
           pickle.dump(self.pages_to_crawl, file)
       with open("pages_crawled.pkl", "wb") as file:
           pickle.dump(self.pages_crawled, file)   
       return
   
    def adaptive_throttle(self, response):
        # Dict of status codes and multipliers
        status_code_ranges = {
            range(500, 600): 2.0,
            range(400, 500): 1.5,
        }
        # Use a lambda function for multiplier according to response status code
        multiplier = next((multiplier for status_range, multiplier in status_code_ranges.items() if response.status_code in status_range), 0.9)
        self.request_interval *= multiplier

        if response.elapsed.total_seconds() < 0.5:
            self.request_interval *= 0.9
        current_hour = datetime.datetime.now().hour
        if 9 <= current_hour < 17:
            self.request_interval *= 1.1
        elif 0 <= current_hour < 6:
            self.request_interval *= 0.9
        self.request_interval = max(self.min_request_interval, self.request_interval)
        self.request_interval = min(self.max_request_interval, self.request_interval)
            
    def normalize_url(self, url):
        scheme, netloc, path, params, query, fragment = urlparse(url)

        netloc = netloc.lower()  # Domain normalization
        path = posixpath.normpath(unquote(path.lower()))  # Path normalization, with case norm and percent-encoding norm

        # Query normalization (sort keys and percent-encoding norm)
        query_dict = parse_qs(query)
        normalized_query = urlencode(sorted((k, sorted(v)) for k, v in query_dict.items()), doseq=True)

        fragment = ''

        return urlunparse((scheme, netloc, path, params, normalized_query, fragment))

    def same_domain(self, url1, url2):
        return urlparse(url1).netloc == urlparse(url2).netloc

    def filter_url(self, url):
        return url.startswith(self.desired_urls)

    def crawl(self, url):
        first_iter = True
        while not crawler.pages_to_crawl.empty() or first_iter == True:        
            first_iter = False
            
            url = self.normalize_url(url)
            
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
                self.adaptive_throttle(response)
                if "text/html" in response.headers["content-type"]:
                    try:
                        soup = BeautifulSoup(response.text, 'html.parser')
                    except ParserRejectedMarkup:
                        logging.error(f'Failed to parse "{url}"')
                        return
                    #except bs4.FeatureNotFound:
                        #logging.error(f'Failed to find a parser library for "{url}"')
                        #return
                if self.filter_url(url):
                    self.pages_crawled.add(url)
                    print(f'Successfully crawled and wrote "{url}"')
                    logging.info(f'Crawled: {url}')
    
                # Enqueue same-domain URLs (ie, ensure crawler does not leave https://www.j-archive.com)
                for link in soup.find_all('a', href=True):
                    url = urljoin(url, link['href'])
                    if self.same_domain(self.base_url, url) or url not in self.pages_crawled and self.filter(url): 
                        if self.filter_url(url):
                            print(f'Successfully crawled and wrote "{url}".')
                            self.pages_to_crawl.put(url)
    
            except requests.exceptions.RequestException as e:
                logging.error(f'Failed to crawl "{url}": {str(e)}')
                time.sleep(3)
            
            finally:
                self.save_state()

if __name__ == "__main__":
    crawler = Crawler()
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
       while not crawler.pages_to_crawl.empty() or first_iter == True:
            url = crawler.pages_to_crawl.get()
            url = crawler.normalize_url(url)
            executor.submit(crawler.crawl, url)
           #try:
               #data = url.result()
           #except Exception as exc:
               #print('%r generated an exception: %s' % (url, exc))
           #else:
               #print('%r page is %d bytes' % (url, len(data)))
            # Program execution time
    if crawler.pages_to_crawl.empty():
        execution_time = (time.time() - start_time) / 60
        print((f"Program executed in {execution_time:.2f} minutes."))
        logging.info(f"Program executed in {execution_time:.2f} minutes.")
        execution_time = execution_time / 60
        (f"Program executed in {execution_time:.2f} hours.")
        logging.info(f"Program executed in {execution_time:.2f} hours.")
