import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


class Neo4jClient:

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        if not self.uri:
            raise ValueError("NEO4J_URI is missing.")

        if not self.username:
            raise ValueError("NEO4J_USERNAME is missing.")

        if not self.password:
            raise ValueError("NEO4J_PASSWORD is missing.")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def verify_connection(self):
        self.driver.verify_connectivity()
        print("Connected to Neo4j successfully.")

    def create_constraints(self):
        constraints = [
            """
            CREATE CONSTRAINT drug_id_unique IF NOT EXISTS
            FOR (n:Drug)
            REQUIRE n.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT disease_id_unique IF NOT EXISTS
            FOR (n:Disease)
            REQUIRE n.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT clinical_trial_id_unique IF NOT EXISTS
            FOR (n:ClinicalTrial)
            REQUIRE n.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT protein_id_unique IF NOT EXISTS
            FOR (n:Protein)
            REQUIRE n.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT gene_id_unique IF NOT EXISTS
            FOR (n:Gene)
            REQUIRE n.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT biomarker_id_unique IF NOT EXISTS
            FOR (n:Biomarker)
            REQUIRE n.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT adverse_event_id_unique IF NOT EXISTS
            FOR (n:AdverseEvent)
            REQUIRE n.id IS UNIQUE
            """,
            """
            CREATE CONSTRAINT population_id_unique IF NOT EXISTS
            FOR (n:PatientPopulation)
            REQUIRE n.id IS UNIQUE
            """,
        ]

        with self.driver.session(database=self.database) as session:
            for constraint in constraints:
                session.run(constraint)

        print("Neo4j constraints created successfully.")

    def load_graph(self, graph):
        """
        Load a GraphBuilder output into Neo4j.

        Expected format:

        {
            "nodes": [...],
            "relationships": [...]
        }
        """

        with self.driver.session(database=self.database) as session:

            # Load nodes
            for node in graph["nodes"]:

                node_type = node.__class__.__name__

                properties = vars(node).copy()

                session.execute_write(
                    self._merge_node,
                    node_type,
                    properties
                )

            # Load relationships
            for relationship in graph["relationships"]:

                session.execute_write(
                    self._merge_relationship,
                    relationship
                )

        print("Graph loaded into Neo4j successfully.")

    @staticmethod
    def _merge_node(tx, node_type, properties):

        allowed_node_types = {
            "Drug",
            "Disease",
            "ClinicalTrial",
            "Protein",
            "Gene",
            "Biomarker",
            "AdverseEvent",
            "PatientPopulation",
            "Outcome",
            "Publication",
        }

        if node_type not in allowed_node_types:
            raise ValueError(
                f"Unsupported node type: {node_type}"
            )

        if "id" not in properties:
            raise ValueError(
                f"Node of type '{node_type}' is missing required 'id': "
                f"{properties}"
            )

        query = f"""
        MERGE (n:{node_type} {{id: $id}})
        SET n += $properties
        """

        tx.run(
            query,
            id=properties["id"],
            properties=properties
        )

    @staticmethod
    def _merge_relationship(tx, relationship):

        allowed_relationship_types = {
            "TESTED_IN",
            "STUDIES",
            "INHIBITS",
            "ENCODED_BY",
            "HAS_BIOMARKER",
            "HAS_OUTCOME",
            "HAS_ADVERSE_EVENT",
            "HAS_POPULATION",
            "REPORTED_IN",
        }

        relationship_type = relationship["type"]

        if relationship_type not in allowed_relationship_types:
            raise ValueError(
                f"Unsupported relationship type: {relationship_type}"
            )

        query = f"""
        MATCH (source {{id: $source_id}})
        MATCH (target {{id: $target_id}})

        MERGE (source)-[r:{relationship_type}]->(target)

        SET r.evidence = $evidence,
            r.source_document = $source_document,
            r.chunk_id = $chunk_id
        """

        tx.run(
            query,
            source_id=relationship["source_id"],
            target_id=relationship["target_id"],
            evidence=relationship.get("evidence"),
            source_document=relationship.get("source_document"),
            chunk_id=relationship.get("chunk_id"),
        )

    def close(self):
        self.driver.close()
