from app.llm.cypher_generator import CypherGenerator
from app.llm.llm_client import GroqClient


def test_generate_cypher_for_nike_products():
    llm_client = GroqClient()
    generator = CypherGenerator(llm_client)

    result = generator.generate(
        "Which Nike products are supplied by TechSupply?"
    )

    print("\nGenerated Cypher:")
    print(result.cypher)

    print("\nParameters:")
    print(result.parameters)

    parameters = result.parameter_dict()

    print("\nParameter Dictionary:")
    print(parameters)

    assert result.cypher
    assert isinstance(result.cypher, str)

    assert isinstance(result.parameters, list)

    assert parameters["brand"] == "Nike"
    assert parameters["vendor"] == "TechSupply"

    assert "MATCH" in result.cypher.upper()
    assert "RETURN" in result.cypher.upper()