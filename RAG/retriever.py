import chromadb
from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="vector_store/chroma_db"
        )

        self.collection = self.client.get_collection(
            "fuel_station_documents"
        )

        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def search(self, query, k=5):

        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        )

        results = self.collection.query(

            query_embeddings=[query_embedding.tolist()],

            n_results=k

        )

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append({

                "text": document,

                "metadata": metadata,

                "distance": distance

            })

        return retrieved_chunks

    def build_context(self, query, k=5):

        results = self.search(query, k)

        context = ""

        for result in results:

            context += (
                f"[{result['metadata']['document_type']}]\n"
                f"{result['text']}\n\n"
        )

        return context


if __name__ == "__main__":

    retriever = Retriever()

    question = input("Question : ")

    results = retriever.search(question)

    print()

    print("=" * 60)

    for i, result in enumerate(results, start=1):

        print(f"Résultat {i}")

        print("Distance :", round(result["distance"], 4))

        print("Metadata :", result["metadata"])

        print()

        print(result["text"])

        print("-" * 60)