import logging
import sys
import requests
from sdk import Client


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def example():
    logger.info("Initializing client...")
    client = Client()

    try:
        logger.info("Creating library 'Test Library'...")
        library = client.create_library("Test Library")
        logger.info(f"Library created: {library['id']}")

        logger.info("Creating document 'Test Document'...")
        document = client.create_document(123, "Test Document")
        logger.info(f"Document created: {document['id']}")

        chunks = [
            "Python is a popular programming language for Data Science",
            "The Eiffel Tower is located in Paris, France",
            "Pizza is a savory dish of Italian origin",
            "France is a country in Europe",
        ]

        logger.info("Creating chunks...")
        for chunk in chunks:
            client.create_chunk(document["id"], chunk)
        logger.info(f"{len(chunks)} chunks created")

        logger.info("Indexing library...")
        res = client.index_library(library["id"])
        logger.info(f"Library indexed: {res['message']}")

        query = "coding"
        logger.info(f"Semantic search for: {query}")
        results = client.search_library(library["id"], query, k=4, search_type="knn")
        for result in results:
            logger.info(f"Result: {result['chunk']['text']} (Score: {result['score']})")

        query = "Paris, France"
        logger.info(f"Keyword search for: {query}")
        results = client.search_library(
            library["id"], query, k=3, search_type="keyword"
        )
        for result in results:
            logger.info(
                f"Result: {result['chunk']['text']} (Match score: {result['score']})"
            )

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    example()
