import pandas as pd


question_data = pd.read_csv(
    "data/questions.csv"
)


def generate_questions(skills):

    result = []

    for skill in skills:

        rows = question_data[
            question_data["skill"]
            ==
            skill
        ]

        if not rows.empty:

            result.extend(

                rows.to_dict(
                    "records"
                )

            )

    return result