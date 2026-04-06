from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass

import pytest
from pytest_mock import MockType, MockerFixture

import src.adapters.ai.similarity_search as similarity_search


@pytest.fixture(autouse=True)
def reset_similarity_search_state() -> Generator[None, None, None]:
    yield
    similarity_search._chunk_stores.clear()
    similarity_search._vector_stores.clear()


def mock_cache_path(mocker: MockerFixture, exists: bool):
    cache_path = mocker.Mock()
    cache_path.exists.return_value = exists
    mocker.patch.object(similarity_search, "get_cache_path", return_value=cache_path)
    return cache_path


@dataclass
class TextSplitterMock:
    constructor: MockType
    text_splitter: MockType


@dataclass
class EmbeddingsMock:
    constructor: MockType
    embeddings: MockType


def mock_text_splitter(mocker: MockerFixture, documents: list) -> TextSplitterMock:
    text_splitter = mocker.Mock()
    text_splitter.create_documents.return_value = documents
    constructor = mocker.patch.object(
        similarity_search,
        "RecursiveCharacterTextSplitter",
        return_value=text_splitter,
    )
    return TextSplitterMock(constructor=constructor, text_splitter=text_splitter)


def mock_embeddings(mocker: MockerFixture) -> EmbeddingsMock:
    embeddings = mocker.Mock()
    constructor = mocker.patch.object(
        similarity_search,
        "FastEmbedEmbeddings",
        return_value=embeddings,
    )
    return EmbeddingsMock(constructor=constructor, embeddings=embeddings)


def mock_faiss(
    mocker: MockerFixture,
    from_documents_result: object,
    load_local_result: object | None = None,
):
    constructor = mocker.patch.object(similarity_search, "FAISS")
    constructor.from_documents.return_value = from_documents_result
    if load_local_result is not None:
        constructor.deserialize_from_bytes.return_value = load_local_result
    return constructor


def test_retrieve_by_keyword_returns_matching_chunks() -> None:
    similarity_search._chunk_stores["keyword_retriever"] = [
        type("Doc", (), {"page_content": "apple"})(),
        type("Doc", (), {"page_content": "banana apple"})(),
        type("Doc", (), {"page_content": "cherry"})(),
    ]

    result = similarity_search.retrieve_by_keyword(
        retriever_name="keyword_retriever",
        keyword="apple",
        limit=2,
    )

    assert result == ["apple", "banana apple"]


def test_retrieve_by_question_uses_vector_store_retriever(
    mocker: MockerFixture,
) -> None:
    documents = [
        type("Doc", (), {"page_content": "answer one"})(),
        type("Doc", (), {"page_content": "answer two"})(),
    ]
    retriever = mocker.Mock()
    retriever.invoke.return_value = documents
    vector_store = mocker.Mock()
    vector_store.as_retriever.return_value = retriever
    similarity_search._vector_stores["question_retriever"] = vector_store

    result = similarity_search.retrieve_by_question(
        retriever_name="question_retriever",
        question="what is the answer?",
        limit=2,
    )

    vector_store.as_retriever.assert_called_once_with(search_kwargs={"k": 2})
    retriever.invoke.assert_called_once_with("what is the answer?")
    assert result == ["answer one", "answer two"]
