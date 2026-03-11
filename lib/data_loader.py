import json
from collections.abc import Callable
from datetime import UTC, datetime
from importlib import import_module
from pathlib import Path
from typing import Any

from lib.filer import Filer


class DataLoader:
    """Class to load documents from files, enrich them and post-hoc processing.

    Attributes:
        filer (Filer): Filer instance to handle file operations.
        filetype (str): Type of files to process (e.g., "json").
        parse_fn (Callable): Function to parse file content into a list of documents.
        optional_data (dict): Optional data to enrich documents, structured as a dictionary where keys are document base folders.
    """

    def __init__(self, filer: Filer, filetype: str, parse_fn: Callable) -> None:
        """Initialize DataLoader with filer, filetype and parse function.

        Args:
            filer (Filer): Filer instance to handle file operations.
            filetype (str): Type of files to process (e.g., "json").
            parse_fn (Callable): Function to parse file content into a list of documents.
            optional_data (dict, optional): Optional data to enrich documents.

        Returns:
            None
        """
        self.filer: Filer = filer
        self.filetype: str = filetype
        self.parse_fn: Callable = parse_fn
        self.optional_data: dict[str, Any] = self.get_optional_data_()

    def get_optional_data_(self) -> dict[str, Any]:
        """Get optional data to enrich documents from an optional_data.json file in the current working directory.

        Returns:
            dict: Optional data to enrich documents, structured as a dictionary where keys are document base folders.
        """
        # Get optional data to enrich documents
        optional_data_filepath: Path = self.filer.get_folderpath("cwd") / "optional_data.json" # type: ignore
        # If optional data file exists
        if (optional_data_filepath).exists():
            # open optional data file
            with optional_data_filepath.open() as f_in:
                # load its content as json
                return json.load(f_in)
        # Otherwise
        else:
            # Set it to an empty object
            return {}

    def add_base_data_(self, document: dict, filepath: Path, index: int) -> dict:
        """Add base data to document such as document filename and date.

        Args:
            document (dict): The document to enrich with base data.
            filepath (Path): The path of the file containing the document.
            index (int): The index of the document within the file.

        Returns:
            dict: The enriched document with base data added.
        """
        # Get document_filename or None
        document_filename: str | None = document.get("document_filename")
        # Add document_filename (default to current file name & index)
        document["document_filename"] = document_filename or f"{filepath.stem}_{index}"
        # Get document_date or None
        document_date: str | None = document.get("document_date")
        # Add document_date (default to current date)
        document["document_date"] = (
            document_date or f"{datetime.now(UTC).strftime('%d/%m/%Y')}"
        )

        return document

    def add_optional_data_(self, document: dict) -> dict:
        """Add optional data to document from the optional_data.json file.

        Args:
            document (dict): The document to enrich with optional data.

        Returns:
            dict: The enriched document with optional data added.
        """
        # Get optional data for current document base folder or empty dict
        optional_data: dict[str, Any] = self.optional_data.get(document["document_base_folder"], {})
        # Update document with optional data
        document.update(optional_data)

        return document

    def post_hoc_process_document_(self, document: dict) -> dict:
        """Post-hoc process a document using a custom post_hoc.py module if it exists.

        Args:
            document (dict): The document to process.

        Returns:
            dict: The processed document.
        """
        # Define post_hoc module path
        post_hoc_path: Path = (
            self.filer.get_folderpath("lib_custom")
                / Path(document["document_base_folder"]) / "post_hoc.py" # type: ignore
        )
        # If post_hoc module is present
        if post_hoc_path.exists():
            # Define module name
            module_name: str = (
                ".".join([
                    "lib",
                    "custom",
                    *document["document_base_folder"].split("/"),
                    "post_hoc"
                ])
            )
            # Importing module
            module: Any = import_module(module_name)
            # Get post_hoc function
            process_data_fn: Callable[[dict[str, Any]], dict[str, Any]] = module.process_data
            # Invoke post_hoc function
            document = process_data_fn(document)

        return document

    def load_documents(self) -> list[dict]:
        """Load documents from files to process, enrich them with base and optional data, and apply post-hoc processing.

        Returns:
            list[dict]: A list of processed and enriched documents.
        """
        # Init documents list
        documents_list: list[dict[str, Any]] = []
        # Loop through files to process
        for filepath in self.filer.get_files_to_process(self.filetype): # type: ignore
            # Open current file
            with filepath.open() as f_in:
                # Parse its content (will contain list of documents)
                documents: list[dict[str, Any]] = self.parse_fn(f_in)
                # Loop through documents
                for index, document in enumerate(documents, 1):
                    # If current document's template specification is valid
                    if self.filer.get_template_filepath(document, "html").exists():
                        # Add base data
                        document: dict[str, Any] = self.add_base_data_(document, filepath, index)
                        # Add optional data
                        document = self.add_optional_data_(document)
                        # Add post-process data
                        document = self.post_hoc_process_document_(document)
                        # Append document to documents list
                        documents_list.append(document)
                    # Otherwise
                    else:
                        # Notify
                        print(f"Template for {filepath} document with index {index} was not found.")  # noqa: T201

        return documents_list
