from dataclasses import dataclass

import numpy
from sentence_transformers import SentenceTransformer

from app.core.chunker import TextChunk
from app.config import get_settings

PASSAGE_PREFIX = ""
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

settings = get_settings()

@dataclass
class ChunkEmbedding:
    heading_embedding: numpy.ndarray
    content_embedding: numpy.ndarray


_model = None


def _get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)

    return _model


def embed(chunks: list[TextChunk]) -> list[tuple[TextChunk, ChunkEmbedding]]:
    model = _get_model()

    heading_texts_to_encode = [chunk.heading for chunk in chunks]

    content_texts_to_encode = [chunk.content for chunk in chunks]

    heading_embeddings = model.encode(
        heading_texts_to_encode,
        batch_size=32,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    content_embeddings = model.encode(
        content_texts_to_encode,
        batch_size=32,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    embeddings = [
        ChunkEmbedding(heading_embedding, content_embedding)
        for heading_embedding, content_embedding in zip(
            heading_embeddings, content_embeddings
        )
    ]

    return list(zip(chunks, embeddings))
