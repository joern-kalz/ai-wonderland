from __future__ import annotations
import base64
import re
from pytest_mock import MockerFixture
import src.adapters.config.config_loader as config_loader
import src.adapters.ai.image_model as image_model
import src.adapters.ai.similarity_search as similarity_search
import src.adapters.ai.text_to_text_model as text_to_text_model
import src.adapters.cache.cache_provider as cache_provider
import src.adapters.web.downloader as downloader


def mock_for_downloader(mocker):
    fake_response = mocker.Mock()
    fake_response.text = "Downloaded text"
    fake_response.raise_for_status.return_value = None
    fake_requests = mocker.Mock()
    fake_requests.get.return_value = fake_response
    mocker.patch.object(downloader, "requests", fake_requests)


def mock_for_similarity_search(mocker):
    fake_splitter = mocker.Mock()
    fake_splitter.create_documents.return_value = [
        mocker.Mock(page_content="some text")
    ]
    mocker.patch.object(
        similarity_search,
        "RecursiveCharacterTextSplitter",
        return_value=fake_splitter,
    )

    fake_embeddings = mocker.Mock()
    mocker.patch.object(
        similarity_search,
        "FastEmbedEmbeddings",
        return_value=fake_embeddings,
    )

    fake_vector_store = mocker.Mock()
    fake_vector_store.save_local.return_value = None
    fake_faiss = mocker.Mock()
    fake_faiss.from_documents.return_value = fake_vector_store
    mocker.patch.object(similarity_search, "FAISS", fake_faiss)


def mock_for_text_to_text_model(
    mocker,
    responses: dict[str, str],
):
    compiled = [(re.compile(pattern), value) for pattern, value in responses.items()]

    def create_side_effect(*_, **kwargs):
        messages = kwargs.get("messages") or []
        prompt = messages[-1]["content"]

        for regex, value in compiled:
            if regex.search(prompt):
                return mocker.Mock(
                    choices=[
                        mocker.Mock(message=mocker.Mock(content=value, tool_calls=[]))
                    ]
                )

        raise AssertionError(f"No mocked response for prompt: {messages}")

    fake_groq = mocker.Mock()
    fake_groq.chat.completions.create.side_effect = create_side_effect
    mocker.patch.object(text_to_text_model, "Groq", return_value=fake_groq)


def mock_for_image_model(mocker, image: bytes):
    fake_openai = mocker.Mock()
    fake_openai.images.generate.return_value = mocker.Mock(
        data=[mocker.Mock(b64_json=base64.b64encode(image).decode())]
    )
    mocker.patch.object(image_model, "OpenAI", return_value=fake_openai)


def mock_for_config_loader(mocker):
    mocker.patch.object(config_loader, "load_dotenv", return_value=None)


def mock_for_cache_provider(tmp_path, mocker: MockerFixture):
    temp_file = tmp_path / "cache_path_provider.py"
    temp_file.write_text("")
    mocker.patch.object(cache_provider, "__file__", str(temp_file))
