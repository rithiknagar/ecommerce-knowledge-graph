from typing import Any

from app.graph.neo4j_client import Neo4jClient


class GraphRepository:
    def __init__(self, client: Neo4jClient) -> None:
        self.client = client

    def clear_database(self) -> None:
        query = """
        MATCH (n)
        DETACH DELETE n
        """

        self.client.execute_query(query)

    def create_constraints(self) -> None:
        constraints = [
            """
            CREATE CONSTRAINT product_id_unique IF NOT EXISTS
            FOR (p:Product)
            REQUIRE p.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT brand_id_unique IF NOT EXISTS
            FOR (b:Brand)
            REQUIRE b.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT category_id_unique IF NOT EXISTS
            FOR (c:Category)
            REQUIRE c.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT vendor_id_unique IF NOT EXISTS
            FOR (v:Vendor)
            REQUIRE v.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
            FOR (c:Customer)
            REQUIRE c.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT order_id_unique IF NOT EXISTS
            FOR (o:Order)
            REQUIRE o.id IS UNIQUE
            """,
        ]

        for query in constraints:
            self.client.execute_query(query)

    def create_brands(self, brands: list[dict[str, Any]]) -> None:
        query = """
        UNWIND $brands AS brand

        MERGE (b:Brand {id: brand.id})
        SET b.name = brand.name
        """

        self.client.execute_query(query, {"brands": brands})

    def create_categories(
        self,
        categories: list[dict[str, Any]],
    ) -> None:
        query = """
        UNWIND $categories AS category

        MERGE (c:Category {id: category.id})
        SET c.name = category.name
        """

        self.client.execute_query(
            query,
            {"categories": categories},
        )

    def create_vendors(self, vendors: list[dict[str, Any]]) -> None:
        query = """
        UNWIND $vendors AS vendor

        MERGE (v:Vendor {id: vendor.id})
        SET v.name = vendor.name
        """

        self.client.execute_query(query, {"vendors": vendors})

    def create_products(self, products: list[dict[str, Any]]) -> None:
        query = """
        UNWIND $products AS product

        MERGE (p:Product {id: product.id})

        SET
            p.name = product.name,
            p.price = product.price,
            p.stock = product.stock
        """

        self.client.execute_query(
            query,
            {"products": products},
        )

    def create_customers(
        self,
        customers: list[dict[str, Any]],
    ) -> None:
        query = """
        UNWIND $customers AS customer

        MERGE (c:Customer {id: customer.id})

        SET
            c.name = customer.name,
            c.email = customer.email,
            c.city = customer.city
        """

        self.client.execute_query(
            query,
            {"customers": customers},
        )

    def create_orders(self, orders: list[dict[str, Any]]) -> None:
        query = """
        UNWIND $orders AS order_data

        MERGE (o:Order {id: order_data.id})

        SET
            o.order_date = order_data.order_date,
            o.status = order_data.status,
            o.total_amount = order_data.total_amount
        """

        self.client.execute_query(
            query,
            {"orders": orders},
        )

    def create_product_relationships(self,products: list[dict[str, Any]],) -> None:
        query = """
        UNWIND $products AS product

        MATCH (p:Product {id: product.id})
        MATCH (b:Brand {id: product.brand_id})
        MATCH (c:Category {id: product.category_id})
        MATCH (v:Vendor {id: product.vendor_id})

        MERGE (b)-[:PRODUCES]->(p)
        MERGE (p)-[:BELONGS_TO]->(c)
        MERGE (v)-[:SUPPLIES]->(p)
        """

        self.client.execute_query(
            query,
            {"products": products},
        )

    def create_customer_order_relationships(self,orders: list[dict[str, Any]],) -> None:
            query = """
            UNWIND $orders AS order_data

            MATCH (c:Customer {id: order_data.customer_id})
            MATCH (o:Order {id: order_data.id})

            MERGE (c)-[:PLACED]->(o)
            """

            self.client.execute_query(
                query,
                {"orders": orders},
            )

    def create_order_product_relationships(self, order_items: list[dict[str, Any]],) -> None:
                query = """
                UNWIND $order_items AS item

                MATCH (o:Order {id: item.order_id})
                MATCH (p:Product {id: item.product_id})

                MERGE (o)-[r:CONTAINS]->(p)

                SET r.quantity = item.quantity
                """

                self.client.execute_query(
                    query,
                    {"order_items": order_items},
                    )

        