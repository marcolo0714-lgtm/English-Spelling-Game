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

word_col, KS_col, pos_col, def_col, alter_col = 0, 1, 2, 3, 4

def excel_2_json():
    # Load Excel file and convert it to a list of lists [vocab, ksid]
    allwords = pd.read_excel('word_folder/custom_wordlist.xlsx', "Words")
    word_list = allwords.values.tolist()

    # Make the word lowercase for sorting
    for word in word_list:
        word[word_col] = str(word[word_col]).lower()

    for word in word_list:
        ksid = word[KS_col]
        vocab = word[word_col].rstrip(" 1234")
        pos = word[pos_col]
        definition = word[def_col]
        alter = word[alter_col]

        fname = f"word_folder/KS{ksid}_words.json"
        word_data = {
                    "word": vocab,
                    "pos": f"{pos}",
                    "def": f"{definition}",
                    "alter": f"{alter}"
                }
        # Read the current json, append it, and write back
        with open(fname, "r") as f:
            word_list = json.load(f)
        word_list.append(word_data)
        with open(fname, "w") as f:
            json.dump(word_list, f, indent=4)


if __name__ == '__main__':
    # For first time initialization
    for ksid in range(1,5):
        fname = f"word_folder/KS{ksid}_words.json"
        with open(fname, "w") as f:
            json.dump([], f, indent=4)
        print(f"{fname} is cleared.")

    excel_2_json()
    print("/word_folder is updated.")
