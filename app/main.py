from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.graph.neo4j_client import Neo4jClient
from app.llm.answer_generator import AnswerGenerator
from app.llm.cypher_generator import CypherGenerator
from app.llm.llm_client import GroqClient
from app.models.schemas import QueryRequest, QueryResponse
from app.retrieval.cypher_validator import CypherValidator
from app.retrieval.retrieval_service import RetrievalService
from app.services.query_service import QueryService


neo4j_client = Neo4jClient()
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    neo4j_client.verify_connection()

    yield

    neo4j_client.close()


app = FastAPI(
    title="E-Commerce Knowledge Graph API",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {
        "status": "Application running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/query",response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        return query_service.execute(
            request.question
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to process the query.",
        ) from exc