import pytest

from app.retrieval.cypher_validator import (
    CypherValidationError,
    CypherValidator,
)


@pytest.fixture
def validator():
    return CypherValidator()


def test_valid_read_only_query(validator):
    cypher = """
    MATCH (b:Brand)-[:PRODUCES]->(p:Product)
    WHERE b.name = $brand
    RETURN p.id AS product_id, p.name AS product_name
    LIMIT 50
    """

    result = validator.validate(cypher)

    assert result.strip() == cypher.strip()


def test_reject_create(validator):
    cypher = """
    CREATE (p:Product {name: 'Test'})
    """

    with pytest.raises(CypherValidationError):
        validator.validate(cypher)


def test_reject_delete(validator):
    cypher = """
    MATCH (p:Product)
    DELETE p
    """

    with pytest.raises(CypherValidationError):
        validator.validate(cypher)


def test_reject_merge(validator):
    cypher = """
    MERGE (p:Product {name: 'Test'})
    """

    with pytest.raises(CypherValidationError):
        validator.validate(cypher)


def test_reject_set(validator):
    cypher = """
    MATCH (p:Product)
    SET p.price = 10
    RETURN p
    """

    with pytest.raises(CypherValidationError):
        validator.validate(cypher)


def test_reject_multiple_statements(validator):
    cypher = """
    MATCH (p:Product)
    RETURN p;

    DELETE p
    """

    with pytest.raises(CypherValidationError):
        validator.validate(cypher)


def test_reject_unknown_label(validator):
    cypher = """
    MATCH (u:User)
    RETURN u
    """

    with pytest.raises(CypherValidationError):
        validator.validate(cypher)


def test_reject_unknown_relationship(validator):
    cypher = """
    MATCH (p:Product)-[:HACKS]->(x:Product)
    RETURN p
    """

    with pytest.raises(CypherValidationError):
        validator.validate(cypher)


def test_reject_empty_query(validator):
    with pytest.raises(CypherValidationError):
        validator.validate("")

def test_reject_call():
    validator = CypherValidator()

    with pytest.raises(CypherValidationError):
        validator.validate(
            "CALL db.labels()"
        )


def test_reject_load_csv():
    validator = CypherValidator()

    with pytest.raises(CypherValidationError):
        validator.validate(
            "LOAD CSV FROM 'file:///data.csv' AS row RETURN row"
        )


def test_reject_use():
    validator = CypherValidator()

    with pytest.raises(CypherValidationError):
        validator.validate(
            "USE system MATCH (n) RETURN n"
        )


def test_reject_foreach():
    validator = CypherValidator()

    with pytest.raises(CypherValidationError):
        validator.validate(
            """
            FOREACH (x IN [1,2,3] |
                CREATE (:Product {id: x})
            )
            """
        )