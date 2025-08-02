import pandas as pd
import logging
from typing import List, Dict, Any
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentLoader:
    """Handles loading and preprocessing of police legal document data from all files in the data folder."""
    
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        
    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Load documents from all Excel and CSV files in the data folder and convert them to a format suitable for processing.
        """
        try:
            logger.info(f"Loading documents from all files in {self.data_folder}")
            all_dfs = []
            for fname in os.listdir(self.data_folder):
                fpath = os.path.join(self.data_folder, fname)
                if fname.endswith('.xlsx'):
                    df = pd.read_excel(fpath)
                    all_dfs.append(df)
                elif fname.endswith('.csv'):
                    try:
                        df = pd.read_csv(fpath, on_bad_lines='warn')  # pandas >=1.3
                        all_dfs.append(df)
                    except TypeError:
                        # For older pandas
                        df = pd.read_csv(fpath, error_bad_lines=False)
                        all_dfs.append(df)
            if not all_dfs:
                raise ValueError("No data files found in the data folder.")
            df = pd.concat(all_dfs, ignore_index=True)
            # Normalize column names for downstream code
            df.columns = [c.strip() for c in df.columns]
            # Convert DataFrame to list of dictionaries
            documents = []
            for _, row in df.iterrows():
                summary = str(
                    row.get("Law Summary")
                    or row.get("Law Details")
                    or row.get("summary")
                    or row.get("details")
                    or "Information not available."
                )
                when_applicable = str(
                    row.get("Applicability")
                    or row.get("When Applicable")
                    or row.get("when_applicable")
                    or "Information not available."
                )
                law_category = (
                    row.get("Law Category")
                    or row.get("Law Type")
                    or row.get("Category")
                    or ""
                )
                law_name = (
                    row.get("Law Name / Code")
                    or row.get("Law Name/Section")
                    or row.get("Law Name")
                    or row.get("Section")
                    or ""
                )
                details = (
                    row.get("Law Details")
                    or row.get("details")
                    or ""
                )
                whom_to_approach = (
                    row.get("Whom to Approach")
                    or row.get("Contact Person")
                    or ""
                )
                historical_context = (
                    row.get("Historical Context")
                    or row.get("Context")
                    or ""
                )
                example_cases = (
                    row.get("Real-life Example")
                    or row.get("Example Use Cases")
                    or row.get("Examples")
                    or ""
                )
                doc = {
                    "law_category": str(law_category),
                    "law_name": str(law_name),
                    "summary": summary,
                    "details": str(details),
                    "when_applicable": when_applicable,
                    "whom_to_approach": str(whom_to_approach),
                    "historical_context": str(historical_context),
                    "example_cases": str(example_cases)
                }
                # Create a combined text field for embedding
                doc["combined_text"] = f"""
                Category: {doc['law_category']}
                Law: {doc['law_name']}
                Details: {doc['details']}
                Summary: {doc['summary']}
                When Applicable: {doc['when_applicable']}
                Whom to Approach: {doc['whom_to_approach']}
                Historical Context: {doc['historical_context']}
                Examples: {doc['example_cases']}
                """.strip()
                documents.append(doc)
            logger.info(f"Successfully loaded {len(documents)} documents from all files.")
            return documents
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise
