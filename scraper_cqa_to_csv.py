import csv
import time
import requests
from bs4 import BeautifulSoup
import os

def scrape_game(game_id):
    url = f"http://www.j-archive.com/showgame.php?game_id={game_id}"
    
    # Disallow scraping search.php
    if "search.php" in url:
        print(f"Skipping disallowed URL: {url}")
        return []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    round_categories = soup.select('.category_name')
    clues = soup.select('.clue')

    qa_pairs = []
    for i, clue in enumerate(clues):
        category = round_categories[i // 6].text
        question_element = clue.select_one('.clue_text')
        answer_element = clue.select_one('.correct_response')

        if question_element and answer_element:
            question = question_element.text
            answer = answer_element.text
            qa_pairs.append([category, question, answer])

    return qa_pairs

def write_to_csv(qa_pairs, filename):  
    file_exists = os.path.isfile(filename)

    if file_exists:
        file_name, file_extension = os.path.splitext(filename)
        return f"{file_name}{file_extension}"

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Clue", "Answer"])
        writer.writerows(qa_pairs)        

# Read URLs from a text file
game_ids = []
with open('j-archive_game_ids.txt', 'r') as file:
    for line in file:
        url = line.strip()
        if url.startswith("https://www.j-archive.com/showgame.php?game_id="):
            index = url.index("=") + 1
            game_id = url[index:]
            if game_id.isdigit():
                game_ids.append(int(game_id))

all_qa_pairs = []
for game_id in game_ids:
    print(f"Scraping game id: {game_id}")
    qa_pairs = scrape_game(game_id)
    all_qa_pairs.extend(qa_pairs)
   
    # Respect the Crawl-delay directive in robots.txt
    print("Waiting for 20 seconds before the next game...")
    time.sleep(20)
    
write_to_csv(all_qa_pairs, 'j-archive_to_anki.csv')
print("Done")
