import re
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def ensure_nltk_resources():
    """
    Download all required NLTK resources.
    Safe to call multiple times.
    """

    resources = [
        "punkt",
        "punkt_tab",
        "stopwords",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng"
    ]

    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except:
            pass


ensure_nltk_resources()

STOP_WORDS = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Used while extracting resume skills.

    Steps:
    1 Lowercase
    2 Tokenize
    3 Remove punctuation
    4 Remove stopwords
    5 Join again
    """

    tokens = word_tokenize(text.lower())

    cleaned = []

    for word in tokens:

        if word.isalnum() and word not in STOP_WORDS:

            cleaned.append(word)

    return " ".join(cleaned)


def get_normalized_text(text: str) -> str:
    """
    Normalization used by TF-IDF.

    This function is intentionally lightweight because
    TF-IDF performs better when most meaningful words
    are preserved.

    Used by:

    • Question Generator
    • Answer Evaluator
    """

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    tokens = word_tokenize(text)

    tokens = [

        word

        for word in tokens

        if word not in STOP_WORDS

        and len(word) > 1

    ]

    return " ".join(tokens)