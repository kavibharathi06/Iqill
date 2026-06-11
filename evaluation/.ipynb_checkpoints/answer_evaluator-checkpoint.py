from sklearn.metrics.pairwise import (
    cosine_similarity
)

from evaluation.train import (
    train_vectorizer
)


def evaluate_answer(
        expected,
        answer):

    if answer.strip() == "":

        return 0


    model = (
        train_vectorizer()
    )


    vectors = (

        model.fit_transform(

            [
                expected,

                answer

            ]

        )

    )


    similarity = (

        cosine_similarity(

            vectors[0],

            vectors[1]

        )[0][0]

    )


    score = (

        similarity
        *
        100

    )


    return round(
        score,
        2
    )