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
    previous_word = ""
    failed_list = []

    # word is a list (row) from the excel
    for word in word_list:
        ksid = word[KS_col]
        vocab = word[word_col].rstrip(" 1234")

        if vocab != previous_word:  # Check for duplicates
            try:
                fname = f"word_folder2 (API)/KS{ksid}_words.json"
                url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{vocab}"

                # Get pos and definition of a vocab
                response = requests.get(url)

                data = response.json()[0]
                meanings = data.get('meanings', [])
                pos = meanings[0].get('partOfSpeech', '')
                definitions = meanings[0].get('definitions', [])
                definition = definitions[0].get('definition', '')
                
                logging.info(f"Word searched: {vocab}, {pos}, {definition}")
                word_data = {
                    "word": vocab,
                    "pos": f"{pos}",
                    "def": f"{definition}"
                }
                
            except:  # The word is not searched
                word_data = {"word": vocab}
                failed_list.append([vocab, ksid])
                logging.info(f"Error: {vocab}")

            # Read the current json, append it, and write back
            with open(fname, "r") as f:
                word_list = json.load(f)
            word_list.append(word_data)
            with open(fname, "w") as f:
                json.dump(word_list, f, indent=4)

        time.sleep(3)  # Avoid spamming API calls
        previous_word = vocab   # Used to remove duplicates

    print(failed_list)


if __name__ == '__main__':
    # # For first time initialization
    # for ksid in range(1,5):
    #     fname = f"word_folder2 (API)/KS{ksid}_words.json"
    #     with open(fname, "w") as f:
    #         json.dump([], f, indent=4)
    #     print(f"{fname} is cleared.")

    excel_2_json("alpha", 0, 1)
    excel_2_json("alpharelated", 1, 2)
    print("/word_folder2 (API) is updated.")
