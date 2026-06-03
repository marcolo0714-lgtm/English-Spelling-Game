from nltk.corpus import wordnet
# pip install nltk
# python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

def get_offline_word_data(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return None
        
    # Grab the most common meaning (the first synset)
    primary_synset = synsets[0]
    
    definition = primary_synset.definition()
    examples = primary_synset.examples()
    sentence = examples[0] if examples else "No example found."
    
    return {
        "word": word,
        "hint": definition,
        "sentence": sentence
    }

print(get_offline_word_data("beautiful"))