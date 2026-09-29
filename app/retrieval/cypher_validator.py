import re


class CypherValidationError(ValueError):
    """Raised when generated Cypher is not safe to execute."""


class CypherValidator:
    READ_ONLY_KEYWORDS = {
        "CREATE",
        "MERGE",
        "DELETE",
        "DETACH",
        "SET",
        "REMOVE",
        "DROP",
        "CALL",
        "LOAD",
        "USE",
        "FOREACH",
    }

    ALLOWED_LABELS = {
        "Product",
        "Brand",
        "Category",
        "Vendor",
        "Customer",
        "Order",
    }

    ALLOWED_RELATIONSHIPS = {
        "PRODUCES",
        "BELONGS_TO",
        "SUPPLIES",
        "PLACED",
        "CONTAINS",
    }

    def validate(self, cypher: str) -> str:
        if not cypher or not cypher.strip():
            raise CypherValidationError(
                "Cypher query cannot be empty."
            )

        normalized = cypher.strip()

        self._validate_single_statement(normalized)
        self._validate_read_only(normalized)
        self._validate_labels(normalized)
        self._validate_relationships(normalized)

        return normalized

    def _validate_single_statement(self, cypher: str) -> None:
        statements = [
            statement.strip()
            for statement in cypher.split(";")
            if statement.strip()
        ]

        if len(statements) > 1:
            raise CypherValidationError(
                "Multiple Cypher statements are not allowed."
            )

    def _validate_read_only(self, cypher: str) -> None:
        for keyword in self.READ_ONLY_KEYWORDS:
            pattern = rf"\b{keyword}\b"

            if re.search(
                pattern,
                cypher,
                re.IGNORECASE,
            ):
                raise CypherValidationError(
                    f"Unsafe Cypher keyword detected: {keyword}"
                )

    def _validate_labels(self, cypher: str) -> None:
        labels = re.findall(
            r":([A-Za-z_][A-Za-z0-9_]*)",
            cypher,
        )

        for label in labels:
            if label in self.ALLOWED_RELATIONSHIPS:
                continue

            if label not in self.ALLOWED_LABELS:
                raise CypherValidationError(
                    f"Unknown graph label detected: {label}"
                )

    def _validate_relationships(self, cypher: str) -> None:
        relationships = re.findall(
            r"\[:([A-Za-z_][A-Za-z0-9_]*)",
            cypher,
        )

        for relationship in relationships:
            if relationship not in self.ALLOWED_RELATIONSHIPS:
                raise CypherValidationError(
                    f"Unknown relationship detected: {relationship}"
                )