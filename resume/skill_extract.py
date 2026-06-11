import pandas as pd


skills = pd.read_csv("data/skills.csv")


def extract_skills(text):

    text = text.lower()

    matched = []

    for skill in skills["skill"]:

        if skill in text:

            matched.append(skill)

    return matched