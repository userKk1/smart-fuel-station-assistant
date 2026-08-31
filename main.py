from simulator.LLM.generate_complaints import generate_complaint
from simulator.LLM.generate_maintenance_reports import generate_maintenance_reports
from simulator.simulation_engine import SimulationEngine
from simulator.stations import StationGenerator
from simulator.pumps import PumpGenerator
from simulator.inventory import InventoryGenerator
from ETL.pipeline import run_pipeline
from RAG.chunker import DocumentChunker
from RAG.embedder import DocumentEmbedder
from RAG.vector_store import VectorStore

if __name__ == "__main__":

    StationGenerator().save()

    PumpGenerator().save()

    InventoryGenerator().save()

    engine = SimulationEngine()

    engine.run()

    generate_complaint()
    generate_maintenance_reports()

    run_pipeline()

    chunker = DocumentChunker()
    chunks = chunker.chunk_documents()

    embedder = DocumentEmbedder()
    embeddings = embedder.embed_chunks(chunks)

    VectorStore().index_documents()