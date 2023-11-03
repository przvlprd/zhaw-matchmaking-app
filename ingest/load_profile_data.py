from langchain.schema import Document
from load_mongo_data import generate_profiles
from preprocess_profile_data import preprocess_profile
from langchain.document_loaders.base import BaseLoader


class CustomLoader(BaseLoader):
    def __init__(self, profile_generator):
        self.profiles = profile_generator

    def lazy_load(self):
        for profile in self.profiles:
            metadata = {
                "source": profile["shorthandSymbol"],
                "name": profile["name"]
                }
            page_content = preprocess_profile(profile["raw_data"])
            yield Document(page_content=page_content, metadata=metadata)

    def load(self):
        return list(self.lazy_load())


loader = CustomLoader(generate_profiles())
