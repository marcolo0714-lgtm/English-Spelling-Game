import pandas as pd

# Load Excel file 1 and convert it to a list of lists [vocab, ksid]
allwords = pd.read_excel('wordlist_KS1-4.xlsx', sheet_name='alpha')
word_list = allwords.values.tolist()

# Make the word lowercase for sorting
for word in word_list:
    word[0] = word[0].lower()

# If the word contains hyphen, remove the word (they are not used in the game)
word_list = [word for word in word_list if '-' not in word[0]]

# Sort the list by word (1st column)
word_list.sort(key=lambda x: x[0])

# Write the sorted list to text files ('KSX_words.txt') according to their ksid (2nd column)
# For duplicate words, only keep the one with the lowest ksid (2nd column)
previous_word = None
for word in word_list:
    ksid = word[1]
    vocab = word[0].rstrip(" 1234")
    if vocab != previous_word:  # Check for duplicates
        with open(f'word_folder/KS{ksid}_words.txt', 'a') as f:
            f.write(vocab + '\n')
        previous_word = vocab

############################################################################
# Load Excel file 2 and convert it to a list of lists [vocab, related, ksid]
allwords = pd.read_excel('wordlist_KS1-4.xlsx', sheet_name='alpharelated')
word_list = allwords.values.tolist()

# Make the word lowercase for sorting
for word in word_list:
    word[1] = word[1].lower()

# If the word contains hyphen, remove the word (they are not used in the game)
word_list = [word for word in word_list if '-' not in word[1]]

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