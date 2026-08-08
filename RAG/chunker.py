from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentChunker:

    def __init__(self):

        self.documents_folder = Path("simulator/LLM/documents")

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=500,

            chunk_overlap=100,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]

        )

    def load_documents(self):

        documents = []

        folders = {

            "complaint": self.documents_folder / "complaints",

            "maintenance": self.documents_folder / "maintenance"

        }

        for document_type, folder in folders.items():

            if not folder.exists():
                continue

            for file in folder.glob("*.txt"):

                with open(file, "r", encoding="utf-8") as f:

                    text = f.read()

                document = Document(

                    page_content=text,

                    metadata={

                        "document_type": document_type,

                        "document_id": file.stem,

                        "source": str(file)

                    }

                )

                documents.append(document)

        return documents

    def chunk_documents(self):

        documents = self.load_documents()

        chunks = self.splitter.split_documents(documents)

        print(f"{len(documents)} documents chargés.")

        print(f"{len(chunks)} chunks créés.")

        return chunks


if __name__ == "__main__":

    chunker = DocumentChunker()

    chunks = chunker.chunk_documents()

    print()

    print(chunks[0].metadata)

    print()

    print(chunks[0].page_content)