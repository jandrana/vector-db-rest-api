# Vector DB REST API

A containerized REST API for indexing and querying documents using a vector database.

It allows users to create libraries, upload text documents, and perform both Semantic Vector Search and Exact Keyword Search through different indexing algorithms.

## ✨ Features

*   **Hybrid Search:** Supports both **k-NN Vector Search** (Semantic) and **Inverted Index Search** (Keyword).
*   **Thread-Safe DB:** In-Memory database implementation using `RLock` to prevent data races and deadlocks.
*   **Layered Architecture:** Strict separation of concerns (API -> Services -> Data Layer).
*   **Dockerized:** Project containerization with Docker.
*   **Setup:** Automated setup via `Makefile`.

## 🏗️ Code Quality & Architecture

### SOLID Principles
*   **SRP:** Clear separation - API routes (HTTP), Services (business logic), Repositories (data access)
*   **OCP:** Extensible via Strategy pattern.
*   **LSP:** All repositories/services implement interfaces (`IChunkRepository`, `ISearchService`, etc.)
*   **ISP:** Focused interfaces in `app/interfaces/`. No forced dependencies
*   **DIP:** Dependency injection via `dependency-injector` containers. Services depend on interfaces

### Domain-Driven Design
*   **Multi-Layer Architecture:** API → Services → Repositories → Storage
*   **Repository Pattern:** Data access abstracted through interfaces
*   **Service Layer:** Business logic separated from data access

### Design Patterns
*   **Strategy Pattern:** Pluggable search strategies (`KnnSearchStrategy`, `KeywordSearchStrategy`)
*   **Repository Pattern:** Data access abstraction via interfaces
*   **Decorator Pattern:** Validation decorators (`@library_exists`, `@document_exists`, `@chunk_exists`)

### Code Quality
*   **No Hardcoded Values:** Configuration via Pydantic Settings
*   **Thread Safety:** `RLock` in repository methods

## 📁 Project Structure

Following a Domain-Driven Design (DDD) inspired structure with strict separation of concerns across three layers: API, Services, and Repositories. The architecture uses dependency injection, interfaces for abstraction, and design patterns for extensibility.

```text
vector-db-rest-api/
├── app/
│   ├── api/                          # 🗣️ API Layer (HTTP Interface)
│   │   ├── routes/                   # RESTful API Endpoints
│   │   └── deps.py                   # FastAPI dependency injection
│   ├── core/                         # ⚙️ Core Utilities & Configuration
│   ├── interfaces/                   # 🔌 Interface Definitions (Abstraction Layer)
│   │   ├── repositories/             # Repository interfaces
│   │   ├── services/                 # Service interfaces
│   │   ├── id_generation.py          # IIdGenerator
│   │   ├── indexing.py               # Indexing interfaces
│   │   └── persistence.py            # Persistence interfaces
│   ├── db/                           # 💾 Data Layer (Repository Implementation)
│   │   ├── containers.py             # DbContainer (DI for data layer)
│   │   ├── id_generator.py           # ID generation implementation
│   │   ├── inverted_index.py         # Keyword search index
│   │   ├── models.py                 # Domain models (Library, Document, Chunk)
│   │   ├── tokenization.py           # Text tokenization strategy
│   │   ├── repositories/             # Repository implementations
│   │   └── storage/                  # Persistence Layer (AOL Pattern)
│   ├── schemas/                      # 📋 Pydantic Schemas (DTOs & Validation)
│   ├── services/                     # 🧠 Business Logic Layer
<<<<<<< HEAD
│   │   ├── containers.py             # ServiceContainer (DI for services)
│   │   ├── chunk_service.py          # ChunkService (business logic)
│   │   ├── document_service.py       # DocumentService
=======
│   │   ├── containers.py            # ServiceContainer (DI for services)
│   │   ├── chunk_service.py          # ChunkService (business logic)
│   │   ├── document_service.py      # DocumentService
>>>>>>> main
│   │   ├── library_service.py        # LibraryService
│   │   ├── index_service.py          # IndexService (embedding generation)
│   │   ├── embedding/                # Embedding Service
│   │   │   ├── embedding_provider.py # CohereEmbeddingProvider
│   │   │   └── embedding_service.py      # EmbeddingService
│   │   └── search/                   # Search Service (Strategy Pattern)
│   │       ├── search_service.py     # SearchService (strategy registry)
│   │       └── strategies/           # Search Strategy Implementations
│   └── main.py                       # 🏁 FastAPI Application Entry Point
├── client/                           # 📦 Python SDK Client
│   ├── sdk.py                        # VectorDBClient class
│   └── example.py                    # SDK usage demonstration
├── tests/                            # 🧪 Test Suite
├── workflows/                        # 🤖 n8n Workflow Definitions
│   └── ai_document_ingestion.json    # AI agent ingestion pipeline
├── Makefile                          # 🛠️ Automation Commands
├── Dockerfile                        # 🐳 Docker Configuration
├── docker-compose.yml                # Docker Compose configuration
├── requirements.txt                  # 🐍 Production Dependencies
└── requirements-dev.txt               # Development Dependencies
```

### Architecture Flow

**Request Flow:** `HTTP Request → API Route → Service → Repository → Storage`

*   **API Layer:** HTTP handling, Pydantic validation, dependency injection via `Depends()`
*   **Service Layer:** Business logic, orchestration, decorators for validation
*   **Repository Layer:** Thread-safe data access (`RLock`), persistence via `PersistenceManager`
*   **Storage Layer:** Append-Only Log (AOL) pattern for persistence

**Dependency Injection:** Three-tier container system (`AppContainer` → `ServiceContainer` + `DbContainer`) manages all dependencies with lifecycle management via FastAPI's `lifespan` context manager.

## 🛠️ Quick Start

### Prerequisites
*   Python 3.10+ or Docker
*   A [Cohere API Key](https://cohere.com/) (for embedding generation)

1.  **Generate and configure `.env`:**
    ```ini
    cp .env.example .env
    ```

2.  **Configure Environment:**
    Open the `.env` file and paste your API Key:
    ```ini
    COHERE_API_KEY=your_cohere_api_key_here
    ```

### Option A: Docker

1.  **Build & Run:**
    ```bash
    make build
    make up
    ```

### Option B: Local Setup

1.  **Create and activate Virtual Environment:**
    ```bash
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate

    make install
    ```

2.  **Run:**
    ```bash
    make run
    ```

## 📚 Documentation & Testing

### Interactive API Docs (Swagger UI)
Once running, visit: **[http://localhost:8000/docs](http://localhost:8000/docs)**
Interact directly with every endpoint directly from the browser.

### 🧑‍💻 Developer Setup

#### Using Makefile

1. Create and activate Virtual Environment:

```bash
make venv
# Windows
.venv\Scripts\activate

# Git Bash (Windows)
source .venv/Scripts/activate

# Mac/Linux
source .venv/bin/activate

```

2. Install dependencies:
```bash
make install	# installs dependencies
make install-dev # installs dev dependencies and pre-commit hooks
```

#### Manual Steps

Install production and developer dependencies
```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
pre-commit install -t pre-push
```

### Running Tests
Run tests with:
```bash
make test	# uses .venv if available
# or
python -m pytest
```

### Testing

*   **Test Isolation:** Temporary DB files per session using fresh container instances.
*   **Dependency Injection:** Tests use same DI container system as production (`test_container` fixture)
*   **Mocking:** External services (Cohere API) stubbed globally to avoid external calls
*   **Coverage:** API routes, database, services, inverted index, math utils, search strategies
*   **FastAPI TestClient:** Realistic HTTP testing with response validation
*   **Pre-commit Hooks:** Automated test execution via `pre-push` hook; CI runs on push/PR

## 🧠 Challenge Approach: Algorithms & Complexity

### 1. Vector Search Algorithm (Semantic)
*   **Implementation:** Linear Scan (Brute Force) with Cosine Similarity.
*   **Logic:** When a query comes in, the system embeds it and calculates the dot product against every chunk in the library, sorting by the highest score.
*   **Time Complexity:** $O(N \cdot D)$
    *   $N$: Number of chunks.
    *   $D$: Dimension of embedding (e.g., 1024).
    *   It iterates over every vector to find the nearest neighbor.
*   **Space Complexity:** $O(N \cdot D)$
    *   It stores the vector for every chunk in memory.

### 2. Inverted Index Algorithm (Keyword)
*   **Implementation:** Hash Map (Dictionary) mapping `Word -> Set[ChunkIDs]`.
*   **Logic:** During chunk creation, text is tokenized and added to the index. Search performs an $O(1)$ lookup to retrieve chunks containing specific terms.
*   **Time Complexity:** $O(1)$
    *   Python dictionary lookups are constant time.
*   **Space Complexity:** $O(T)$
    *   $T$: Total number of tokens.
    *   Each unique word points to a list of IDs where it appears.

### 3. Concurrency & Data Safety
To avoid data races between reads and writes to the database, the `Database` class is implemented thread-safe by using **`threading.RLock()`** which allows nested method calls without causing a deadlock.

## 🤖 n8n AI Agent (Bonus)

I implemented an **Agentic Ingestion Pipeline** using n8n and Google Gemini.
*   **Workflow:** The user asks the agent in natural language to create a document about a topic in a given library (e.g., "Create a document in Library 1 about why Python is great for AI"). The AI generates the content, structures it into JSON, divides the document content in chunks, and uploads it to the Vector DB via the API.

### How to Import:
1.  Run `make up`.
2.  Open [http://localhost:5678](http://localhost:5678).
3.  **Setup Credentials:**
    *   Go to **Credentials** -> **Add Credential**.
    *   Search for **Google Gemini (PaLM) API**.
    *   Enter your API Key (or use OpenAI if you prefer, switching the model node).
4.  **Import Workflow:**
    *   Click **Add Workflow** -> **Import from File**.
    *   Select `workflows/ai_agent_ingestion_pipeline.json`.
5.  **Connect Credential:**
    *   Double click the **Google Gemini Chat Model** node.
    *   Select the Credential you just created.
6.  **Run:** Click "Chat" and ask it to create a document!

## 💾 Persistence to Disk (Bonus)

To ensure data durability across container restarts, I implemented an **Append-Only Log (AOL)** persistence mechanism for the In-Memory Database.

### Design Choices
*   **Mechanism:**. Pivoted from snapshotting the entire database state to disk on every change (which would be $O(N)$) to implementing an AOL mechanism, where the system appends each operation as a single JSON line to `vector_db.jsonl`.
*   **Performance:** AOL improves performance significantly since it only writes a single line ( instantaneous regardless of database size) without making a complete snapshot every time.
*   **Recovery:** On startup, the system reads the log file line-by-line and "replays" the events to rebuild the in-memory state.

### Tradeoffs
*   **Pros:** $O(1)$ write performance, human-readable data format, crash recovery and easy data recovery.
*   **Cons:** Startup time grows linearly with the number of historical operations (since the whole log must be replayed).
*   **Solution:** I would implement a Log Cleaning system to periodically rewrite the log to remove "old" records (cancelled creates because of later deletes) to save disk space and optimize startup time.

## 📦 Python SDK Client (Bonus)

I implemented a dedicated Python client to simplify interacting with the API programmatically. It handles session management, error parsing, and type hinting.

### 1. Structure
The client code is located in the `client/` directory:
*   `client/sdk.py`: The reusable `VectorDBClient` class.
*   `client/example.py`: A runnable script demonstrating a full workflow.

### 2. Usage Example

You can use the client in your own scripts:

```python
from client.sdk import Client

# Initialize
client = Client()

# Create a library
lib = client.create_library("My Knowledge Base")

# Upload data
doc = client.create_document(library['id'], "Physics Notes")
client.create_chunk(document['id'], "E=mc^2 is the mass-energy equivalence.")

# Index
client.index_library(library['id'])

# Search
# 1. Semantic Search
results = client.search(library['id'], "Energy", k=3, search_type="knn")

# 2. Keyword Search
results = client.search(library['id'], "E=mc^2", k=2, search_type="keyword")
```

### 3. Running the Demo
I have provided a pre-built example script that runs through all features:
1. Make sure your server is running
2. Run the example script: `python client/example.py`
