import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from src.extraction.models import (
    ExtractedDrugProfile,
    ExtractedTrialProfile
)

from src.extraction.prompt import (
    build_extraction_prompt
)


load_dotenv()


class GraphExtractor:

    def __init__(self):

        api_key = os.getenv(
            "GOOGLE_API_KEY"
        )

        if not api_key:
            #print("API_KEY",api_key)
            raise ValueError(
                "GOOGLE_API_KEY is missing."
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            temperature=0
        )

    def extract(
        self,
        chunk_text: str,
        document_type: str
    ):

        prompt = build_extraction_prompt(
            chunk_text=chunk_text,
            document_type=document_type
        )

        if document_type == "drug_label":

            structured_llm = (
                self.llm.with_structured_output(
                    ExtractedDrugProfile
                )
            )

        elif document_type == "clinical_trial":

            structured_llm = (
                self.llm.with_structured_output(
                    ExtractedTrialProfile
                )
            )

        else:

            raise ValueError(
                f"Unsupported document type: "
                f"{document_type}"
            )

        return structured_llm.invoke(
            prompt
        )
