"""Loader that loads DayOne json dump"""
from typing import List
import json

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader

class DayOneFileLoader(BaseLoader):
    def __init__(self, path: str, encoding: str = "UTF-8"):
        """ Initialize with path. """
        self.file_path = path
        self.encoding = encoding

    def load(self) -> List[Document]:
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            data = json.load(f)
        
        documents = []
        for entry in data["entries"]:
            metadata = {
                "creationDate": entry["creationDate"],
                "modifiedDate": entry["modifiedDate"],
                "location": entry.get("location", {}).get("placeName"),
                "creationDevice": entry["creationDevice"],
                "editingTime": entry["editingTime"]
            }
            documents.append(
                Document(page_content=entry["text"], metadata=metadata)
            )
        return documents