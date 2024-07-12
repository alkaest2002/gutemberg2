import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment

# constants
BASE_PATH = Path(os.getcwd())
LIB_PATH = BASE_PATH / "lib"
LIB_BASE_PATH = LIB_PATH / "_base"
LIB_CUSTOM_PATH = LIB_PATH / "custom"

# init jinja environment
jinja_env = Environment(
    loader=FileSystemLoader([ LIB_BASE_PATH, LIB_CUSTOM_PATH ]))
