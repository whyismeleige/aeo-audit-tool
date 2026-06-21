import numpy
from sentence_transformers import SentenceTransformer

from app.core.chunker import TextChunk

PASSAGE_PREFIX = ""
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

_model = None


def _get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    return _model


def embed(chunks: list[TextChunk]) -> list[tuple[TextChunk, numpy.ndarray]]:
    model = _get_model()

    texts_to_encode = [
        f"{PASSAGE_PREFIX}{chunk.heading}\n{chunk.content}" for chunk in chunks
    ]

    embeddings = model.encode(
        texts_to_encode,
        batch_size=32,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return list(zip(chunks, embeddings))
