from src.extraction.models import (
    Drug,
    Disease,
    ClinicalTrial,
    Protein,
    Gene,
    Biomarker,
    AdverseEvent,
    PatientPopulation,
    ExtractedDrugProfile,
    ExtractedTrialProfile,
)


class GraphBuilder:

    def __init__(self, source_document: str, chunk_id: str):
        self.source_document = source_document
        self.chunk_id = chunk_id

    @staticmethod
    def make_id(entity_type: str, name: str) -> str:
        normalized = (
            name.strip()
            .upper()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("/", "_")
        )

        return f"{entity_type.upper()}:{normalized}"

    # ---------------------------------------------------------
    # Drug label
    # ---------------------------------------------------------

    def build_drug_profile(
        self,
        profile: ExtractedDrugProfile,
    ):
        nodes = []
        relationships = []

        # -------------------------
        # Drug
        # -------------------------

        drug_id = self.make_id(
            "Drug",
            profile.drug.name
        )

        drug = Drug(
            id=drug_id,
            name=profile.drug.name,
            active_ingredient=profile.drug.active_ingredient,
            drug_class=profile.drug.drug_class,
        )

        nodes.append(drug)

        # -------------------------
        # Proteins
        # -------------------------

        for extracted_protein in profile.inhibits:

            protein_id = self.make_id(
                "Protein",
                extracted_protein.name
            )

            protein = Protein(
                id=protein_id,
                name=extracted_protein.name,
                symbol=extracted_protein.symbol,
            )

            nodes.append(protein)

            relationships.append({
                "source_id": drug_id,
                "target_id": protein_id,
                "type": "INHIBITS",
                "evidence": extracted_protein.evidence,
                "source_document": self.source_document,
                "chunk_id": self.chunk_id,
            })

        # -------------------------
        # Diseases / indications
        # -------------------------

        for extracted_disease in profile.indications:

            disease_id = self.make_id(
                "Disease",
                extracted_disease.name
            )

            disease = Disease(
                id=disease_id,
                name=extracted_disease.name,
            )

            nodes.append(disease)

            # Drug indications are currently represented
            # as Drug -> Disease using TESTED_IN? No.
            #
            # We don't currently have a DRUG -> DISEASE
            # relationship in schema, so we intentionally
            # don't create an edge here.
            #
            # Entity extraction is preserved for now.

        # -------------------------
        # Adverse events
        # -------------------------

        for extracted_event in profile.adverse_events:

            event_id = self.make_id(
                "AdverseEvent",
                extracted_event.name
            )

            event = AdverseEvent(
                id=event_id,
                name=extracted_event.name,
            )

            nodes.append(event)

        return {
            "nodes": nodes,
            "relationships": relationships,
        }

    # ---------------------------------------------------------
    # Clinical trial
    # ---------------------------------------------------------

    def build_trial_profile(
        self,
        profile: ExtractedTrialProfile,
    ):
        nodes = []
        relationships = []

        # -------------------------
        # Clinical Trial
        # -------------------------

        trial_id = self.make_id(
            "ClinicalTrial",
            profile.trial.name
        )

        trial = ClinicalTrial(
            id=trial_id,
            name=profile.trial.name,
            study_type=profile.trial.study_type,
            objective=profile.trial.objective,
            conclusion=profile.trial.conclusion,
        )

        nodes.append(trial)

        # -------------------------
        # Interventions
        # -------------------------

        for extracted_drug in profile.interventions:

            drug_id = self.make_id(
                "Drug",
                extracted_drug.name
            )

            drug = Drug(
                id=drug_id,
                name=extracted_drug.name,
                active_ingredient=extracted_drug.active_ingredient,
                drug_class=extracted_drug.drug_class,
            )

            nodes.append(drug)

            relationships.append({
                "source_id": drug_id,
                "target_id": trial_id,
                "type": "TESTED_IN",
                "evidence": extracted_drug.evidence,
                "source_document": self.source_document,
                "chunk_id": self.chunk_id,
            })

        # -------------------------
        # Diseases
        # -------------------------

        for extracted_disease in profile.diseases:

            disease_id = self.make_id(
                "Disease",
                extracted_disease.name
            )

            disease = Disease(
                id=disease_id,
                name=extracted_disease.name,
            )

            nodes.append(disease)

            relationships.append({
                "source_id": trial_id,
                "target_id": disease_id,
                "type": "STUDIES",
                "evidence": extracted_disease.evidence,
                "source_document": self.source_document,
                "chunk_id": self.chunk_id,
            })

        # -------------------------
        # Biomarkers
        # -------------------------

        for extracted_biomarker in profile.biomarkers:

            biomarker_id = self.make_id(
                "Biomarker",
                extracted_biomarker.name
            )

            biomarker = Biomarker(
                id=biomarker_id,
                name=extracted_biomarker.name,
            )

            nodes.append(biomarker)

            relationships.append({
                "source_id": trial_id,
                "target_id": biomarker_id,
                "type": "HAS_BIOMARKER",
                "evidence": extracted_biomarker.evidence,
                "source_document": self.source_document,
                "chunk_id": self.chunk_id,
            })

        # -------------------------
        # Populations
        # -------------------------

        for extracted_population in profile.populations:

            population_id = self.make_id(
                "PatientPopulation",
                extracted_population.description
            )

            population = PatientPopulation(
                id=population_id,
                description=extracted_population.description,
            )

            nodes.append(population)

            relationships.append({
                "source_id": trial_id,
                "target_id": population_id,
                "type": "HAS_POPULATION",
                "evidence": extracted_population.evidence,
                "source_document": self.source_document,
                "chunk_id": self.chunk_id,
            })

        # -------------------------
        # Adverse Events
        # -------------------------

        for extracted_event in profile.adverse_events:

            event_id = self.make_id(
                "AdverseEvent",
                extracted_event.name
            )

            event = AdverseEvent(
                id=event_id,
                name=extracted_event.name,
            )

            nodes.append(event)

            relationships.append({
                "source_id": trial_id,
                "target_id": event_id,
                "type": "HAS_ADVERSE_EVENT",
                "evidence": extracted_event.evidence,
                "source_document": self.source_document,
                "chunk_id": self.chunk_id,
            })

        return {
            "nodes": nodes,
            "relationships": relationships,
        }
