NODE_TYPES = {
    "Drug": {
        "description": (
            "A pharmaceutical drug or active ingredient."
        )
    },

    "Disease": {
        "description": (
            "A disease, disorder, condition, "
            "or clinical indication."
        )
    },

    "ClinicalTrial": {
        "description": (
            "A clinical study or clinical trial."
        )
    },

    "Protein": {
        "description": (
            "A protein or molecular target."
        )
    },

    "Gene": {
        "description": (
            "A gene associated with a protein or disease."
        )
    },

    "Biomarker": {
        "description": (
            "A measurable biological marker."
        )
    },

    "Outcome": {
        "description": (
            "A reported clinical or biological study outcome."
        )
    },

    "AdverseEvent": {
        "description": (
            "An adverse event or undesirable clinical effect."
        )
    },

    "PatientPopulation": {
        "description": (
            "The patient population participating in a study."
        )
    },

    "Publication": {
        "description": (
            "A scientific publication or source document."
        )
    }
}


RELATIONSHIPS = {
    "TESTED_IN": {
        "source": "Drug",
        "target": "ClinicalTrial"
    },

    "STUDIES": {
        "source": "ClinicalTrial",
        "target": "Disease"
    },

    "INHIBITS": {
        "source": "Drug",
        "target": "Protein"
    },

    "ENCODED_BY": {
        "source": "Protein",
        "target": "Gene"
    },

    "HAS_BIOMARKER": {
        "source": "ClinicalTrial",
        "target": "Biomarker"
    },

    "HAS_OUTCOME": {
        "source": "ClinicalTrial",
        "target": "Outcome"
    },

    "HAS_ADVERSE_EVENT": {
        "source": "ClinicalTrial",
        "target": "AdverseEvent"
    },

    "HAS_POPULATION": {
        "source": "ClinicalTrial",
        "target": "PatientPopulation"
    },

    "REPORTED_IN": {
        "source": "ClinicalTrial",
        "target": "Publication"
    }
}
