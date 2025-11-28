from sdk import Client


def example():
    print("Initializing client...\n")
    client = Client()

    try:
        print("Creating library 'Test Library'...")
        library = client.create_library("Test Library")
        print(f"  --> Library created: {library['id']}\n")

        print("Creating document 'Test Document'...")
        document = client.create_document(library["id"], "Test Document")
        print(f"  --> Document created: {document['id']}\n")

        chunks = [
            "Python is a popular programming language for Data Science",
            "The Eiffel Tower is located in Paris, France",
            "Pizza is a savory dish of Italian origin",
            "France is a country in Europe",
        ]

        print("Creating chunks...")
        for chunk in chunks:
            client.create_chunk(document["id"], chunk)
        print(f"  --> {len(chunks)} chunks created\n")

        print("Indexing library...")
        res = client.index_library(library["id"])
        print(f"  --> Library indexed: {res['message']}\n")

        query = "coding"
        print(f"Semantic search for: {query}")
        results = client.search_library(library["id"], query, k=4, search_type="knn")
        for result in results:
            print(f"  --> {result['chunk']['text']} (Score: {result['score']})")

        query = "Paris, France"
        print(f"\nKeyword search for: {query}")
        results = client.search_library(
            library["id"], query, k=3, search_type="keyword"
        )
        for result in results:
            print(f"  --> {result['chunk']['text']} (Match score: {result['score']})")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    example()
