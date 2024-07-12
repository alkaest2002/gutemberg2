import argparse
from lib.Filer import Filer
from lib.Errors import TracebackNotifier

# argparse
parser = argparse.ArgumentParser(prog="Gutemberg2")
parser.add_argument("-t", "--template", required=True)
parser.add_argument("-f", "--filetype", default="yaml", choices=["yaml", "json"])
args = parser.parse_args()

try:
    # init filer
    filer = Filer()
    # clone data template
    filer.clone_template_file(dict(document_base_folder=args.template), args.filetype)
# on error
except Exception as e:
    # notify error message
    print(e)
    # notify traceback
    TracebackNotifier(e).notify_traceback()
