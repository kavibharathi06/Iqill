import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stop_words = set(stopwords.words("english"))


def preprocess_text(text):

    text = text.lower()

    words = word_tokenize(text)

    filtered = []

    for word in words:

        if word.isalpha():

            if word not in stop_words:

                filtered.append(word)

    return " ".join(filtered)