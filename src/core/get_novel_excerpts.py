"""Retrieval of excerpts from Lewis Carrol's novel Alice's Adventures in Wonderland"""

import sys

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.adapters.downloader import download_text
from src.adapters.cache import read_from_cache, write_to_cache


def get_novel_excerpts(question: str) -> list[str]:
    """Provides excerpts from the novel Alice's Adventures in Wonderland related to the question"""

    documents = _retriever.invoke(question)
    return [document.page_content for document in documents]


_CACHE_KEY = "novel_alices_adventures_in_wonderland"
_NOVEL_URL = "https://www.gutenberg.org/cache/epub/11/pg11.txt"

_text = read_from_cache(_CACHE_KEY)

if _text == None:
    _text = download_text(_NOVEL_URL)
    write_to_cache(_CACHE_KEY, _text)

_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
_documents = _text_splitter.create_documents([_text])

_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
_vector_store = FAISS.from_documents(_documents, _embeddings)
_retriever = _vector_store.as_retriever(search_kwargs={"k": 2})

if __name__ == "__main__":
    while True:
        excerpts = get_novel_excerpts(input("Question: "))
        print("\n---------------\n".join(excerpts))
