from pathlib import Path
from typing import Any

from weasyprint import HTML

from lib import LIB_CUSTOM_PATH, jinja_env
from lib.data_loader import DataLoader
from lib.filer import Filer


class Renderer:
    """Class to render documents using Jinja templates and WeasyPrint.

    Attributes:
        filer (Filer): Filer instance to handle file operations.
        data_loader (DataLoader): DataLoader instance to load documents.
    """

    def __init__(self, filer: Filer, data_loader: DataLoader):
        """Initialize Renderer with filer and data_loader.

        Args:
            filer (Filer): Filer instance to handle file operations.
            data_loader (DataLoader): DataLoader instance to load documents.

        Returns:
            None
        """

        self.filer: Filer = filer
        self.data_loader: DataLoader = data_loader

    def render_documents(self) -> None:
        """Render documents using Jinja templates and WeasyPrint.
        Returns:
            None
        """
        # Get documents to render
        documents_to_render: list[dict[str, Any]] = self.data_loader.load_documents()

        # Loop through documents to render
        for no_document, document in enumerate(documents_to_render, 1):

            # Notify number of documents to render
            print(no_document, " documents were rendered out of", len(documents_to_render), end="\r", flush=True)  # noqa: T201

            # Determine jinja template to load
            template_to_get: Path = self.filer.get_template_filepath(document, "html").relative_to(LIB_CUSTOM_PATH)

            # Load jinja template
            jinja_template: Any = jinja_env.get_template(str(template_to_get))

            # Render jinja template with current document
            rendered_template: str = jinja_template.render(document)

            # Determine output filepath
            output_filepath: Path = self.filer.get_folderpath("xerox") / f"{document['document_filename']}.pdf" # type: ignore

            # Write rendered jinja template to output filepath
            HTML(string=rendered_template).write_pdf(output_filepath)

        # Notify end of rendering
        print("Rendering job is done.", len(documents_to_render), "processed document(s).")  # noqa: T201
