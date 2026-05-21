import pandas as pd

# Load the Excel file and convert it to a list of lists [id, vocab, ksid, posid]
allwords = pd.read_excel('wordlist_KS1-4.xlsx', sheet_name='wordlist')
word_list = allwords.values.tolist()

# Remove all words containing hyphens (they are prefixes/suffixes)
word_list = [word for word in word_list if '-' not in word[1]]

# Make the word lowercase for sorting
for word in word_list:
    word[1] = word[1].lower()

# Sort the list by word (2nd column)
word_list.sort(key=lambda x: x[1])

# Write the sorted list to text files ('KSX_words.txt') according to their ksid (3rd column)
# For duplicate words, only keep the one with the lowest ksid (3rd column)
previous_word = None
for word in word_list:
    ksid = word[2]
    vocab = word[1].rstrip(" 1234")
    if vocab != previous_word:  # Check for duplicates
        with open(f'word_folder/KS{ksid}_words.txt', 'a') as f:
            f.write(vocab + '\n')
        previous_word = vocab