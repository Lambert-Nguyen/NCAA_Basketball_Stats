# queries/base.py
from typing import Dict, Any

class BaseQuery:
    def __init__(self):
        self.query = ""
       

    def build_query(self) -> None:
        """Child classes must implement this method"""
        raise NotImplementedError("Subclasses must implement build_query()")

    def get_query(self) -> str:
        """Returns the finalized SQL query"""
        return self.query.strip()

   