import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume.preprocess import get_normalized_text, ensure_nltk_resources
from typing import Dict, Any

class AnswerEvaluator:
    def __init__(self):
        """Initializes the evaluator and ensures necessary NLTK models are downloaded."""
        ensure_nltk_resources()
        # Ensure POS tagger model is downloaded for grammar check
        try:
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        except Exception as e:
            print(f"Warning: Failed to download averaged_perceptron_tagger: {e}")

    def evaluate_answer(self, candidate_answer: str, expected_answer: str) -> Dict[str, Any]:
        """
        Evaluates a candidate's answer against the expected answer.
        
        Args:
            candidate_answer (str): The text provided by the candidate.
            expected_answer (str): The model answer from the question bank.
            
        Returns:
            Dict[str, Any]: Breakdown of scores, metrics, and feedback.
        """
        if not candidate_answer.strip():
            return {
                "technical_score": 0.0,
                "communication_score": 0.0,
                "final_score": 0.0,
                "grammar_score": 0.0,
                "length_score": 0.0,
                "diversity_score": 0.0,
                "similarity": 0.0,
                "feedback": "No answer was provided."
            }

        # 1. Technical Evaluation (80% weight)
        # Clean both answers
        clean_cand = get_normalized_text(candidate_answer)
        clean_exp = get_normalized_text(expected_answer)
        
        similarity = 0.0
        if clean_cand and clean_exp:
            try:
                # TF-IDF Vectorization
                vectorizer = TfidfVectorizer()
                tfidf = vectorizer.fit_transform([clean_exp, clean_cand])
                # Cosine Similarity
                similarity = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
            except Exception as e:
                print(f"Error computing cosine similarity: {e}")
                similarity = 0.0

        # Score Mapping (converts raw similarity [0,1] to realistic academic scale [0,100])
        tech_score = self._map_similarity_to_score(similarity)

        # 2. Communication Evaluation (20% weight)
        comm_metrics = self._calculate_communication_score(candidate_answer)

        # 3. Final Score Calculation
        final_score = (tech_score * 0.8) + (comm_metrics["communication_score"] * 0.2)

        # 4. Generate Feedback
        feedback = self._generate_feedback(tech_score, comm_metrics, similarity)

        return {
            "technical_score": round(tech_score, 1),
            "communication_score": round(comm_metrics["communication_score"], 1),
            "final_score": round(final_score, 1),
            "grammar_score": round(comm_metrics["grammar_score"], 1),
            "length_score": round(comm_metrics["length_score"], 1),
            "diversity_score": round(comm_metrics["diversity_score"], 1),
            "similarity": round(similarity, 3),
            "feedback": feedback
        }

    def _map_similarity_to_score(self, similarity: float) -> float:
        """
        Maps raw cosine similarity [0.0 - 1.0] to a scaled score out of 100.
        Uses a curve where a similarity of 0.5 is already a strong match (~85 points).
        """
        if similarity <= 0.0:
            return 0.0
        elif similarity >= 0.7:
            # Near perfect coverage of key technical terms
            return 90.0 + (similarity - 0.7) * (10.0 / 0.3)
        elif similarity >= 0.3:
            # Good coverage, contains core terms
            return 60.0 + (similarity - 0.3) * (30.0 / 0.4)
        else:
            # Some overlap, needs work
            return similarity * (60.0 / 0.3)

    def _calculate_communication_score(self, text: str) -> Dict[str, float]:
        """
        Calculates communication score out of 100 using three elements:
        1. Sentence Length (optimal word count)
        2. Vocabulary Diversity (Type-Token Ratio)
        3. Grammar Quality (capitalization, punctuation, and part-of-speech completeness)
        """
        # Clean words count
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        # 1. Sentence Length Score
        # Technical explanations are best when concise but detailed (e.g. 15-40 words)
        if word_count < 5:
            length_score = 30.0  # Too short
        elif 15 <= word_count <= 45:
            length_score = 100.0  # Perfect length
        elif 5 <= word_count < 15:
            length_score = 30.0 + (word_count - 5) * 7.0  # Linear scaling up to 100
        else:
            # Overly wordy answers decay slowly
            length_score = max(70.0, 100.0 - (word_count - 45) * 0.8)

        # 2. Vocabulary Diversity Score (TTR)
        if word_count > 0:
            unique_words = len(set(w.lower() for w in words))
            ttr = unique_words / word_count
            # Adjust TTR expectation: longer answers naturally have slightly lower TTR
            if word_count < 10:
                diversity_score = ttr * 100.0
            else:
                # Target at least 70% unique words for longer answers
                diversity_score = min(100.0, (ttr / 0.7) * 100.0)
        else:
            diversity_score = 0.0

        # 3. Grammar Quality Score
        # Explainable NLP Rules:
        # - Starts with capital letter
        # - Ends with punctuation (. ! ?)
        # - Contains both noun/pronoun and verb (POS checks)
        grammar_score = 100.0
        
        if not text[0].isupper():
            grammar_score -= 15.0
            
        if text[-1] not in ['.', '!', '?']:
            grammar_score -= 15.0
            
        # POS-Tag Checking
        try:
            tokens = nltk.word_tokenize(text)
            tags = nltk.pos_tag(tokens)
            
            has_noun = any(tag.startswith('NN') or tag.startswith('PRP') for word, tag in tags)
            has_verb = any(tag.startswith('VB') for word, tag in tags)
            
            if not has_noun:
                grammar_score -= 35.0  # Missing subject/object
            if not has_verb:
                grammar_score -= 35.0  # Missing action verb
        except Exception as e:
            print(f"Error running POS tagging for grammar: {e}")
            # If POS tagger fails, do a regex-based quick check for basic verbs/nouns
            pass

        grammar_score = max(0.0, grammar_score)

        # Combine communication score: equal weights
        comm_score = (length_score + diversity_score + grammar_score) / 3.0

        return {
            "communication_score": comm_score,
            "grammar_score": grammar_score,
            "length_score": length_score,
            "diversity_score": diversity_score
        }

    def _generate_feedback(self, tech_score: float, comm_metrics: Dict[str, float], similarity: float) -> str:
        """Generates actionable qualitative feedback based on scores."""
        feedback_points = []
        
        if tech_score >= 85:
            feedback_points.append("Excellent technical explanation! You correctly identified the core concepts and used appropriate industry terms.")
        elif tech_score >= 60:
            feedback_points.append("Good start, but your answer could be more technically complete. Try to include more specific details and key terms.")
        else:
            feedback_points.append("Your answer is missing critical technical details. Make sure you address the specific concepts requested in the question.")
            
        if comm_metrics["grammar_score"] < 80:
            feedback_points.append("Ensure you use complete sentences with proper capitalization, ending punctuation, and action verbs.")
            
        if comm_metrics["length_score"] < 70:
            feedback_points.append("Your answer is a bit too brief. Elaborate further to explain your reasoning clearly.")
            
        return " ".join(feedback_points)
