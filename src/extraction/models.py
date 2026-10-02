from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# 1. CANONICAL GRAPH NODE MODELS
# ============================================================

@dataclass
class Drug:
    id: str
    name: str
    active_ingredient: Optional[str] = None
    drug_class: list[str] = field(default_factory=list)


@dataclass
class Disease:
    id: str
    name: str


@dataclass
class ClinicalTrial:
    id: str
    name: str
    study_type: Optional[str] = None
    objective: Optional[str] = None
    conclusion: Optional[str] = None


@dataclass
class Protein:
    id: str
    name: str
    symbol: Optional[str] = None


@dataclass
class Gene:
    id: str
    name: str
    symbol: Optional[str] = None


@dataclass
class Biomarker:
    id: str
    name: str


@dataclass
class AdverseEvent:
    id: str
    name: str


@dataclass
class PatientPopulation:
    id: str
    description: str


# ============================================================
# 2. RELATIONSHIP MODELS
# ============================================================

@dataclass
class TestedInRel:
    evidence: str
    source_document: str
    chunk_id: str


@dataclass
class StudiesRel:
    evidence: str
    source_document: str
    chunk_id: str


@dataclass
class InhibitsRel:
    evidence: str
    source_document: str
    chunk_id: str


@dataclass
class EncodedByRel:
    evidence: str
    source_document: str
    chunk_id: str


@dataclass
class HasBiomarkerRel:
    evidence: str
    source_document: str
    chunk_id: str


@dataclass
class HasAdverseEventRel:
    evidence: str
    source_document: str
    chunk_id: str


@dataclass
class HasPopulationRel:
    evidence: str
    source_document: str
    chunk_id: str


@dataclass
class HasOutcomeRel:
    evidence: str
    source_document: str
    chunk_id: str


# ============================================================
# 3. LLM EXTRACTION MODELS
# ============================================================

class ExtractedDrug(BaseModel):

    name: str = Field(
        description="Drug name exactly as mentioned in the source."
    )

    active_ingredient: Optional[str] = Field(
        default=None,
        description="Active ingredient if explicitly stated."
    )

    drug_class: list[str] = Field(
        default_factory=list,
        description="Drug classes explicitly stated in the source."
    )

    evidence: str = Field(
            description=(
                "Exact supporting text from the source."
            )
        )


class ExtractedDisease(BaseModel):

    name: str = Field(
        description="Disease or condition explicitly mentioned."
    )

    evidence: str = Field(
        description=(
            "Exact supporting text from the source."
        )
    )

class ExtractedProtein(BaseModel):

    name: str = Field(
        description="Protein name exactly as mentioned."
    )

    symbol: Optional[str] = Field(
        default=None,
        description="Protein symbol if explicitly stated."
    )

    evidence: str = Field(
        description=(
            "Exact supporting text from the source."
        )
    )

class ExtractedGene(BaseModel):

    name: str = Field(
        description="Gene name exactly as mentioned."
    )

    symbol: Optional[str] = Field(
        default=None,
        description="Gene symbol if explicitly stated."
    )

    evidence: str = Field(
            description=(
                "Exact supporting text from the source."
            )
        )


class ExtractedBiomarker(BaseModel):

    name: str = Field(
        description="Biomarker explicitly mentioned in the source."
    )

    evidence: str = Field(
            description=(
                "Exact supporting text from the source."
            )
        )


class ExtractedAdverseEvent(BaseModel):

    name: str = Field(
        description="Adverse event explicitly mentioned."
    )

    evidence: str = Field(
            description=(
                "Exact supporting text from the source."
            )
        )


class ExtractedPopulation(BaseModel):

    description: str = Field(
        description="Description of the study population."
    )

    evidence: str = Field(
            description=(
                "Exact supporting text from the source."
            )
        )


# ============================================================
# 4. DRUG LABEL EXTRACTION
# ============================================================

class ExtractedDrugProfile(BaseModel):

    drug: ExtractedDrug

    inhibits: list[ExtractedProtein] = Field(
        default_factory=list,
        description="Proteins explicitly targeted or inhibited by the drug."
    )

    indications: list[ExtractedDisease] = Field(
        default_factory=list,
        description="Diseases or conditions explicitly indicated."
    )

    adverse_events: list[ExtractedAdverseEvent] = Field(
        default_factory=list,
        description="Adverse events explicitly reported."
    )


# ============================================================
# 5. CLINICAL TRIAL EXTRACTION
# ============================================================

class ExtractedClinicalTrial(BaseModel):

    name: str = Field(
        description="Clinical trial or study name."
    )

    study_type: Optional[str] = Field(
        default=None,
        description="Study type such as randomized clinical trial."
    )

    objective: Optional[str] = Field(
        default=None,
        description="Study objective explicitly stated."
    )

    conclusion: Optional[str] = Field(
        default=None,
        description="Study conclusion explicitly stated."
    )

    evidence: str = Field(
        description=(
            "Exact supporting text from the source "
            "for the clinical trial."
        )
    )


class ExtractedTrialProfile(BaseModel):

    trial: ExtractedClinicalTrial

    interventions: list[ExtractedDrug] = Field(
        default_factory=list,
        description="Drugs or interventions used in the trial."
    )

    diseases: list[ExtractedDisease] = Field(
        default_factory=list,
        description="Diseases or conditions studied by the trial."
    )

    biomarkers: list[ExtractedBiomarker] = Field(
        default_factory=list,
        description="Biomarkers measured in the trial."
    )

    populations: list[ExtractedPopulation] = Field(
        default_factory=list,
        description="Study populations explicitly described."
    )

    adverse_events: list[ExtractedAdverseEvent] = Field(
        default_factory=list,
        description="Adverse events reported by the study."
    )
