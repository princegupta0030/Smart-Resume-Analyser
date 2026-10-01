from src.ml_ranker import calculate_precision_at_k

def test_pk():
    # Ground truth top 2 indices: 0 and 2
    llm = [0, 2, 1, 3]
    # Predicts top 2 indices: 0 and 1
    pred = [0, 1, 2, 3]

    # K=2
    # Ground truth set: {0, 2}
    # Pred set: {0, 1}
    # Intersection: {0} (len 1)
    # Precision@2 = 1 / 2 = 50.0

    assert calculate_precision_at_k(llm, pred, 2) == 50.0

def test_pk_perfect():
    llm = [0, 2, 1, 3]
    pred = [2, 0, 3, 1]

    # K=2
    # Ground truth set: {0, 2}
    # Pred set: {2, 0}
    # Intersection: {0, 2} (len 2)
    # Precision@2 = 2 / 2 = 100.0

    assert calculate_precision_at_k(llm, pred, 2) == 100.0
