from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Generator
from fastapi.testclient import TestClient
import pytest
from pytest_mock import MockerFixture
import src.adapters.api.fast_api_app as fast_api_app
import src.adapters.ai.similarity_search as similarity_search
from tests.mocks import (
    mock_for_cache_provider,
    mock_for_config_loader,
    mock_for_downloader,
    mock_for_image_model,
    mock_for_similarity_search,
    mock_for_text_to_text_model,
)


def test_get_image(tmp_path: Path, mocker: MockerFixture) -> None:
    with setup_app(tmp_path, mocker) as setup:
        image_response = setup.client.get(
            "/image",
            headers={"x-session-token": setup.token},
        )

    assert image_response.status_code == 200
    assert image_response.content == setup.npc_image


@dataclass
class SetupAppResult:
    client: TestClient
    token: str
    npc_image: bytes


@contextmanager
def setup_app(
    tmp_path: Path, mocker: MockerFixture
) -> Generator[SetupAppResult, None, None]:
    responses = {
        r"Create a description of .*": "A cat with a mischievous grin",
        r"generate a walkthrough": '{"crisis":"A crisis","introduction_npc":"Alice","quests_to_resolve_crisis":["Find the rabbit"]}',
    }
    npc_image = b"fake-image"

    mock_for_cache_provider(tmp_path, mocker)
    mock_for_config_loader(mocker)
    mock_for_image_model(mocker, npc_image)
    mock_for_text_to_text_model(mocker, responses)
    mock_for_similarity_search(mocker)
    mock_for_downloader(mocker)

    app = fast_api_app.create_app()

    with TestClient(app) as client:
        response = client.post("/start")

        assert response.status_code == 200
        token = response.json()["session_token"].strip()
        assert token != ""
        yield SetupAppResult(client=client, token=token, npc_image=npc_image)


@pytest.fixture(autouse=True)
def reset_similarity_search_state() -> None:
    similarity_search._chunk_stores.clear()
    similarity_search._vector_stores.clear()
