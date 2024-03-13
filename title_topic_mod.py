# adapted from https://ourcodingclub.github.io/tutorials/topic-modelling-python/
import re

import nltk
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# from sklearn.decomposition import NMF

df = pd.read_csv("porn-with-dates-2022.csv")

# count number of words in title per video
df.title.astype(str).apply(len).hist()
df.title.astype(str).apply(len).describe()

df.title.astype(str)[0].split(" ")[0]

# nltk.download("stopwords")

my_stopwords = nltk.corpus.stopwords.words("english")
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
my_punctuation = "!\"$%&'()*+,-./:;<=>?[\\]^_`{|}~•@"


def clean_title(t, bigrams=False):
    t = t.lower()  # lower case
    t = re.sub("[" + my_punctuation + "]+", " ", t)  # strip punctuation
    t = re.sub("\s+", " ", t)  # remove double spacing
    t = re.sub("([0-9]+)", "", t)  # remove numbers
    t_token_list = [
        word for word in t.split(" ") if word not in my_stopwords
    ]  # remove stopwords
    t_token_list = [
        word_rooter(word) if "#" not in word else word for word in t_token_list
    ]  # apply word rooter
    if bigrams:
        t_token_list = t_token_list + [
            t_token_list[i] + "_" + t_token_list[i + 1]
            for i in range(len(t_token_list) - 1)
        ]
    t = " ".join(t_token_list)
    return t


df["clean_title"] = df.title.apply(clean_title)

# the vectorizer object will be used to transform text to vector form
# discarding words that appear in more than 90% of the titles
# discarding words that appear in less than 25 titles
# TODO tweaks numbers

vectorizer = CountVectorizer(max_df=0.9, min_df=25, token_pattern="\w+|\$[\d\.]+|\S+")

title_freq = vectorizer.fit_transform(df["clean_title"]).toarray()
title_freq_features = vectorizer.get_feature_names_out()

title_freq.shape
title_freq_features

from sklearn.decomposition import LatentDirichletAllocation

number_of_topics = 10

model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)
model.fit(title_freq)


def display_topics(model, feature_names, no_top_words):
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict["Topic %d words" % (topic_idx)] = [
            "{}".format(feature_names[i])
            for i in topic.argsort()[: -no_top_words - 1 : -1]
        ]
        topic_dict["Topic %d weights" % (topic_idx)] = [
            "{:.1f}".format(topic[i]) for i in topic.argsort()[: -no_top_words - 1 : -1]
        ]
    return pd.DataFrame(topic_dict)


no_top_words = 10
display_topics(model, title_freq_features, no_top_words)
