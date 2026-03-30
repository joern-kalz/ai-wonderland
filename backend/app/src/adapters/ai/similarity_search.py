"""Retrieval of excerpts from a text based on their similarity to a question"""

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

from src.adapters.cache.cache_path_provider import get_cache_path


def create_retriever(
    retriever_name: str,
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> None:
    """Creates a retriever providing excerpts from the text related to a question"""

    _text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    _chunk_stores[retriever_name] = _text_splitter.create_documents([text])
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    cache = get_cache_path(retriever_name)

    if cache.exists():
        _vector_stores[retriever_name] = FAISS.load_local(
            str(cache), embeddings, allow_dangerous_deserialization=True
        )
    else:
        print("Creating vector store. This can take a few seconds...")
        _vector_stores[retriever_name] = FAISS.from_documents(
            _chunk_stores[retriever_name], embeddings
        )
        _vector_stores[retriever_name].save_local(str(cache))
        print("Vector store created.")


def retrieve_by_keyword(
    retriever_name: str,
    keyword: str,
    limit: int,
) -> list[str]:
    chunk_store = _chunk_stores[retriever_name]
    matches = [doc for doc in chunk_store if keyword in doc.page_content]
    return [match.page_content for match in matches[:limit]]


def retrieve_by_question(retriever_name: str, question: str, limit: int) -> list[str]:
    _retriever = _vector_stores[retriever_name].as_retriever(search_kwargs={"k": limit})
    documents = _retriever.invoke(question)
    return [document.page_content for document in documents]


_chunk_stores: dict[str, list] = {}
_vector_stores: dict[str, FAISS] = {}
