# 🧬 Clinical Knowledge Graph

From unstructured clinical documents to a structured, queryable knowledge graph using LLMs, Pydantic, and Neo4j.

Clinical documents contain much more than isolated pieces of information.

A drug label may mention a drug, its active ingredient, indications, molecular targets, and adverse events. A clinical trial may connect drugs to diseases, biomarkers, patient populations, outcomes, and reported adverse events.

Traditional document search can retrieve the relevant text, but it does not explicitly model these relationships.

This project explores how to transform those documents into a Clinical Knowledge Graph where entities and relationships can be queried directly.

<img width="1380" height="741" alt="clinical_graph_neo4j" src="https://github.com/user-attachments/assets/3b5980a7-44fa-4ad7-9144-a41c93d7a0f2" />
