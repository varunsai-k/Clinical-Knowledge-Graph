from src.config.schema import (
    NODE_TYPES,
    RELATIONSHIPS
)


def build_extraction_prompt(
    chunk_text: str,
    document_type: str
) -> str:

    entity_types = "\n".join(
        f"- {name}: {definition['description']}"
        for name, definition in NODE_TYPES.items()
    )

    relationship_types = "\n".join(
        f"- {name}: "
        f"{definition['source']} -> "
        f"{definition['target']}"
        for name, definition in RELATIONSHIPS.items()
    )

    base_rules = f"""
You are a clinical knowledge graph extraction system.

Extract structured clinical information from the
provided document chunk.

Only extract information explicitly supported
by the text.

Do NOT infer medical facts.

Do NOT invent entities.

Do NOT invent facts that are not present.

========================
ALLOWED ENTITY TYPES
========================

{entity_types}

========================
ALLOWED RELATIONSHIPS
========================

{relationship_types}

========================
GENERAL RULES
========================

1. Preserve terminology from the source.

2. Only extract explicitly stated information.

3. Do not infer relationships.

4. Do not infer diseases, drugs, proteins,
   biomarkers, or adverse events.

5. If information is not present, return an
   empty list or null.

6. Evidence must come directly from the
   provided text.

"""

    if document_type == "drug_label":

        return base_rules + """

========================
DOCUMENT TYPE
========================

DRUG LABEL

========================
EXTRACTION TASK
========================

Extract:

1. Drug information
   - name
   - active ingredient
   - drug class

2. Molecular targets
   - proteins explicitly targeted or inhibited

3. Indications
   - diseases or clinical conditions explicitly
     associated with the drug

4. Adverse events
   - adverse events explicitly mentioned

========================
TEXT
========================

""" + chunk_text

    if document_type == "clinical_trial":

        return base_rules + """

========================
DOCUMENT TYPE
========================

CLINICAL TRIAL

========================
EXTRACTION TASK
========================

Extract:

1. Clinical trial
   - name
   - study type
   - objective
   - conclusion

2. Interventions
   - drugs or interventions used

3. Diseases
   - diseases or conditions studied

4. Biomarkers
   - biomarkers measured or evaluated

5. Patient populations
   - study population explicitly described

6. Adverse events
   - adverse events reported

========================
TEXT
========================

""" + chunk_text

    raise ValueError(
        f"Unsupported document type: {document_type}"
    )
