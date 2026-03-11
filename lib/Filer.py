import shutil
from datetime import UTC, datetime
from pathlib import Path

from lib import LIB_BASE_PATH, LIB_CUSTOM_PATH, LIB_PATH
from lib.errors import NotFoundError


class Filer:
    """Class to handle file operations such as retrieving folder paths, cloning template files and getting files to process.

    Attributes:
        folderpaths (dict): A dictionary containing relevant folder paths.
    """

    def __init__(self) -> None:
        """Initialize Filer and set folder paths."""
        self.folderpaths: dict = self.set_folderpaths_()

    def set_folderpaths_(self):
        """Define and ensure existence of relevant folder paths.

        Returns:
            dict: A dictionary containing relevant folder paths.

        Raises:
                NotFoundError: If any of the required folder paths do not exist.
        """
        # Define relevant paths
        folder_paths = {
            "cwd": Path.cwd(),
            "data" : Path("./data"),
            "xerox" : Path("./xerox"),
            "lib" : LIB_PATH,
            "lib_base": LIB_BASE_PATH,
            "lib_custom": LIB_CUSTOM_PATH
        }
        # Ensure all relevant paths exist
        if all(f.exists() for f in folder_paths.values()):
            # Return relevant paths
            return folder_paths
        # Raise error, otherwise
        raise NotFoundError(f"Missing paths: {[ str(p) for p in folder_paths.values() if not p.exists() ]}.")

    def get_folderpath(self, folder_path: str = "all") -> Path | dict[str, Path]:
        """Get a specific folder path or all folder paths.

        Args:
            folder_path (str, optional): The key of the folder path to retrieve. Defaults to "all".

        Returns:
            Path | dict[str, Path]: The requested folder path or all folder paths.

        Raises:
            NotFoundError: If the requested folder path does not exist.
        """
        # User requests all paths
        if folder_path == "all":
            return self.folderpaths
        # User requests specific path
        if folder_path in self.folderpaths:
            return self.folderpaths[folder_path]
        # Raise error, if user requests invalid path
        raise NotFoundError(f"'{folder_path}' doesn't exist.")

    def get_template_filepath(self, document: dict, filetype: str) -> Path:
        """Get the template filepath for a given document and filetype.

        Args:
            document (dict): The document for which to get the template filepath. Must contain a "document_base_folder" key.
            filetype (str): The filetype for which to get the template filepath (e.g., "json", "yaml", "html").

        Returns:
            Path: The template filepath for the given document and filetype.
        """
        # Unpack area and template
        base_folder, base_template = document["document_base_folder"].split("/")
        # If filetype is html
        if filetype == "html":
            # Return html template filepath
            return (self.folderpaths["lib_custom"] / base_folder / base_template / f"{
                document.get('jinja_template', base_template)
            }.{filetype}")
        # Otherwise, return json or yaml template filepath
        return (self.folderpaths["lib_custom"] / base_folder / base_template / f"{base_template}.{filetype}")

    def clone_template_file(self, document: dict, filetype: str) -> None:
        """Clone a template file for a given document and filetype.

        Args:
            document (dict): The document for which to clone the template file. Must contain a "document_base_folder" key.
            filetype (str): The filetype of the template file to clone (e.g., "json", "yaml", "html").

        Raises:
            NotFoundError: If the source template file does not exist.
        """
        # Determine source template filepath
        source_filepath = self.get_template_filepath(document, filetype)
        # If template does not exist
        if not source_filepath.exists():
            # Raise error
            raise NotFoundError(f"{source_filepath} doesn't exist.")
        # Define source filename
        source_filename = source_filepath.name
        # Define destination filename
        destination_filename = f"{
            datetime.now(tz=UTC).strftime('%Y_%m_%d__%H%M%S')}__{
                document['document_base_folder'].replace("/","_")}.{filetype}"
        # Clone template
        shutil.copy(source_filepath, self.folderpaths["data"])
        # Rename cloned template
        shutil.move(
            self.folderpaths["data"] / source_filename,
            self.folderpaths["data"] / destination_filename
        )

    def get_files_to_process(self, filetype: str) -> Path:
        """Get all files in the data folder with the specified filetype.

        Args:
            filetype (str): The filetype of the files to retrieve (e.g., "json", "yaml", "html").

        Returns:
            Path: A generator of paths to the files with the specified filetype.
        """
        return self.folderpaths["data"].rglob(f"*.{filetype}")
