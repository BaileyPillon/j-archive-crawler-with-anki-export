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
        category = round_categories[i//6].text
        question = clue.select_one('.clue_text').text
        answer = clue.select_one('.correct_response').text

        # Anki importable format: Category | Question | Answer
        qa_pairs.append([category, question, answer])

    return qa_pairs

def generate_true_random_number():
    response = requests.get('https://www.random.org/integers/?num=1&min=0&max=999999999&col=1&base=10&format=plain&rnd=new')
    number = int(response.text.strip())
    return number

random_number = generate_true_random_number()
print(random_number)


def write_to_csv(qa_pairs, filename):
    file_exists = os.path.isfile(filename)

    if file_exists:
        # Append a true random number to the filename to ensure uniqueness
        random_number = generate_true_random_number()
        file_name, file_extension = os.path.splitext(filename)
        return f"{file_name}_{random_number}{file_extension}"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Question", "Answer"])
        writer.writerows(qa_pairs)

# Specify your list of game IDs here
game_ids = [3575, 3576, 3577]

all_qa_pairs = []

for game_id in game_ids:
    print(f"Scraping game id: {game_id}")
    qa_pairs = scrape_game(game_id)
    all_qa_pairs.extend(qa_pairs)

    # Respect the Crawl-delay directive in robots.txt
    print("Waiting for 20 seconds before the next game...")
    time.sleep(20)

write_to_csv(all_qa_pairs, 'jeopardy_ibm_watson_episodes.csv')
print("Done")
