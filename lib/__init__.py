from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# Constants
BASE_PATH = Path.cwd()
LIB_PATH = BASE_PATH / "lib"
LIB_BASE_PATH = LIB_PATH / "_base"
LIB_CUSTOM_PATH = LIB_PATH / "custom"

# Init Jinja environment
jinja_env = Environment(
    loader=FileSystemLoader([ LIB_BASE_PATH, LIB_CUSTOM_PATH ])
)
