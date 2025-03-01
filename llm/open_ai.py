import os
import asyncio
from typing import Dict, List, Optional, Type

from openai import AsyncOpenAI

from utils.logger import logger


class ChatGPTClient:

    def __init__(
        self,
        api_key: str = os.environ.get("OPENAI_API_KEY", ""),
        model: str = "gpt-4o-mini",
    ):
        self.client = AsyncOpenAI(api_key=api_key)
        self.max_tokens = 16383
        self.model = model
        self.max_retries = 3
        self.delays = [10, 30, 60]

    async def query(
        self,
        messages: List[Dict[str, str]],
        response_format: Optional[Type] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ) -> str:

        for attempt in range(self.max_retries + 1):
            try:
                if response_format is None:
                    completion = await self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=self.max_tokens,
                    )
                    return completion.choices[0].message.content

                completion = await self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=messages,
                    response_format=response_format,
                    max_tokens=self.max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                )
                return completion.choices[0].message.parsed

            except Exception as e:
                if attempt == self.max_retries:  
                    raise
                delay = self.delays[attempt]
                logger.error(
                    f"OpenAI API error (attempt {attempt + 1}/{self.max_retries}): {str(e)}. Retrying in {delay}s..."
                )
                await asyncio.sleep(delay)

    async def query_with_functions(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict],
        temperature: float = 1.0,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ) -> List[Dict]:

        for attempt in range(self.max_retries + 1):
            try:
                completion = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                    max_tokens=self.max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                )

                response = completion.choices[0].message

                if response.tool_calls:
                    return response.tool_calls

                return []

            except Exception as e:
                if attempt == self.max_retries:  
                    raise
                delay = self.delays[attempt]
                logger.error(
                    f"OpenAI API error (attempt {attempt + 1}/{self.max_retries}): {str(e)}. Retrying in {delay}s..."
                )
                await asyncio.sleep(delay)
