from pathlib import Path

import chromadb

from .chunker import DocumentChunker
from .embedder import DocumentEmbedder


class VectorStore:

    def __init__(self):

        db_path = Path("vector_store/chroma_db")

        db_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(db_path)
        )

        self.collection = self.client.get_or_create_collection(
            name="fuel_station_documents"
        )

    def index_documents(self):

        chunker = DocumentChunker()

        chunks = chunker.chunk_documents()

        if len(chunks) == 0:

            print("Aucun document trouvé.")

            return

        embedder = DocumentEmbedder()

        embeddings = embedder.embed_chunks(chunks)

        ids = []

        documents = []

        metadatas = []

        for i, chunk in enumerate(chunks):

            ids.append(f"chunk_{i}")

            documents.append(chunk.page_content)

            metadatas.append(chunk.metadata)

        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=embeddings.tolist(),

            metadatas=metadatas

        )

        print()

        print("=" * 50)

        print(f"{len(chunks)} chunks indexés.")

        print(f"Collection : {self.collection.name}")

        print("=" * 50)


if __name__ == "__main__":

    VectorStore().index_documents()