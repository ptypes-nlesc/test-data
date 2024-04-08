# Description: This script will take the data from the csv file and tokenize the data
import string

import pandas as pd

df = pd.read_csv("porn-with-dates-2022.csv")


# TODO gives error on df.title[2]
def extract_words(text):
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
word_dict


print(title_tokens)
