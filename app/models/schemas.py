from typing import Any

from pydantic import BaseModel, ConfigDict


class RetrievalResult(BaseModel):
    query: str
    data: list[dict[str, Any]]


class CypherParameter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    value: str


class CypherQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cypher: str
    parameters: list[CypherParameter]

    def parameter_dict(self) -> dict[str, str]:
        return {
            parameter.name: parameter.value
            for parameter in self.parameters
        }

class GroundedAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    cypher: str
    retrieved_data: list[dict[str, Any]]

class QueryRequest(BaseModel):
    question: str