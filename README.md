# InterQill

InterQill is an AI-powered interview preparation platform that generates personalized technical interview questions from a candidate's resume and evaluates their answers using Natural Language Processing (NLP) techniques.

The system extracts technical skills from an uploaded resume, selects relevant interview questions from a curated dataset, evaluates candidate responses using TF-IDF and Cosine Similarity, analyzes communication quality, and generates detailed performance reports.

---

## Features

- Resume PDF parsing
- Automatic skill extraction
- Resume-based interview question generation
- TF-IDF based question ranking
- Randomized question selection
- Technical answer evaluation
- Communication quality assessment
- Grammar and vocabulary analysis
- Skill-wise performance report
- Overall interview score
- Personalized feedback

---

## Project Workflow

Resume Upload

↓

PDF Text Extraction

↓

Text Preprocessing

↓

Skill Extraction

↓

Question Generation

↓

Interview Session

↓

Answer Evaluation

↓

Performance Report

---

## Technologies Used

### Frontend

- Streamlit

### Programming Language

- Python

### NLP Techniques

- Tokenization
- Stopword Removal
- Text Normalization
- Dictionary-Based Skill Extraction
- TF-IDF Vectorization
- Cosine Similarity
- Part-of-Speech Tagging

### Libraries

- Streamlit
- pdfplumber
- pandas
- nltk
- scikit-learn
- matplotlib

---

## Project Structure

```
InterQill/
│
├── app.py
│
├── data/
│   ├── skills.csv
│   └── questions.csv
│
├── resume/
│   ├── extract_text.py
│   ├── preprocess.py
│   └── skill_extract.py
│
├── questions/
│   └── question_generator.py
│
├── evaluation/
│   └── answer_evaluator.py
│
├── requirements.txt
│
└── README.md
```

---

## Modules

### Resume Parser

Extracts text from uploaded PDF resumes using pdfplumber.

### Text Preprocessing

Performs:

- Lowercasing
- Tokenization
- Stopword Removal
- Text Normalization

### Skill Extraction

Identifies technical skills using dictionary matching against a predefined skills dataset.

### Question Generator

Generates interview questions by:

- Filtering questions based on detected skills
- Ranking questions using TF-IDF
- Computing Cosine Similarity with resume content
- Selecting relevant questions
- Randomizing final interview order

### Answer Evaluator

Evaluates candidate responses using:

- TF-IDF Vectorization
- Cosine Similarity
- Technical Score
- Communication Score
- Grammar Analysis
- Vocabulary Diversity
- Length Analysis
- Feedback Generation

---

## Algorithms and Techniques

### Resume Processing

- Dictionary Matching

### Question Generation

- TF-IDF Vectorization
- Cosine Similarity
- Random Sampling

### Answer Evaluation

- TF-IDF
- Cosine Similarity
- Rule-Based Communication Analysis
- Part-of-Speech Tagging

---

## Installation

Clone the repository

```bash
git clone https://github.com/kavibharathi06/Iqill.git
```

Navigate into the project

```bash
cd Iqill
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## Future Enhancements

- Adaptive difficulty-based questioning
- Semantic similarity using Sentence Transformers
- Speech-based interview mode
- LLM-powered answer evaluation
- Recruiter dashboard
- Interview history tracking
- Candidate progress analytics

---

## Author

Kavi Bharathi
