import streamlit as st

from resume.extract_text import extract_resume_text
from resume.preprocess import preprocess_text
from resume.skill_extract import SkillExtractor

from questions.question_generator import QuestionGenerator
from evaluation.answer_evaluator import AnswerEvaluator


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="InterQill",
    page_icon="💼",
    layout="wide"
)


st.title("💼 InterQill")
st.subheader("AI Resume Based Interview Evaluation System")


# -------------------------------------------------
# Initialize Components
# -------------------------------------------------

skill_extractor = SkillExtractor()

question_generator = QuestionGenerator()

answer_evaluator = AnswerEvaluator()


# -------------------------------------------------
# Session State
# -------------------------------------------------

if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "show_next" not in st.session_state:
    st.session_state.show_next = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "all_scores" not in st.session_state:
    st.session_state.all_scores = []

if "skill_scores" not in st.session_state:
    st.session_state.skill_scores = {}

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "detected_skills" not in st.session_state:
    st.session_state.detected_skills = []


# -------------------------------------------------
# Upload Resume
# -------------------------------------------------

uploaded = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


if uploaded:

    # ---------------------------------------------
    # Resume Parsing
    # ---------------------------------------------

    if len(st.session_state.generated_questions) == 0:

        resume_text = extract_resume_text(uploaded)

        st.session_state.resume_text = resume_text

        cleaned_text = preprocess_text(
            resume_text
        )

        skills = skill_extractor.extract_skills(
            cleaned_text
        )

        st.session_state.detected_skills = skills


        # -----------------------------------------
        # Generate Questions
        # -----------------------------------------

        grouped_questions = question_generator.get_questions_for_skills(

            skills=skills,

            resume_text=resume_text,

            limit_per_skill=2

        )


        generated = []

        for skill in skills:

            if skill in grouped_questions:

                generated.extend(
                    grouped_questions[skill]
                )


        st.session_state.generated_questions = generated


    generated = st.session_state.generated_questions

    skills = st.session_state.detected_skills


    # ---------------------------------------------
    # Display Skills
    # ---------------------------------------------

    st.subheader("Detected Skills")

    if skills:

        cols = st.columns(4)

        for i, skill in enumerate(skills):

            cols[i % 4].success(skill.title())

    else:

        st.warning(
            "No skills detected from resume."
        )


    # ---------------------------------------------
    # Continue only if questions exist
    # ---------------------------------------------

    if len(generated) == 0:

        st.error(
            "No interview questions found."
        )

        st.stop()


    # ---------------------------------------------
    # Active Question
    # ---------------------------------------------

    if st.session_state.index < len(generated):

        current = generated[
            st.session_state.index
        ]

        skill = current["skill"]

        st.divider()

        st.subheader(
            f"Question {st.session_state.index+1} / {len(generated)}"
        )

        st.caption(
            f"Skill : {skill}"
        )

        st.write(
            current["question"]
        )

        answer = st.text_area(

            "Your Answer",

            height=180,

            key=f"answer_{st.session_state.index}"

        )
            # ---------------------------------------------
        # Submit Answer
        # ---------------------------------------------

        if not st.session_state.show_next:

            if st.button("Submit Answer"):

                if not answer.strip():

                    st.warning(
                        "Please enter your answer before submitting."
                    )

                else:

                    result = answer_evaluator.evaluate_answer(

                        candidate_answer=answer,

                        expected_answer=current[
                            "expected_answer"
                        ]

                    )

                    st.session_state.last_result = result

                    st.session_state.all_scores.append(

                        result["final_score"]

                    )

                    if skill not in st.session_state.skill_scores:

                        st.session_state.skill_scores[
                            skill
                        ] = []

                    st.session_state.skill_scores[
                        skill
                    ].append(

                        result["final_score"]

                    )

                    st.session_state.show_next = True

                    st.rerun()


        # ---------------------------------------------
        # Display Evaluation
        # ---------------------------------------------

        if (

            st.session_state.show_next

            and

            st.session_state.last_result

        ):

            r = st.session_state.last_result

            st.divider()

            st.subheader("Evaluation Report")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "Technical Score",

                    f"{r['technical_score']}%"

                )

            with col2:

                st.metric(

                    "Communication",

                    f"{r['communication_score']}%"

                )

            with col3:

                st.metric(

                    "Final Score",

                    f"{r['final_score']}%"

                )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Grammar",

                    f"{r['grammar_score']}%"

                )

                st.metric(

                    "Vocabulary",

                    f"{r['diversity_score']}%"

                )

            with col2:

                st.metric(

                    "Length",

                    f"{r['length_score']}%"

                )

                st.metric(

                    "Similarity",

                    r["similarity"]

                )

            st.divider()

            st.subheader("Reference Answer")

            st.info(

                current["expected_answer"]

            )

            st.subheader("AI Feedback")

            st.success(

                r["feedback"]

            )

            if st.button("Next Question"):

                answer_key = f"answer_{st.session_state.index}"

                if answer_key in st.session_state:

                    del st.session_state[
                        answer_key
                    ]

                st.session_state.index += 1

                st.session_state.show_next = False

                st.session_state.last_result = None

                st.rerun()
            # ----------------------------------------------------
    # Interview Completed
    # ----------------------------------------------------

    else:

        st.balloons()

        st.success(
            "🎉 Interview Completed Successfully!"
        )

        overall_score = round(

            sum(
                st.session_state.all_scores
            )

            /

            len(
                st.session_state.all_scores
            ),

            2

        )

        st.header(
            "📊 Final Interview Report"
        )

        st.metric(
            "Overall Score",
            f"{overall_score}%"
        )

        st.divider()

        st.subheader(
            "📌 Skill-wise Performance"
        )

        for skill, scores in (

            st.session_state
            .skill_scores
            .items()

        ):

            avg = round(

                sum(scores)

                /

                len(scores),

                2

            )

            st.write(
                f"**{skill.title()} : {avg}%**"
            )

        st.divider()

        st.subheader(
            "📝 Overall Performance"
        )

        if overall_score >= 85:

            st.success(
                """
Excellent Performance!

You demonstrated strong technical knowledge,
good communication skills,
and a solid understanding
of the interview topics.
                """
            )

        elif overall_score >= 70:

            st.info(
                """
Good Performance!

You understand most concepts,
but you can improve
technical depth
and explanation quality.
                """
            )

        elif overall_score >= 50:

            st.warning(
                """
Average Performance.

Revise the fundamental concepts
and practice answering
using more technical keywords.
                """
            )

        else:

            st.error(
                """
Needs Improvement.

Focus on understanding
the core concepts,
practice interview questions,
and improve communication.
                """
            )

        st.divider()

        st.subheader(
            "📚 Recommended Skills to Improve"
        )

        weak_skills = []

        for skill, scores in (

            st.session_state
            .skill_scores
            .items()

        ):

            avg = sum(scores) / len(scores)

            if avg < 70:

                weak_skills.append(
                    (skill, avg)
                )

        if weak_skills:

            weak_skills.sort(
                key=lambda x: x[1]
            )

            for skill, score in weak_skills:

                st.write(

                    f"🔸 {skill.title()} ({round(score,1)}%)"

                )

        else:

            st.success(
                "Excellent! No weak skills detected."
            )

        st.divider()

        if st.button(
            "🔄 Restart Interview"
        ):

            st.session_state.clear()

            st.rerun()