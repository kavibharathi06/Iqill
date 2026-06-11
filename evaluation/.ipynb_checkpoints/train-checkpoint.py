from sklearn.feature_extraction.text import (
    TfidfVectorizer
)


def train_vectorizer():

    model = (
        TfidfVectorizer()
    )

    return model