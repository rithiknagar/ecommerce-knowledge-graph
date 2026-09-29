import json
from typing import TypeVar

from groq import Groq
from pydantic import BaseModel

from app.core.config import settings


T = TypeVar("T", bound=BaseModel)


class GroqClient:
    def __init__(self) -> None:
        self.client = Groq(
            api_key=settings.groq_api_key
        )

    def generate_structured_output(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        response = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "strict": True,
                    "schema": response_model.model_json_schema(),
                },
            },
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Groq returned an empty response.")

        data = json.loads(content)

        return response_model.model_validate(data)