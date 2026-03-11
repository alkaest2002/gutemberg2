import argparse

from lib.errors import TracebackNotifier
from lib.filer import Filer

# Init argparse parser
parser = argparse.ArgumentParser(prog="Gutemberg2")

# Add arguments
parser.add_argument("-t", "--template", required=True)
parser.add_argument("-f", "--filetype", default="yaml", choices=["yaml", "json"])

# Parse arguments
args = parser.parse_args()

try:
    # Init filer
    filer = Filer()
    # Clone data template
    filer.clone_template_file({"document_base_folder": args.template}, args.filetype)

# On error
except Exception as e:
    # Notify error message
    print(e)  # noqa: T201
    # Traceback
    TracebackNotifier(e).notify_traceback()
