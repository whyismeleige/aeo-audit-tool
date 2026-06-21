from dataclasses import dataclass

from app.core.parser import ParsedPage

@dataclass
class TextChunk:
    url: str
    heading: str
    content: str
    section_position: int


def chunk(page: ParsedPage) -> list[TextChunk]:
    chunks: list[TextChunk] = []

    for position, section in enumerate(page.sections):
        if section.heading and section.content:
            chunks.append(TextChunk(url=page.url, heading=section.heading, content=section.content, section_position=position))

    return chunks
