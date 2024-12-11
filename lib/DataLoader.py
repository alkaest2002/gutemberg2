import json

from typing import Callable
from datetime import datetime
from pathlib import Path
from importlib import import_module
from lib.Filer import Filer

class DataLoader(object):

    def __init__(self, filer: Filer, filetype: str, parse_fn: Callable) -> None:
        self.filer = filer
        self.filetype = filetype
        self.parse_fn = parse_fn
        self.optional_data = self.get_optional_data()

    def get_optional_data(self) -> dict:
        # get optional data to enrich documents
        optional_data_filepath = self.filer.get_folderpath("cwd") / "optional_data.json" # type: ignore
        # if optional data file exixts
        if (optional_data_filepath).exists():
            # open optional data file
            with optional_data_filepath.open() as f_in:
                # load its content as json
                return json.load(f_in)
        # otherwise
        else:
            # set it to an empty object
            return {}

    def add_base_data(self, document: dict, filepath: Path, index: int) -> dict:
        # get document_filename or None
        document_filename = document.get("document_filename", None)
        # add document_filename (default to current file name & index)
        document["document_filename"] = document_filename or f"{filepath.stem}_{index}"
        # get document_date or None
        document_date = document.get("document_date", None)
        # add document_date (default to current date)
        document["document_date"] = document_date or f"{datetime.now().strftime('%d/%m/%Y')}"
        # return document
        return document

    def add_optional_data(self, document: dict) -> dict:
        # update document with optional data
        document.update(self.optional_data.get(document["document_base_folder"], {}))
        # return document
        return document

    def post_hoc_process_document(self, document: dict) -> dict:
        # define post_hoc module path
        post_hoc_path = self.filer.get_folderpath("lib_custom") / Path(document["document_base_folder"]) / "post_hoc.py" # type: ignore
        # if post_hoc module is present
        if post_hoc_path.exists():
            # define module name
            module_name = ".".join(["lib", "custom", *document["document_base_folder"].split("/"), "post_hoc"])
            # import module
            module = import_module(module_name)
            # get post_hoc function
            process_data_fn = getattr(module, "process_data")
            # invoke post_hoc function
            document = process_data_fn(document)
        # return document
        return document

    def load_documents(self) -> list[dict]:
        # init documents list
        documents_list = []
        # loop through files to process
        for filepath in self.filer.get_files_to_process(self.filetype): # type: ignore
            # open current file
            with filepath.open() as f_in:
                # parse its content (will contain list of documents)
                documents = self.parse_fn(f_in)
                # loop through documents
                for index, document in enumerate(documents, 1):
                    # if current document's template specification is valid
                    if self.filer.get_template_filepath(document, "html").exists():
                        # add base data
                        document = self.add_base_data(document, filepath, index)
                        # add optional data
                        document = self.add_optional_data(document)
                        # add post-process data
                        document = self.post_hoc_process_document(document)
                        # append document to documents list
                        documents_list.append(document)
                    # otherwise
                    else:
                        # notify
                        print(f"Template for {filepath} document with index {index} was not found.")
        # return documents list
        return documents_list
