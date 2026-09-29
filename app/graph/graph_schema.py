GRAPH_SCHEMA = """
Nodes:

Product:
- id
- name
- price
- stock

Brand:
- id
- name

Category:
- id
- name

Vendor:
- id
- name

Customer:
- id
- name
- email
- city

Order:
- id
- order_date
- status
- total_amount


Relationships:

(:Brand)-[:PRODUCES]->(:Product)

(:Product)-[:BELONGS_TO]->(:Category)

(:Vendor)-[:SUPPLIES]->(:Product)

(:Customer)-[:PLACED]->(:Order)

(:Order)-[:CONTAINS]->(:Product)


Relationship direction is important.

Brand -> Product:
(:Brand)-[:PRODUCES]->(:Product)

Vendor -> Product:
(:Vendor)-[:SUPPLIES]->(:Product)

Product -> Category:
(:Product)-[:BELONGS_TO]->(:Category)

Customer -> Order:
(:Customer)-[:PLACED]->(:Order)

Order -> Product:
(:Order)-[:CONTAINS]->(:Product)


Common multi-hop traversal:

Brand -> Product <- Vendor:
(:Brand)-[:PRODUCES]->(:Product)<-[:SUPPLIES]-(:Vendor)

Customer -> Order -> Product:
(:Customer)-[:PLACED]->(:Order)-[:CONTAINS]->(:Product)

Customer -> Order -> Product <- Brand:
(:Customer)-[:PLACED]->(:Order)-[:CONTAINS]->(:Product)<-[:PRODUCES]-(:Brand)
"""