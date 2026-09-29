from pathlib import Path

from app.graph.data_loader import CSVDataLoader
from app.graph.graph_repository import GraphRepository
from app.graph.neo4j_client import Neo4jClient


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def prepare_products(products: list[dict]) -> list[dict]:
    for product in products:
        product["price"] = float(product["price"])
        product["stock"] = int(product["stock"])

    return products


def prepare_orders(orders: list[dict]) -> list[dict]:
    for order in orders:
        order["total_amount"] = float(order["total_amount"])

    return orders


def main() -> None:
    loader = CSVDataLoader(DATA_DIR)

    brands = loader.load("brands.csv")
    categories = loader.load("categories.csv")
    vendors = loader.load("vendors.csv")
    products = prepare_products(
        loader.load("products.csv")
    )
    customers = loader.load("customers.csv")
    orders = prepare_orders(
        loader.load("orders.csv")
    )
    order_items = loader.load("order_items.csv")

    client = Neo4jClient()
    repository = GraphRepository(client)

    try:
        print("Connecting to Neo4j...")
        client.verify_connection()

        print("Clearing existing graph...")
        repository.clear_database()

        print("Creating constraints...")
        repository.create_constraints()

        print("Creating brands...")
        repository.create_brands(brands)

        print("Creating categories...")
        repository.create_categories(categories)

        print("Creating vendors...")
        repository.create_vendors(vendors)

        print("Creating products...")
        repository.create_products(products)

        print("Creating customers...")
        repository.create_customers(customers)

        print("Creating orders...")
        repository.create_orders(orders)

        print("Creating product relationships...")
        repository.create_product_relationships(products)

        print("Creating customer-order relationships...")
        repository.create_customer_order_relationships(orders)

        print("Creating order-product relationships...")
        repository.create_order_product_relationships(
            order_items
        )

        print("\nKnowledge graph successfully created.")

    finally:
        client.close()


if __name__ == "__main__":
    main()