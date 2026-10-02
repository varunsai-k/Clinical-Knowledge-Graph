from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents

from src.extraction.extractor import GraphExtractor
from src.extraction.models import (
    ExtractedDrugProfile,
    ExtractedTrialProfile,
)

from src.graph.builder import GraphBuilder
from src.graph.neo4j_client import Neo4jClient


def main():


    documents = load_documents()
    print(f"\nLoaded {len(documents)} documents.")
    chunks = chunk_documents(
        documents,
        chunk_size=800,
        overlap=100,
    )
    print(f"Created {len(chunks)} chunks.")
    extractor = GraphExtractor()
    neo4j_client = Neo4jClient()

    try:

        neo4j_client.verify_connection()
        neo4j_client.create_constraints()

        for chunk in chunks:

            print("\n" + "=" * 80)
            print(f"DOCUMENT : {chunk.source}")
            print(f"TYPE     : {chunk.document_type}")
            print(f"CHUNK    : {chunk.chunk_id}")
            print("=" * 80)


            extraction = extractor.extract(
                chunk_text=chunk.text,
                document_type=chunk.document_type,
            )

            print("\nExtraction completed.")

            builder = GraphBuilder(
                source_document=chunk.source,
                chunk_id=chunk.chunk_id,
            )

            if isinstance(
                extraction,
                ExtractedDrugProfile
            ):

                graph = builder.build_drug_profile(
                    extraction
                )

            elif isinstance(
                extraction,
                ExtractedTrialProfile
            ):

                graph = builder.build_trial_profile(
                    extraction
                )

            else:

                raise TypeError(
                    f"Unsupported extraction type: "
                    f"{type(extraction)}"
                )

            print(
                f"Nodes extracted       : "
                f"{len(graph['nodes'])}"
            )

            print(
                f"Relationships extracted: "
                f"{len(graph['relationships'])}"
            )
            neo4j_client.load_graph(graph)

            print(
                f"Loaded {chunk.chunk_id} into Neo4j."
            )

    finally:

        neo4j_client.close()

        print("\nNeo4j connection closed.")


if __name__ == "__main__":
    main()
