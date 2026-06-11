import streamlit as st

from resume.extract_text import extract_resume_text
from resume.preprocess import preprocess_text
from resume.skill_extract import extract_skills
from questions.question_generator import generate_questions
from evaluation.answer_evaluator import evaluate_answer


st.title("InterQill")
st.title("Interview Question Generator And Evaluation System")


uploaded = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)


if uploaded:

    text = extract_resume_text(uploaded)

    cleaned = preprocess_text(text)

    skills = extract_skills(cleaned)

    generated = generate_questions(skills)

    st.subheader(
       "Skills Identified"
    )

    for skill in skills:

        st.markdown(
           f"• {skill.title()}"
        )

    if "index" not in st.session_state:
        st.session_state.index = 0

    if "all_scores" not in st.session_state:
        st.session_state.all_scores = []

    if "skill_scores" not in st.session_state:
        st.session_state.skill_scores = {}

    if "show_next" not in st.session_state:
        st.session_state.show_next = False

    if "last_result" not in st.session_state:
        st.session_state.last_result = None


    if st.session_state.index < len(generated):

        current = generated[
            st.session_state.index
        ]

        skill = current["skill"]

        st.subheader(
            f"Skill: {skill}"
        )

        st.write(
            current["question"]
        )


        answer = st.text_area(
            "Answer",
            key=f"answer_{st.session_state.index}"
        )


        if (
            not
            st.session_state.show_next
        ):

            if st.button(
                "Submit"
            ):

                if answer.strip():

                    technical = evaluate_answer(
                        current[
                            "expected_answer"
                        ],
                        answer
                    )

                    communication = min(
                        len(
                            answer.split()
                        )
                        * 4,
                        100
                    )

                    final = round(
                        (
                            technical
                            +
                            communication
                        )
                        /
                        2,
                        2
                    )

                    st.session_state.last_result = {

                        "technical":
                        technical,

                        "communication":
                        communication,

                        "final":
                        final,

                        "skill":
                        skill

                    }

                    st.session_state.all_scores.append(
                        final
                    )


                    if (
                        skill
                        not in
                        st.session_state.skill_scores
                    ):

                        st.session_state.skill_scores[
                            skill
                        ] = []


                    st.session_state.skill_scores[
                        skill
                    ].append(
                        final
                    )


                    st.session_state.show_next = True

                    st.rerun()


        if (

            st.session_state.show_next

            and

            st.session_state.last_result

        ):

            r = (
                st.session_state
                .last_result
            )

            st.success(
f"""
Technical Score:
{r['technical']}

Communication Score:
{r['communication']}

Question Score:
{r['final']}
"""
            )


            if st.button(
                "Next Question"
            ):

                old_key = (
                    f"answer_{st.session_state.index}"
                )


                if (
                    old_key
                    in
                    st.session_state
                ):

                    del st.session_state[
                        old_key
                    ]


                st.session_state.index += 1


                st.session_state.show_next = False


                st.session_state.last_result = None


                st.rerun()


    else:

        st.success(
            "Interview Completed"
        )


        final = round(

            sum(
                st.session_state
                .all_scores
            )

            /

            len(
                st.session_state
                .all_scores
            ),

            2

        )


        st.subheader(
            "Overall Score"
        )

        st.write(
            final
        )


        st.subheader(
            "Skill Wise Result"
        )


        for k, v in (

            st.session_state
            .skill_scores
            .items()

        ):

            st.write(

                k,

                round(

                    sum(v)

                    /

                    len(v),

                    2

                )

            )


        if st.button(
            "Restart"
        ):

            st.session_state.clear()

            st.rerun()

