from typing import Any

from neo4j import Driver, GraphDatabase

from app.core.config import settings


class Neo4jClient:
    def __init__(self) -> None:
        self.driver: Driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_username,
                settings.neo4j_password,
            ),
        )

    def verify_connection(self) -> None:
        self.driver.verify_connectivity()

    def execute_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ):
        result = self.driver.execute_query(
            query,
            parameters_=parameters or {},
        )

        records, summary, keys = result

        return records

    def close(self) -> None:
        self.driver.close()