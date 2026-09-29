import json

from app.llm.llm_client import GroqClient
from app.llm.prompts import GROUNDED_ANSWER_PROMPT
from app.models.schemas import GroundedAnswer


class AnswerGenerator:
    def __init__(
        self,
        llm_client: GroqClient,
    ) -> None:
        self.llm_client = llm_client

    def generate(
        self,
        question: str,
        retrieved_data: list[dict],
    ) -> GroundedAnswer:

        retrieved_data_text = json.dumps(
            retrieved_data,
            indent=2,
            default=str,
        )

        prompt = GROUNDED_ANSWER_PROMPT.format(
            question=question,
            retrieved_data=retrieved_data_text,
        )

        return self.llm_client.generate_structured_output(
            prompt=prompt,
            response_model=GroundedAnswer,
        )