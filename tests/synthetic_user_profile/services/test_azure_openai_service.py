import pytest
from pytest_mock import MockerFixture

from synthetic_user_profile.services.azure_openai_service import (
    AzureOpenAIEnv,
    AzureOpenAIService,
)


@pytest.mark.asyncio
async def test_generate(mocker: MockerFixture):
    mocker.patch(
        "synthetic_user_profile.services.azure_openai_service.AsyncAzureOpenAI",
        return_value=mocker.AsyncMock(),
    )
    service = AzureOpenAIService(
        AzureOpenAIEnv(
            azure_openai_endpoint="https://api.openai.com",
            azure_openai_key="fake_key",
            azure_openai_api_version="2020-05-10",
            azure_openai_deployed_model_name="curie",
        )
    )
    result = await service.generate(
        [
            {
                "role": "system",
                "content": "Hello, how are you?",
            }
        ]
    )
    assert result is not None
