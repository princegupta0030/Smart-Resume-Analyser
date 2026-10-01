from src.ml_ranker import calculate_tfidf_similarity, calculate_embedding_similarity

def test_tfidf_similarity():
    jd = "Looking for a Python developer with Django experience."
    resumes = [
        "I am a Python developer with 5 years of Django experience.",
        "I am a Java developer with Spring Boot experience.",
    ]

    scores = calculate_tfidf_similarity(jd, resumes)
    assert len(scores) == 2
    assert scores[0] > scores[1]  # Python resume should score higher

def test_embedding_similarity():
    jd = "Software Engineer experienced in backend development."
    resumes = [
        "Backend developer skilled in building APIs and server logic.",
        "Frontend developer creating UI components with React.",
    ]

    scores = calculate_embedding_similarity(jd, resumes)
    assert len(scores) == 2
    assert scores[0] > scores[1]  # Backend resume should score higher semantically
