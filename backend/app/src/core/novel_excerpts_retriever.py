"""Retrieval of excerpts from Lewis Carrol's novel Alice's Adventures in Wonderland"""

from src.adapters.ai.similarity_search import (
    create_retriever,
    retrieve_by_keyword,
    retrieve_by_question,
)
from src.adapters.web.downloader import download_text
from src.adapters.storage.cache import read_from_cache, write_to_cache


def get_novel_excerpts_for_question(question: str, limit: int) -> list[str]:
    """Provides excerpts from the novel Alice's Adventures in Wonderland related to the question"""

    return retrieve_by_question(retriever_name=_KEY, question=question, limit=limit)


def get_novel_excerpts_for_keyword(keyword: str, limit: int) -> list[str]:
    """Provides excerpts from the novel Alice's Adventures in Wonderland related to the keyword"""

    return retrieve_by_keyword(retriever_name=_KEY, keyword=keyword, limit=limit)


_KEY = "novel_alices_adventures_in_wonderland"
_NOVEL_URL = "https://www.gutenberg.org/cache/epub/11/pg11.txt"
_text = read_from_cache(_KEY)

if _text == None:
    _text = download_text(_NOVEL_URL)
    write_to_cache(_KEY, _text)

create_retriever(retriever_name=_KEY, text=_text)
