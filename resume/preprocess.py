import nltk

nltk.download(
    "stopwords",
    quiet=True
)

nltk.download(
    "punkt",
    quiet=True
)


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stop_words = set(
    stopwords.words(
        "english"
    )
)


def preprocess_text(text):

    tokens = word_tokenize(
        text.lower()
    )

    cleaned = []

    for word in tokens:

        if (
            word.isalnum()
            and
            word not in stop_words
        ):

            cleaned.append(
                word
            )

    return " ".join(
        cleaned
    )