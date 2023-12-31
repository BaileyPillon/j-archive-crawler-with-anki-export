# j-archive crawler with Anki export
![image](https://github.com/BaileyPillon/j-archive-crawler-with-anki-export/assets/138253619/ddfb2aa9-f2dc-43d2-a1ff-7dc4327a4bbd)

NOTE: Please ethically crawl j-archive by respecting robots.txt. Too many numerous requests will get you temporarily blocked or potentially IP banned.

Scrapes all game_id URLs within https://www.j-archive.com into a txt file then reads the txt file, scraping the game_ids within to category | clue | answer into a csv file to import into Anki. j-archive is a website that hosts an archive of all Jeopardy! gameshows since the 1980s to the present day. Crawler only considers https://www.j-archive.com and not http://www.j-archive.com .

Multithreaded Crawler initalizes a queue and a bloom filter. It also compares abs_url to base_url so it does not leave j-archive.com.

Download Anki here: https://apps.ankiweb.net/ . For Anki, you will need your cards need to be match the number of fields to the csv file in order for it to import and display properly (if it somehow does import).

Thorough explanation of spaced repetition and spaced repetition software (SRS) such as Anki here: https://gwern.net/spaced-repetition

Inspiration: Past Jeopardy! contestants Arthur Chu and Roger Craig.

An article by Mental Floss dated February 1st, 2014 (https://www.mentalfloss.com/article/54853/our-interview-jeopardy-champion-arthur-chu), about Arthur Chu, reads:

**On Flashcards & Becoming a "Jeopardy! Machine"**
Chu: As far as preparing for Jeopardy!, I did look up Roger Craig, who was a pretty famous Jeopardy! contestant (and a computer scientist), and who talked about how he developed an algorithm to scrape through the Jeopardy! Archive, which is entirely fan-made, and it's crazy that people put this much energy and intensity into it, archiving all the clues that have run, and then figuring out which categories are most likely to come up in the first round of Jeopardy, which ones come up in Double Jeopardy, which ones in Final Jeopardy. **I figured out what knowledge is the most valuable for Jeopardy!, and then matched that up to my own deficits in knowledge, and just hyper-focused on boning up on those specific areas of knowledge**. I don't know anything about computers and I'm probably way lazier than Roger Craig, so I didn't do it with his mathematical precision, but I did look up, okay, these things are always on Jeopardy! Of these things that are always on Jeopardy!, these are the easiest to remember. You know, it's not everything. There's a certain bias, there's a cultural bias to what they put in Jeopardy!. US Presidents are very important. State Nicknames, which are a thing that nobody has any practical reason to know, but they keep going back to that to generate clues.

# Features 
Placeholder

# In Memoriam to Alex Trebek
![trebek_last_episode](https://github.com/BaileyPillon/j-archive-crawler-with-anki-export/assets/138253619/451b22d1-87de-4dc7-a11c-fb6af64bc132)

# EXAMPLE - IBM Watson Episodes
Included is ibm_watson_episodes_scraper.py as an example. It scrapes the three games (three game IDs) associated with the IBM Watson episodes and exports category | clue | answer to a CSV file to then be imported into Anki. It takes about one minute to scrape these three episodes due to crawl-delay of j-archive.com.

# Clarification
scrape_cqa_to_csv.py includes category | clue | answer while scrape_cqa_values_to_csv.py includes category | clue | answer | value .

# j-archive.com/robots.txt
![image](https://github.com/BaileyPillon/j-archive-crawler-with-anki-export/assets/138253619/c53678b8-2f2b-455e-a3da-6f48215bbf0b)

# Wagering Strategies
Some wagering strategies in Jeopardy! include: Expected value, DDs, Final Jeopardy Wagering, Risk Management, Probabilities, which are the more basic ones. Less obvious is: Game Theory, Binomial Distribution in terms of self-evaluating your own accuracy across categories, Kelly Criterion, Bayesian Updating, Mone Carlo Simulations, Regression Analysis, and more. Past that, it is moreso analyzing the game itself as it too difficult if not impossible to analyze beyond that level in real time while having to react to the buzzer with speed and also wracking your brain for the answer to the clue.

# TO DO
Optimize the crawler more.

Respect robots.txt.

Count top 100 most appearing categories & count top 1,000 most appearing categories and put those in a txt file along with the count.

Handle daily doubles, final jeopardy, and media such as .mp4s and .jpgs.

List dependencies here.

Short pictorial Anki tutorial here.

Statistical analysis on wagering calculations, betting on daily doubles, final jeopardy, tie-breakers, and overall gameplay strategy (including contestants over time who have broken the mold). In other words, the overall, the strategies that Jeopardy! constestants and champions have employed over time. 

Improve parallelization to crawler.

Fix redundancy and improve object oriented crawler py file.
