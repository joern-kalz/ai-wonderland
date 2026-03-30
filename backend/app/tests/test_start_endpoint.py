from pathlib import Path
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


@pytest.fixture(autouse=True)
def reset_similarity_search_state() -> None:
    similarity_search._chunk_stores.clear()
    similarity_search._vector_stores.clear()


def test_start_endpoint_returns_session_token(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    responses = {
        r"Create a description of .*": "A cat with a mischievous grin",
        r"generate a walkthrough": '{"crisis":"A crisis","introduction_npc":"Alice","quests_to_resolve_crisis":["Find the rabbit"]}',
    }

    mock_for_cache_provider(tmp_path, mocker)
    mock_for_config_loader(mocker)
    mock_for_image_model(mocker)
    mock_for_text_to_text_model(mocker, responses)
    mock_for_similarity_search(mocker)
    mock_for_downloader(mocker)

    app = fast_api_app.create_app()

    with TestClient(app) as client:
        response = client.post("/start")

    assert response.status_code == 200
    assert response.json()["session_token"].strip() != ""
