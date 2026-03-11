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
    # init filer
    filer = Filer()
    # clone data template
    filer.clone_template_file({"document_base_folder": args.template}, args.filetype)
# on error
except Exception as e:
    # notify error message
    print(e)  # noqa: T201
    # notify traceback
    TracebackNotifier(e).notify_traceback()
