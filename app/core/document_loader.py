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
            
            # Make sure data folder exists
            if not os.path.exists(self.data_folder):
                logger.warning(f"Data folder {self.data_folder} does not exist. Creating it.")
                os.makedirs(self.data_folder, exist_ok=True)
            
            # Check if there are any files
            files = os.listdir(self.data_folder)
            if not files:
                logger.warning("No files found in data folder. Creating a placeholder file.")
                import json
                placeholder_data = {
                    "columns": ["Law Type", "Law Name/Section", "Law Details", "When Applicable", "Legal Reference"],
                    "data": [["Example", "Section 1", "This is an example law", "When relevant", "Legal Code 1"]]
                }
                placeholder_path = os.path.join(self.data_folder, "placeholder_data.json")
                with open(placeholder_path, 'w') as f:
                    json.dump(placeholder_data, f)
                files = ["placeholder_data.json"]
            
            for fname in files:
                fpath = os.path.join(self.data_folder, fname)
                try:
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
                    elif fname.endswith('.json'):
                        import json
                        with open(fpath, 'r') as f:
                            json_data = json.load(f)
                            df = pd.DataFrame(data=json_data.get('data', []), columns=json_data.get('columns', []))
                            all_dfs.append(df)
                except Exception as e:
                    logger.error(f"Error loading file {fname}: {str(e)}")
            
            if not all_dfs:
                # Create a minimal placeholder DataFrame if no data was loaded
                logger.warning("No data could be loaded. Creating a placeholder DataFrame.")
                df = pd.DataFrame({
                    "Law Type": ["Example"], 
                    "Law Name/Section": ["Placeholder Law"],
                    "Law Details": ["This is a placeholder for demonstration purposes."],
                    "When Applicable": ["This is not a real law entry."],
                    "Legal Reference": ["N/A"]
                })
                all_dfs.append(df)
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
