from app.llm.llm_client import GroqClient
from app.llm.prompts import CYPHER_GENERATION_PROMPT
from app.models.schemas import CypherQuery


class CypherGenerator:
    def __init__(self, llm_client: GroqClient) -> None:
        self.llm_client = llm_client

    def generate(self, question: str) -> CypherQuery:
        prompt = CYPHER_GENERATION_PROMPT.format(
            question=question
        )

        result = self.llm_client.generate_structured_output(
            prompt=prompt,
            response_model=CypherQuery,
        )

        return CypherQuery(
            cypher=result.cypher,
            parameters=result.parameters,
        )