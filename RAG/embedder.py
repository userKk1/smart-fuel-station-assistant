from sentence_transformers import SentenceTransformer


class DocumentEmbedder:

    def __init__(self):

        print("Chargement du modèle d'embeddings...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Modèle chargé.")

    def embed_chunks(self, chunks):

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = self.model.encode(

            texts,

            show_progress_bar=True,

            convert_to_numpy=True

        )

        print(f"\n{len(embeddings)} embeddings générés.")

        return embeddings


if __name__ == "__main__":

    from chunker import DocumentChunker

    chunker = DocumentChunker()

    chunks = chunker.chunk_documents()

    embedder = DocumentEmbedder()

    embeddings = embedder.embed_chunks(chunks)

    print()

    print("Dimension d'un embedding :", embeddings.shape)

    print()

    print("Premier vecteur :")

    print(embeddings[0][:10])