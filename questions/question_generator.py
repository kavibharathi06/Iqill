import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume.preprocess import get_normalized_text
from typing import List, Dict, Any
import random


class QuestionGenerator:

    def __init__(self, questions_csv_path: str = "data/questions.csv"):
        """
        Initializes Question Generator
        """

        self.questions_csv_path = questions_csv_path

        if os.path.exists(questions_csv_path):

            self.df_questions = pd.read_csv(
                questions_csv_path
            )

        else:

            self.df_questions = pd.DataFrame(
                columns=[
                    "skill",
                    "question",
                    "expected_answer",
                    "difficulty",
                    "domain",
                    "source",
                    "experience_level"
                ]
            )

            print(
                f"Warning: {questions_csv_path} not found."
            )

    def get_questions_for_skills(
        self,
        skills: List[str],
        resume_text: str = "",
        limit_per_skill: int = 3
    ) -> Dict[str, List[Dict[str, Any]]]:

        selected_questions = {}

        if self.df_questions.empty:
            return selected_questions

        normalized_resume = (
            get_normalized_text(resume_text)
            if resume_text
            else ""
        )

        for skill in skills:

            df_skill = self.df_questions[
                self.df_questions["skill"]
                .str.lower()
                ==
                skill.lower()
            ].copy()

            if df_skill.empty:
                continue

            # Resume-aware ranking
            if normalized_resume and len(df_skill) > 1:

                try:

                    corpus = [normalized_resume]

                    for _, row in df_skill.iterrows():

                        text = (
                            f"{row['question']} "
                            f"{row.get('domain','')} "
                            f"{row.get('difficulty','')}"
                        )

                        corpus.append(
                            get_normalized_text(
                                text
                            )
                        )

                    vectorizer = (
                        TfidfVectorizer()
                    )

                    matrix = (
                        vectorizer.fit_transform(
                            corpus
                        )
                    )

                    similarity = (
                        cosine_similarity(
                            matrix[0:1],
                            matrix[1:]
                        )[0]
                    )

                    df_skill[
                        "similarity"
                    ] = similarity

                    top_n = min(
                        max(
                            limit_per_skill * 3,
                            limit_per_skill
                        ),
                        len(df_skill)
                    )

                    df_skill = (
                        df_skill
                        .sort_values(
                            "similarity",
                            ascending=False
                        )
                        .head(top_n)
                    )

                except Exception as e:

                    print(
                        f"Ranking error: {e}"
                    )

            # Random selection
            if len(df_skill) > limit_per_skill:

                df_skill = (
                    df_skill.sample(
                        n=limit_per_skill
                    )
                )

            # Shuffle final order
            questions = (
                df_skill
                .sample(frac=1)
                .to_dict(
                    orient="records"
                )
            )

            selected_questions[
                skill
            ] = questions

        return selected_questions