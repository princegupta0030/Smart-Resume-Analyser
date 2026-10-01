import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_embedding_model():
    """Load the model once and cache it in Streamlit memory."""
    return SentenceTransformer('all-MiniLM-L6-v2')

def calculate_tfidf_similarity(jd: str, resume_texts: list[str]) -> list[float]:
    """
    Computes TF-IDF cosine similarity between a single Job Description and a list of resumes.
    Returns a list of similarity scores scaled 0-100.
    """
    if not resume_texts:
        return []

    vectorizer = TfidfVectorizer(stop_words='english')
    documents = [jd] + resume_texts
    tfidf_matrix = vectorizer.fit_transform(documents)

    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(jd_vector, resume_vectors)[0]
    return [int(round(sim * 100)) for sim in similarities]

def calculate_embedding_similarity(jd: str, resume_texts: list[str]) -> list[float]:
    """
    Computes semantic similarity using Sentence Transformers.
    Returns a list of similarity scores scaled 0-100.
    """
    if not resume_texts:
        return []

    model = load_embedding_model()
    jd_embedding = model.encode([jd])
    resume_embeddings = model.encode(resume_texts)

    similarities = cosine_similarity(jd_embedding, resume_embeddings)[0]
    return [int(round(max(0, sim) * 100)) for sim in similarities]

def calculate_precision_at_k(actual_ranks: list[int], predicted_ranks: list[int], k: int) -> float:
    """
    Calculates Precision@K.
    Actual ranks (ground truth) = the top K indices from the LLM.
    Predicted ranks = the top K indices from the TF-IDF or Embedding model.
    """
    if not actual_ranks or not predicted_ranks or k <= 0:
        return 0.0

    actual_top_k = set(actual_ranks[:k])
    predicted_top_k = set(predicted_ranks[:k])

    if not actual_top_k:
        return 0.0

    # Intersection of true top K and predicted top K
    relevant_retrieved = len(actual_top_k.intersection(predicted_top_k))
    return (relevant_retrieved / k) * 100
