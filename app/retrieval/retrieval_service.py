from typing import Any

from app.graph.neo4j_client import Neo4jClient
from app.llm.cypher_generator import CypherGenerator
from app.models.schemas import RetrievalResult
from app.retrieval.cypher_validator import CypherValidator


class RetrievalService:
    def __init__(
        self,
        neo4j_client: Neo4jClient,
        cypher_generator: CypherGenerator,
        cypher_validator: CypherValidator,
    ) -> None:
        self.neo4j_client = neo4j_client
        self.cypher_generator = cypher_generator
        self.cypher_validator = cypher_validator

    def execute(
        self,
        question: str,
    ) -> RetrievalResult:
        generated_query = self.cypher_generator.generate(
            question
        )

        cypher = self.cypher_validator.validate(
            generated_query.cypher
        )

        parameters: dict[str, Any] = (
            generated_query.parameter_dict()
        )

        records = self.neo4j_client.execute_query(
            cypher,
            parameters,
        )

        data = [
            record.data()
            for record in records
        ]

        return RetrievalResult(
            query=cypher,
            data=data,
        )