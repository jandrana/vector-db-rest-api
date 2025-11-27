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
app/
├── api/
│   ├── routes/
│   └── deps.py
├── core/
│   ├── config.py
│   └── math_utils.py
├── db/
│   ├── database.py
│   └── models.py
├── schemas/
├── services/
│   ├── index_service.py
│   └── search_service.py
└── main.py
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

## Table of Contents

- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running Instructions](#running-instructions)
- [Documentation](#documentation)
  - [View Documentation](#view-documentation)
  - [Updating the Documentation](#updating-the-documentation)
- [Challenge Approach](#challenge-approach)

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
