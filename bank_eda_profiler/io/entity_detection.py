import difflib
from typing import List, Tuple, Optional
from ..banking.schemas import SCHEMAS

class EntityDetectionEngine:
    def __init__(self, schemas: Optional[dict] = None):
        """
        Initializes the EntityDetectionEngine with a set of known schemas.
        If no schemas are provided, it uses the default SCHEMAS from banking.schemas.
        """
        self.schemas = schemas if schemas is not None else SCHEMAS

    def detect_entity(self, columns: List[str]) -> Tuple[Optional[str], float]:
        """
        Detects the best matching logical entity for a given list of columns.
        
        Args:
            columns: A list of column names from the dataset.
            
        Returns:
            A tuple containing the (best_match_entity_name, confidence_score).
            confidence_score is between 0.0 and 100.0.
            If no schemas are defined, returns (None, 0.0).
        """
        if not self.schemas:
            return None, 0.0
            
        best_match = None
        highest_score = 0.0
        
        # Convert dataset columns to lowercase for case-insensitive matching
        dataset_cols_lower = [str(c).lower() for c in columns]
        
        for entity_name, schema_cols in self.schemas.items():
            schema_cols_lower = [str(c).lower() for c in schema_cols]
            
            if not schema_cols_lower:
                continue
                
            # Calculate how many schema columns are present in the dataset
            matched_count = 0
            for req_col in schema_cols_lower:
                # Exact match
                if req_col in dataset_cols_lower:
                    matched_count += 1
                else:
                    # Fuzzy match fallback (e.g. "account_id" matches "accountid")
                    matches = difflib.get_close_matches(req_col, dataset_cols_lower, n=1, cutoff=0.85)
                    if matches:
                        matched_count += 1
                        
            # Confidence is the percentage of required schema columns found in the dataset
            confidence = (matched_count / len(schema_cols_lower)) * 100.0
            
            if confidence > highest_score:
                highest_score = confidence
                best_match = entity_name
                
        return best_match, highest_score
