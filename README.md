# Vector DB REST API

A containerized REST API for indexing and querying documents using a vector database.

It allows users to create libraries, upload text documents, and perform both Semantic Vector Search and Exact Keyword Search through different indexing algorithms.

## ✨ Features

*   **Hybrid Search:** Supports both **k-NN Vector Search** (Semantic) and **Inverted Index Search** (Keyword).
*   **Thread-Safe DB:** In-Memory database implementation using `RLock` to prevent data races and deadlocks.
*   **Layered Architecture:** Strict separation of concerns (API -> Services -> Data Layer).
*   **Dockerized:** Project containerization with Docker.
*   **Setup:** Automated setup via `Makefile`.

## 📁 Project Structure

Following a Domain Driven Design inspired structure, separating the code in different logical layers.

```text
vector-db-rest-api/
├── app/
│   ├── api/                  # 🗣️ Interface
│   │   ├── routes/           # API Endpoints
│   │   └── deps.py           # Dependency Injection (get_db)
│   ├── core/                 # ⚙️ Core Utilities
│   │   ├── config.py         # Environment Configuration
│   │   └── math_utils.py     # Cosine Similarity Logic
│   ├── db/                   # 💾 Data Layer
│   │   ├── database.py       # Main Database Controller (Thread-safe)
│   │   ├── inverted_index.py # Keyword Search Algorithm Logic
│   │   ├── persistence.py    # Append-Only Log Logic (File I/O)
│   │   └── models.py         # Internal Data Models
│   ├── schemas/              # 📋 Data Transfer Objects (DTOs)
│   │   └── ...               # Pydantic Schemas for Validation
│   ├── services/             # 🧠 Business Logic Layer
│   │   ├── index_service.py  # Cohere Embedding Integration
│   │   └── search_service.py # Search Orchestration
│   └── main.py               # 🏁 Application Entry Point
├── client/                   # 📦 Python SDK Client
│   ├── sdk.py                # Reusable API Client Library
│   └── example.py            # SDK Usage Demo Script
├── tests/                    # 🧪 Integration Tests
├── Makefile                  # 🛠️ Automation Commands
├── Dockerfile                # 🐳 Docker Configuration
└── requirements.txt          # 🐍 Dependencies
```

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

## 💾 Persistence to Disk (Bonus)

To ensure data durability across container restarts, I implemented an **Append-Only Log (AOL)** persistence mechanism for the In-Memory Database.

### Design Choices
*   **Mechanism:**. Pivoted from snapshotting the entire database state to disk on every change (which would be $O(N)$) to implementing an AOL mechanism, where the system appends each operation as a single JSON line to `vector_db.jsonl`.
*   **Performance:** AOL improves performance significantly since it only writes a single line ( instantaneous regardless of database size) without making a complete snapshot every time.
*   **Recovery:** On startup, the system reads the log file line-by-line and "replays" the events to rebuild the in-memory state.

### Tradeoffs
*   **Pros:** High write performance, human-readable data format, crash recovery.
*   **Cons:** Startup time grows linearly with the number of historical operations (since the whole log must be replayed).

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
