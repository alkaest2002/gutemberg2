import os
import shutil

from datetime import datetime
from pathlib import Path

from lib import LIB_PATH, LIB_BASE_PATH, LIB_CUSTOM_PATH
from lib.Errors import NotFoundError

class Filer(object):

    def __init__(self) -> None:
        self.folderpaths: dict = self.set_folderpaths()

    def set_folderpaths(self):
        # define relevant paths
        folder_paths = {
            "cwd": Path(os.getcwd()),
            "data" : Path("./data"),
            "xerox" : Path("./xerox"),
            "lib" : LIB_PATH,
            "lib_base": LIB_BASE_PATH,
            "lib_custom": LIB_CUSTOM_PATH
        }
        # ensure all relevant paths exist
        if all(map(lambda f: f.exists(), folder_paths.values())):
            # return relevant paths
            return folder_paths
        # otherwise
        else:
            # raise error
            raise NotFoundError(f"Missing paths: {[ str(p) for p in folder_paths.values() if not p.exists() ]}.")

    def get_folderpath(self, folder_path: str = "all") -> Path | dict[str, Path]:
        # user requests all paths
        if folder_path == "all":
            return self.folderpaths
        # user requests specific path
        elif folder_path in self.folderpaths.keys():
            return self.folderpaths[folder_path]
        # if users requests invalid path
        else:
            # raise error
            raise NotFoundError(f"'{folder_path}' doesn't exist.")

    def get_template_filepath(self, document: dict, filetype: str) -> Path:
        # unpack area and template
        base_folder, base_template = document["document_base_folder"].split("/")
        # if filetype is html
        if filetype == "html":
            # return html template filepath
            return (self.folderpaths["lib_custom"] / base_folder / base_template / f"{
                document.get('jinja_template', base_template)
            }.{filetype}")
        # otherwise
        else:
            # return json or yaml template filepath
            return (self.folderpaths["lib_custom"] / base_folder / base_template / f"{base_template}.{filetype}")

    def clone_template_file(self, document: dict, filetype: str) -> None:
        # determine soruce template filepath
        source_filepath = self.get_template_filepath(document, filetype)
        # if template does not exist
        if not source_filepath.exists():
            # raise error
            raise NotFoundError(f"{source_filepath} doesn't exist.")
        # define source filename
        source_filename = source_filepath.name
        # define destination filename
        destination_filename = f"{
            datetime.now().strftime('%Y_%m_%d__%H%M%S')}__{
                document['document_base_folder'].replace("/","_")}.{filetype}"
        # clone template
        shutil.copy(source_filepath, self.folderpaths["data"])
        # rename cloned template
        shutil.move(
            self.folderpaths["data"] / source_filename,
            self.folderpaths["data"] / destination_filename
        )

    def get_files_to_process(self, filetype: str) -> Path:
        # get all files in data folder with specifid filetype
        return self.folderpaths["data"].rglob(f"*.{filetype}")
