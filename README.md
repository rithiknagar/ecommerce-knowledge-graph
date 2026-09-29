# E-Commerce Knowledge Graph

A Python-based e-commerce knowledge graph application that uses **Neo4j** for graph storage and an **LLM** to convert natural-language questions into Cypher queries.

The system retrieves relevant data from the graph and generates answers **only from the retrieved graph data**, preventing the answer generator from relying on outside knowledge.

## Features

* E-commerce knowledge graph using Neo4j
* Products, Brands, Categories, Vendors, Customers, and Orders
* Relationship-based graph retrieval
* Natural language → Cypher generation using an LLM
* Read-only Cypher validation
* Parameterized Cypher queries
* Grounded answer generation using retrieved graph data only
* FastAPI REST API
* CSV-based sample dataset
* Automated database seeding
* Unit and integration tests
* Five `banana` product nodes included in the knowledge graph

---

## Architecture

```text
User
 │
 ▼
FastAPI /query
 │
 ▼
Query Service
 │
 ├──────────────► Cypher Generator
 │                      │
 │                      ▼
 │                 LLM (Groq)
 │                      │
 │                      ▼
 │                 Cypher Query
 │                      │
 │                      ▼
 │                Cypher Validator
 │                      │
 │                      ▼
 │                    Neo4j
 │                      │
 │                      ▼
 │               Retrieved Graph Data
 │                      │
 └──────────────────────┘
                        │
                        ▼
                Answer Generator
                        │
                        ▼
                  Grounded Answer
```

### Query flow

1. The user sends a natural-language question.
2. The LLM converts the question into a Cypher query.
3. The generated query is validated to ensure it is read-only and uses the allowed graph schema.
4. The validated query is executed against Neo4j.
5. The retrieved graph data is passed to the answer generator.
6. The answer generator produces the final answer using only the retrieved data.

---

## Graph Model

The knowledge graph contains the following node types:

```text
Product
Brand
Category
Vendor
Customer
Order
```

### Relationships

```text
(:Brand)-[:PRODUCES]->(:Product)

(:Product)-[:BELONGS_TO]->(:Category)

(:Vendor)-[:SUPPLIES]->(:Product)

(:Customer)-[:PLACED]->(:Order)

(:Order)-[:CONTAINS]->(:Product)
```

Relationship direction is important because it represents the semantic meaning of the graph.

For example:

```text
Brand ──PRODUCES──> Product <──SUPPLIES── Vendor
```

This allows multi-hop queries such as:

```cypher
MATCH (b:Brand)-[:PRODUCES]->(p:Product)<-[:SUPPLIES]-(v:Vendor)
WHERE b.name = $brand
RETURN DISTINCT
    b { .* } AS brand,
    p { .* } AS product,
    v { .* } AS vendor
LIMIT 50
```

---

## Tech Stack

* **Python 3.13+**
* **FastAPI**
* **Neo4j 5**
* **Neo4j Python Driver**
* **Groq API / LLM**
* **Pydantic**
* **Pydantic Settings**
* **Pytest**
* **Docker Compose**
* **CSV** for sample data

---

## Project Structure

```text
ecommerce-knowledge-graph/
│
├── app/
│   ├── core/
│   │   └── config.py
│   │
│   ├── graph/
│   │   ├── data_loader.py
│   │   ├── graph_repository.py
│   │   ├── graph_schema.py
│   │   └── neo4j_client.py
│   │
│   ├── llm/
│   │   ├── answer_generator.py
│   │   ├── cypher_generator.py
│   │   ├── llm_client.py
│   │   └── prompts.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── retrieval/
│   │   ├── cypher_validator.py
│   │   └── retrieval_service.py
│   │
│   ├── services/
│   │   └── query_service.py
│   │
│   └── main.py
│
├── data/
│   ├── brands.csv
│   ├── categories.csv
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   └── vendors.csv
│
├── scripts/
│   └── seed_database.py
│
├── tests/
│   ├── test_answer_generator.py
│   ├── test_api.py
│   ├── test_cypher_generator.py
│   ├── test_cypher_validator.py
│   └── test_query_service.py
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Prerequisites

Make sure the following are installed:

* Python 3.13+
* Docker Desktop
* Git
* A Groq API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/rithiknagar/ecommerce-knowledge-graph.git
cd ecommerce-knowledge-graph
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file from `.env.example`.

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Replace:

```text
your_groq_api_key
```

with your actual Groq API key.

---

## 5. Start Neo4j

Start the Neo4j container:

```bash
docker compose up -d
```

Neo4j will be available at:

```text
http://localhost:7474
```

Bolt connection:

```text
bolt://localhost:7687
```

Default credentials used by the project:

```text
Username: neo4j
Password: password123
```

---

## 6. Seed the Database

Run:

```bash
python -m scripts.seed_database 
```

The seed process:

1. Clears the existing development graph.
2. Creates the required constraints.
3. Loads CSV data.
4. Creates nodes.
5. Creates relationships.
6. Adds order quantities to `CONTAINS` relationships.

After successful execution, the Neo4j database contains the sample e-commerce graph.

---

## 7. Run the API

Start FastAPI with:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Query Knowledge Graph

```http
POST /query
```

Request:

```json
{
  "question": "Which vendors supply Apple products?"
}
```

The response contains:

* Original question
* Generated Cypher
* Retrieved graph data
* Final grounded answer

Example response structure:

```json
{
  "question": "Which vendors supply Apple products?",
  "answer": "PrimeWholesale, FastTrade, GlobalDistributors",
  "cypher": "MATCH ...",
  "retrieved_data": [
    {
      "brand": {},
      "product": {},
      "vendor": {}
    }
  ]
}
```

---

## Example Questions

The system supports natural-language questions such as:

### 1. Products by Brand and Vendor

```text
Which Nike products are supplied by TechSupply?
```

### 2. Products by Category

```text
Which products are in the Electronics category?
```

### 3. Customer Purchases

```text
Which products did John Smith purchase?
```

### 4. Vendors by Brand

```text
Which vendors supply Apple products?
```

### 5. Customers by Brand

```text
Which customers purchased Nike products?
```

### 6. Banana Requirement

```text
How many banana products are in the catalog?
```

### 7. Empty Result Handling

```text
Which products are in the NonExistingCategory category?
```

For questions where no matching graph data exists, the system returns an answer indicating that the requested information was not found.

---

## Banana Requirement

The assignment requires the word `banana` to exist exactly five times as a node/value in the knowledge graph and to be retrievable.

The dataset contains five separate Product nodes with the name:

```text
banana
```

They are:

```text
P009
P010
P011
P012
P013
```

They are connected to the rest of the graph through their respective Brand, Category, and Vendor relationships.

Example query:

```text
How many banana products are in the catalog?
```

The retrieval layer can retrieve all five matching Product nodes.

---

## LLM Integration

The application uses an LLM for two separate tasks.

### 1. Natural Language → Cypher

The Cypher generator receives:

```text
User question
+
Graph schema
+
Relationship direction rules
```

and generates a structured Cypher query with parameters.

Example:

```text
Which vendors supply Apple products?
```

can be converted into a graph traversal similar to:

```cypher
MATCH (b:Brand)-[:PRODUCES]->(p:Product)<-[:SUPPLIES]-(v:Vendor)
WHERE b.name = $brand
RETURN DISTINCT
    b { .* } AS brand,
    p { .* } AS product,
    v { .* } AS vendor
LIMIT 50
```

### 2. Retrieved Data → Answer

The retrieved graph data is passed to a separate answer generator.

The answer generator is explicitly instructed to:

* use only retrieved graph data
* not use outside knowledge
* not invent information
* report when information is missing

This keeps the final answer grounded in the knowledge graph.

---

## Cypher Safety

Generated Cypher is validated before execution.

The validator ensures that:

* The query is not empty.
* Only one Cypher statement is allowed.
* Only approved node labels are used.
* Only approved relationship types are used.
* Write operations are rejected.
* Dangerous operations such as `CREATE`, `MERGE`, `DELETE`, `SET`, `DROP`, and `CALL` are rejected.
* User-provided values are passed as query parameters.

This prevents the LLM from directly modifying the graph.

---

## Data Retrieval

The retrieval layer follows:

```text
Natural Language Question
        ↓
Cypher Generation
        ↓
Cypher Validation
        ↓
Neo4j Query Execution
        ↓
Retrieved Graph Data
```

The retrieved records are then passed to the grounded answer generator.

---

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

The test suite covers:

* Cypher generation
* Cypher safety validation
* Grounded answer generation
* End-to-end query execution
* FastAPI `/query` endpoint

---

## Development Notes

The project uses a modular structure so that graph access, LLM interaction, retrieval, validation, API handling, and business orchestration remain separated.

Main responsibilities:

| Component          | Responsibility                               |
| ------------------ | -------------------------------------------- |
| `Neo4jClient`      | Neo4j connection and query execution         |
| `GraphRepository`  | Graph creation and database seeding          |
| `CSVDataLoader`    | CSV dataset loading                          |
| `CypherGenerator`  | Natural language to Cypher                   |
| `CypherValidator`  | Validates generated Cypher                   |
| `RetrievalService` | Executes generated graph queries             |
| `AnswerGenerator`  | Generates grounded answers                   |
| `QueryService`     | Orchestrates retrieval and answer generation |
| `main.py`          | FastAPI application and endpoints            |

---

## Grounding Strategy

The application uses a two-stage LLM flow:

```text
             User Question
                   │
                   ▼
          Cypher Generation LLM
                   │
                   ▼
             Cypher Query
                   │
                   ▼
          Cypher Safety Check
                   │
                   ▼
                Neo4j
                   │
                   ▼
          Retrieved Graph Data
                   │
                   ▼
          Grounded Answer LLM
                   │
                   ▼
             Final Answer
```

The final answer is generated from the retrieved graph data rather than directly from the user's question.

If the graph does not contain the requested information, the answer generator is instructed to report that instead of using external knowledge.

---

## Stopping Neo4j

To stop the Neo4j container:

```bash
docker compose down
```

To start it again:

```bash
docker compose up -d
```

---

## Quick Start

After configuring the environment, the complete workflow is:

```bash
# Install dependencies
pip install -r requirements.txt

# Start Neo4j
docker compose up -d

# Seed database
python -m scripts.seed_database 

# Start API
uvicorn app.main:app --reload
```

Then open:

```text
http://localhost:8000/docs
```

and use:

```text
POST /query
```

with a natural-language e-commerce question.

---

## Assignment Deliverables Covered

| Requirement                    | Implementation              |
| ------------------------------ | --------------------------- |
| Python                         | Python application          |
| Graph database                 | Neo4j                       |
| Products                       | Product nodes               |
| Brands                         | Brand nodes                 |
| Categories                     | Category nodes              |
| Vendors                        | Vendor nodes                |
| Orders                         | Order nodes                 |
| Customers                      | Customer nodes              |
| Relationships                  | Neo4j relationships         |
| Retrieval layer                | `RetrievalService`          |
| LLM integration                | Groq LLM                    |
| Natural language → graph query | `CypherGenerator`           |
| Grounded answers               | `AnswerGenerator`           |
| Query safety                   | `CypherValidator`           |
| Sample dataset                 | CSV files                   |
| Banana requirement             | Five `banana` Product nodes |
| API                            | FastAPI                     |
| Testing                        | Pytest                      |
| Documentation                  | This README                 |

---

## License

This project was created by `Rithik kumar` as a technical assignment/demo project.
