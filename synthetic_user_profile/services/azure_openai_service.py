from dataclasses import dataclass

from lagom.environment import Env
from openai import AsyncAzureOpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionMessageParam,
)

from synthetic_user_profile.protocols.i_azure_openai_service import (
    IAzureOpenAIService,
)


class AzureOpenAIEnv(Env):
    azure_openai_endpoint: str
    azure_openai_key: str
    azure_openai_api_version: str
    azure_openai_deployed_model_name: str


@dataclass
class AzureOpenAIService(IAzureOpenAIService):
    env: AzureOpenAIEnv

    async def generate(
        self, prompts: list[ChatCompletionMessageParam], **kwargs
    ) -> ChatCompletion:
        client = AsyncAzureOpenAI(
            api_key=self.env.azure_openai_key,
            api_version=self.env.azure_openai_api_version,
            azure_endpoint=self.env.azure_openai_endpoint,
        )
        result = await client.chat.completions.create(
            model=self.env.azure_openai_deployed_model_name,
            messages=prompts,
            **kwargs,
        )

        return result
