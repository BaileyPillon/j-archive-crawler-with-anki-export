# j-archive-crawler-with-anki-export
![image](https://github.com/BaileyPillon/j-archive-crawler-with-anki-export/assets/138253619/ddfb2aa9-f2dc-43d2-a1ff-7dc4327a4bbd)

Scrapes all game_id URLs within https://www.j-archive.com into a txt file then reads the txt file, scraping the game_ids within to category | clue | answer into a csv file to import into Anki. j-archive is a website that hosts an archive of all Jeopardy! gameshows since the 1980s to the present day.

Multithreaded Crawler initalizes a queue and a bloom filter. It also compares url to base url so it does not leave j-archive.com.

Download Anki here: https://apps.ankiweb.net/

Thorough explanation of spaced repetition and spaced repetition software (SRS) such as Anki here: https://gwern.net/spaced-repetition

Inspiration: Past Jeopardy! contestants Arthur Chu and Roger Craig.

An article by Mental Floss dated February 1st, 2014 (https://www.mentalfloss.com/article/54853/our-interview-jeopardy-champion-arthur-chu), about Arthur Chu, reads:

**On Flashcards & Becoming a "Jeopardy! Machine"**
Chu: As far as preparing for Jeopardy!, I did look up Roger Craig, who was a pretty famous Jeopardy! contestant (and a computer scientist), and who talked about how he developed an algorithm to scrape through the Jeopardy! Archive, which is entirely fan-made, and it's crazy that people put this much energy and intensity into it, archiving all the clues that have run, and then figuring out which categories are most likely to come up in the first round of Jeopardy, which ones come up in Double Jeopardy, which ones in Final Jeopardy. **I figured out what knowledge is the most valuable for Jeopardy!, and then matched that up to my own deficits in knowledge, and just hyper-focused on boning up on those specific areas of knowledge**. I don't know anything about computers and I'm probably way lazier than Roger Craig, so I didn't do it with his mathematical precision, but I did look up, okay, these things are always on Jeopardy! Of these things that are always on Jeopardy!, these are the easiest to remember. You know, it's not everything. There's a certain bias, there's a cultural bias to what they put in Jeopardy!. US Presidents are very important. State Nicknames, which are a thing that nobody has any practical reason to know, but they keep going back to that to generate clues.

# EXAMPLE - IBM Watson Episodes
Included is ibm_watson_episodes_scraper.py as an example. It scrapes the three games (three game IDs) associated with the IBM Watson episodes and exports category | clue | answer to a CSV file to then be imported into Anki. It takes about one minute to scrape these three episodes due to crawl-delay of j-archive.com.

# Clarification
scrape_cqa_to_csv.py includes category | clue | answer while scrape_cqa_values_to_csv.py includes category | clue | answer | value .

# j-archive.com/robots.txt
![image](https://github.com/BaileyPillon/j-archive-crawler-with-anki-export/assets/138253619/c53678b8-2f2b-455e-a3da-6f48215bbf0b)

# TO DO
Optimize the crawler more.

Respect robots.txt.

Count top 100 most appearing categories & count top 1,000 most appearing categories and put those in a txt file along with the count.

Handle daily doubles, final jeopardy, and media such as .mp4s and .jpgs.

List dependencies here.

Short pictorial Anki tutorial here.

Statistical analysis on wagering calculations, betting on daily doubles, final jeopardy, and overall gameplay strategy (including contestants over time who have broken the mold). In other words, the overall, the strategies that Jeopardy! constestants and champions have employed over time. 
