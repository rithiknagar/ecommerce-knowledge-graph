from app.llm.answer_generator import AnswerGenerator
from app.llm.llm_client import GroqClient


def test_generate_grounded_answer():
    llm_client = GroqClient()
    answer_generator = AnswerGenerator(llm_client)

    retrieved_data = [
        {
            "product_id": "P009",
            "product_name": "banana",
            "product_price": 1.99,
            "product_stock": 100,
            "brand_id": "B001",
            "brand_name": "Nike",
            "vendor_id": "V001",
            "vendor_name": "TechSupply",
        },
        {
            "product_id": "P001",
            "product_name": "Air Max 90",
            "product_price": 129.99,
            "product_stock": 25,
            "brand_id": "B001",
            "brand_name": "Nike",
            "vendor_id": "V001",
            "vendor_name": "TechSupply",
        },
    ]

    result = answer_generator.generate(
        question="Which Nike products are supplied by TechSupply?",
        retrieved_data=retrieved_data,
    )

    print("\nGrounded Answer:")
    print(result.answer)

    assert result.answer
    assert isinstance(result.answer, str)

def test_empty_retrieval_is_grounded():
    from app.llm.answer_generator import AnswerGenerator
    from app.llm.llm_client import GroqClient

    answer_generator = AnswerGenerator(
        GroqClient()
    )

    result = answer_generator.generate(
        question="Which Nike products are supplied by an unknown vendor?",
        retrieved_data=[],
    )

    print("\nGrounded Empty-Data Answer:")
    print(result.answer)

    assert result.answer