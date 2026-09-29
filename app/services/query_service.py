from app.llm.answer_generator import AnswerGenerator
from app.models.schemas import QueryResponse
from app.retrieval.retrieval_service import RetrievalService


class QueryService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        answer_generator: AnswerGenerator,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.answer_generator = answer_generator

    def execute(self, question: str) -> QueryResponse:
        retrieval_result = self.retrieval_service.execute(
            question
        )

        grounded_answer = self.answer_generator.generate(
            question=question,
            retrieved_data=retrieval_result.data,
        )

        return QueryResponse(
            question=question,
            answer=grounded_answer.answer,
            cypher=retrieval_result.query,
            retrieved_data=retrieval_result.data,
        )