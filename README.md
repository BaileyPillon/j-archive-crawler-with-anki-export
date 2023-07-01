# j-archive-crawler-with-anki-export
![image](https://github.com/BaileyPillon/j-archive-crawler-with-anki-export/assets/138253619/ddfb2aa9-f2dc-43d2-a1ff-7dc4327a4bbd)

Scrapes all game_id URLs within j-archive.com into a txt file then reads the txt file, scraping the game_ids within to category | clue | answer into a csv file to import into Anki.

Crawler initalizes a queue and a bloom filter. It also compares url to base url so it does not leave j-archive.com.

Included is ibm_watson_episodes_scraper.py as an example.

Download Anki here: https://apps.ankiweb.net/

Thorough explanation of spaced repetition software such as Anki here: https://gwern.net/spaced-repetition

Inspiration: Past Jeopardy! contestant Arthur Chu

# j-archive.com/robots.txt
![image](https://github.com/BaileyPillon/j-archive-crawler-with-anki-export/assets/138253619/c53678b8-2f2b-455e-a3da-6f48215bbf0b)

# TO DO
Optimize the crawler more.

Respect robots.txt.

Upload the game_ids scraper.

Count top 100 most appearing categories & count top 1,000 most appearing categories and put those in a txt file along with the count.

Handle daily doubles, final jeopardy, and media such as .mp4s and .jpgs.

List dependencies here.

Short pictorial Anki tutorial here.
