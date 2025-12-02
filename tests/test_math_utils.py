from app.core.math_utils import cosine_similarity


def test_cosine_similarity_identical():
    v = [1.0, 2.0, 3.0]
    assert round(cosine_similarity(v, v), 6) == 1.0


def test_cosine_similarity_orthogonal():
    v1 = [1.0, 0.0]
    v2 = [0.0, 1.0]
    assert abs(cosine_similarity(v1, v2)) < 1e-6
