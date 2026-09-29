from app.graph.neo4j_client import Neo4jClient
from app.llm.answer_generator import AnswerGenerator
from app.llm.cypher_generator import CypherGenerator
from app.llm.llm_client import GroqClient
from app.retrieval.cypher_validator import CypherValidator
from app.retrieval.retrieval_service import RetrievalService
from app.services.query_service import QueryService


def test_end_to_end_query_service():
    neo4j_client = Neo4jClient()

    try:
        groq_client = GroqClient()

        cypher_generator = CypherGenerator(
            groq_client
        )

        cypher_validator = CypherValidator()

        retrieval_service = RetrievalService(
            neo4j_client=neo4j_client,
            cypher_generator=cypher_generator,
            cypher_validator=cypher_validator,
        )

        answer_generator = AnswerGenerator(
            groq_client
        )

        query_service = QueryService(
            retrieval_service=retrieval_service,
            answer_generator=answer_generator,
        )

        result = query_service.execute(
            "Which Nike products are supplied by TechSupply?"
        )

        print("\nQuestion:")
        print(result.question)

        print("\nGenerated Cypher:")
        print(result.cypher)

        print("\nRetrieved Graph Data:")
        print(result.retrieved_data)

        print("\nFinal Grounded Answer:")
        print(result.answer)

        assert result.question
        assert result.cypher
        assert result.retrieved_data
        assert result.answer

        product_names = {
            item["product_name"]
            for item in result.retrieved_data
        }

        assert "Air Max 90" in product_names
        assert "banana" in product_names

    finally:
        neo4j_client.close()