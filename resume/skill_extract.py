import pandas as pd


class SkillExtractor:
    """
    Extracts technical skills from the cleaned resume text
    using Dictionary Matching.
    """

    def __init__(self, skills_path: str = "data/skills.csv"):

        self.skills_df = pd.read_csv(skills_path)

        self.skills = (
            self.skills_df["skill"]
            .dropna()
            .str.lower()
            .unique()
            .tolist()
        )


    def extract_skills(self, text: str):

        text = text.lower()

        detected = []

        for skill in self.skills:

            if skill in text:

                detected.append(skill)

        detected = sorted(
            list(
                set(detected)
            )
        )

        return detected