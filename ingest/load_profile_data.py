#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain.schema import Document
from load_mongo_data import generate_profiles
from preprocess_profile_data import preprocess_profile
from langchain.document_loaders.base import BaseLoader
from typing import List, Generator, Dict


class CustomLoader(BaseLoader):
    """
    Custom loader for processing profiles and creating Document instances for
    langchain.

    Args:
        profile_generator (Generator[Dict, None, None]): Generator producing
        profile dictionaries.

    Attributes:
        profiles (Generator[Dict, None, None]): Generator producing profile
         dictionaries.

    Methods:
        lazy_load(): Lazy loading method to generate Documents with metadata
            and preprocessed content.
        load(): Eager loading method to load all Documents.
    """
    def __init__(self, profile_generator: Generator[Dict, None, None]):
        self.profiles = profile_generator

    def lazy_load(self) -> Generator[Document, None, None]:
        """
        Generate Document instances lazily from profiles.

        Yields:
            Document: A Document instance with page content and metadata.
        """
        for profile in self.profiles:
            metadata = {
                "source": profile["shorthandSymbol"],
                "name": profile["name"]
                }
            page_content = preprocess_profile(profile["raw_data"])
            yield Document(page_content=page_content, metadata=metadata)

    def load(self) -> List[Document]:
        """
        Load all Document instances eagerly.

        Returns:
            List[Document]: List of Document instances.
        """
        return list(self.lazy_load())


# Example usage (also exportable)
loader = CustomLoader(generate_profiles())
