# j-archive-crawler-with-anki-export
Scrapes all game_id URLs within j-archive.com into a txt file then reads the txt file, scraping category | clue | answer into a csv file to import into anki.

Crawler initalizes a queue and a bloom filter. It also compares url to base url so it does not leave j-archive.com.

Included is ibm_watson_episodes_scraper.py as an example.

Download Anki here: https://apps.ankiweb.net/

# j-archive.com/robots.txt
user-agent: *

Crawl-delay: 20


User-Agent: bingbot

Crawl-delay: 20

Disallow: /search.php

# TO DO
Optimize the crawler more.

Respect robots.txt.

Upload the game_ids scraper.

Count top 100 most appearing categories & count top 1,000 most appearing categories and put those in a txt file along with the count.

Handle daily doubles, final jeopardy, and media such as .mp4s and .jpgs.

List dependencies here.

Short pictorial Anki tutorial here.
