import pandas as pd
import requests
import json
import time
import logging

# Configure level, log format, and file destination
logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def excel_2_json(sheet_name, word_col, KS_col):
    # Load Excel file and convert it to a list of lists [vocab, ksid]
    allwords = pd.read_excel('wordlist_KS1-4.xlsx', sheet_name=sheet_name)
    word_list = allwords.values.tolist()

    # Make the word lowercase for sorting
    for word in word_list:
        word[word_col] = word[word_col].lower()

    # If the word contains hyphen or apostrophe, remove the word (they are not used in the game)
    word_list = [word for word in word_list if word[word_col].count('-') == 0 and word[word_col].count('\'') == 0]

    # Sort the list by word alphabetical order
    word_list.sort(key=lambda x: x[word_col])

    # Write the sorted list to files ('KSX_words.json') according to their KS level
    # For duplicate words, only keep the one with the lowest ksid (2nd column)
    previous_word = None
    failed_list = []

    pos_selector = "#id-sec-entry-group-dcom > div > div.box-posb-content > div.box-posb.box-posb-last > div > h2"
    def_selector = "#id-sec-entry-group-dcom > div > div.box-posb-content > div.box-posb.box-posb-last > ol > li:nth-child(1) > p"

    
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=10) 
        page = browser.new_page()

        for word in word_list:
            ksid = word[KS_col]
            vocab = word[word_col].rstrip(" 1234")
            if vocab != previous_word:  # Check for duplicates
                try:
                    fname = f"word_folder/KS{ksid}_words.json"
                    url = f"https://www.dictionary.com/browse/{word}"
                    page.goto(url)
                    
                    page.wait_for_selector(pos_selector, timeout=10000)
                    pos = page.locator(pos_selector).text_content(timeout=1000)
                    mean = page.locator(def_selector).text_content(timeout=1000)
                    mean = mean.strip(" \n()")
                    
                    word_data = {"word": word, "pos": pos, "def": mean}
                    logging.info(f"Returned: {word}, {pos}, {mean}")

                    with open(fname, "r") as f:
                        word_list = json.load(f) if json.load(f) == None else []
                        word_list.append(word_data)
                    with open(fname, "w") as f:
                        json.dump(word_list, f, indent=4)

                except:
                    with open(fname, "r") as f:
                        word_list = json.load(f) if json.load(f) == None else []
                        word_list.append({"word": vocab})
                    with open(fname, "w") as f:
                        json.dump(word_list, f, indent=4)
                    failed_list.append([vocab, ksid])
                    logging.info(f"Error: {word}")

            time.sleep(5)
            previous_word = vocab
    print(failed_list)


if __name__ == '__main__':
    for ksid in range(1,5):
        fname = f"word_folder/KS{ksid}_words.json"
        with open(fname, "w") as f:
            json.dump([], f, indent=4)
        print(f"{fname} is cleared.")
    excel_2_json("alpha", 0, 1)
    excel_2_json("alpharelated", 1, 2)
    print("/word_folder is updated.")
