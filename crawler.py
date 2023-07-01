import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from queue import Queue
from pybloom_live import BloomFilter
import concurrent.futures
import time

base_url = 'https://www.j-archive.com'

# URL parsing helper function
def same_domain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc

# Crawl function for each thread
def crawl():
    while not pages_to_crawl.empty():
        page_url = pages_to_crawl.get()
        
        if page_url in pages_crawled:
            print(f'Already crawled "{page_url}"')
            continue
        if page_url.startswith("https://www.j-archive.com/suggestcorrection.php?clue_id="):
            print(f'Skipping... "{page_url}"')
            continue
        if page_url.startswith("https://www.j-archive.com/showplayer.php?player_id="):
           print(f'Skipping... "{page_url}"')
           continue
        if page_url.startswith("https://www.j-archive.com/media/") or page_url.startswith("http://www.j-archive.com/media/"):
            print(f'Skipping... "{page_url}"')
            continue        
        if page_url.startswith("https://www.j-archive.com/wageringcalculator.php?"):
            print(f'Skipping... "{page_url}"')
            continue  
            
        try:
            response = requests.get(page_url)

            # Check if we got an HTML response
            if "text/html" in response.headers["content-type"]:
                soup = BeautifulSoup(response.text, 'html.parser')
                pages_crawled.add(page_url)
                print(page_url)
                
                # Write crawled game URLs to file
                if page_url.startswith("https://www.j-archive.com/showgame.php?game_id="):
                    with open("j-archive-game-ids.txt", "a") as file:
                        print(f'Successfully crawled and wrote "{page_url}" to the txt file.')
                        file.write(page_url + "\n")

                # Enqueue same-domain URLs
                for link in soup.find_all('a', href=True):
                    abs_url = urljoin(page_url, link['href'])
                    if same_domain(abs_url, base_url) and abs_url not in pages_crawled:
                        pages_to_crawl.put(abs_url)

        except Exception as e:
            print(f'Failed to crawl "{page_url}": {str(e)}')

# Initialize Queue and Bloom Filter
pages_to_crawl = Queue()
pages_to_crawl.put(base_url)
pages_crawled = BloomFilter(capacity=1000000, error_rate=0.01)

# Start time
start_time = time.time()

# Start crawling with multiple threads
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(crawl) for _ in range(10)]

# Program execution time
execution_time = time.time() - start_time
print(f"Program executed in {execution_time} seconds.")
execution_time = execution_time / 60
print(f"Program executed in {execution_time:.2f} minutes.")
execution_time = execution_time / 60
print(f"Program executed in {execution_time:.2f} hours.")
