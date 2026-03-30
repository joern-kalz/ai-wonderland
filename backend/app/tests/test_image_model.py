from __future__ import annotations
import base64
from collections.abc import Generator
import pytest
from pytest_mock import MockerFixture
import src.adapters.ai.image_model as image_model


@pytest.fixture(autouse=True)
def reset_client() -> Generator[None, None, None]:
    yield
    image_model._client = None


def test_initialize_image_model_sets_client(mocker: MockerFixture) -> None:
    mock_client = mocker.Mock()
    mocker.patch.object(image_model, "OpenAI", return_value=mock_client)

    image_model.initialize_image_model()

    assert image_model._client is mock_client


def test_generate_png_image_returns_decoded_bytes(
    mocker: MockerFixture,
) -> None:
    mock_client = mock_open_ai(mocker)

    image_model.initialize_image_model()
    result = image_model.generate_png_image("a rabbit")

    mock_client.images.generate.assert_called_once_with(
        model="gpt-image-1-mini",
        prompt="a rabbit",
        quality="low",
        size="1024x1024",
    )
    assert result == b"a rabbit"


def mock_open_ai(mocker: MockerFixture):
    def generate(*args, **kwargs):
        prompt = str(kwargs.get("prompt"))
        b64_prompt = base64.b64encode(prompt.encode()).decode()
        fake_image_result = mocker.Mock(b64_json=b64_prompt)
        return mocker.Mock(data=[fake_image_result])

    mock_client = mocker.Mock()
    mock_client.images.generate.side_effect = generate
    mocker.patch.object(image_model, "OpenAI", return_value=mock_client)
    return mock_client


def test_generate_png_image_raises_when_not_initialized() -> None:
    image_model._client = None

    with pytest.raises(
        RuntimeError, match=r"Call initialize_image_model\(\) before use\."
    ):
        image_model.generate_png_image("a rabbit")
