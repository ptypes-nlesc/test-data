# This script is used to tokenize words in the title column

import string
import spacy
import pandas as pd

df = pd.read_csv("porn-with-dates-2022.csv")

# print 20 random titles
import random
random.choices(df.title, k=20)

# create a list of titles
titles = [_ for _ in df.title]

# download model
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# lets try to detect videos with 'blowjob' in the title
def has_blowjob(text):
    doc = nlp(text)
    for t in doc:
        if t.lower_ in ["blowjob", "blow job"]:
            if t.pos_!='VERB':
                return True
    return False
    

g = (title for title in titles if has_blowjob(title))
[next(g) for i in range(10)]

from spacy import displacy  
displacy.render(nlp("Angel Kisses Hot Cock | Gentle Blowjob and Mouth Full of Cum | Luxury Girl"))
spacy.explain("amod")





# TODO cleaning the data
def extract_words(text):
    """Extract words from a text and return them in a list."""s
    temp = text.split()  # Split the text on whitespace
    text_words = []

    for word in temp:
        # Remove any punctuation characters present in the beginning of the word
        while word[0] in string.punctuation:
            word = word[1:]

        # Remove any punctuation characters present in the end of the word
        while word[-1] in string.punctuation:
            word = word[:-1]

        # Append this word into our list of words.
        text_words.append(word.lower())

    return text_words


# apply to the whole title column
# df.title_words = df.title.apply(extract_words)
# TODO title[2] is breaking
title_words = extract_words(df.title[1])
print(title_words)

word_dict = {}
word_list = []
vocabulary_size = 0
title_tokens = []

for word in title_words:
    # If we are seeing this word for the first time, create an id for it and added it to our word dictionary
    if word not in word_dict:
        word_dict[word] = vocabulary_size
        word_list.append(word)
        vocabulary_size += 1

    # add the token corresponding to the current word to the tokenized text.
    title_tokens.append(word_dict[word])

print("Word list:", word_list, "\n\n Word dictionary:")

print(title_tokens)
