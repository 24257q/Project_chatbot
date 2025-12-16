import numpy as np
from sentence_transformers import SentenceTransformer
from langdetect import detect, LangDetectException
from ..models import FQA

_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def detect_lang(text: str) -> str:
    """
    Detect language of user message.
    Returns 'ar' or 'fr'. Defaults to 'fr'.
    """
    try:
        return detect(text)
    except LangDetectException:
        return "fr"


def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def best_faq_match_semantic(message: str):
    q_vec = _model.encode(message, normalize_embeddings=True).tolist()
    best, best_score = None, 0.0

    for faq in FQA.objects.filter(is_active=True).exclude(embedding__isnull=True):
        score = cosine(q_vec, faq.embedding)
        if score > best_score:
            best, best_score = faq, score

    return best, best_score
