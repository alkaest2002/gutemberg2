import json
import yaml

from typing import Callable, Self
from lib.Filer import Filer
from lib.DataLoader import DataLoader
from lib.Renderer import Renderer
from lib.Errors import TracebackNotifier

class Processor(object):

    def __init__(self, filetype: str, parse_fn: Callable) -> None:
        self.filetype = filetype
        self.parse_fn = parse_fn

    @classmethod
    def json_processor(cls) -> Self:
        # init Processor class with json
        return cls("json", json.load)

    @classmethod
    def yaml_processor(cls) -> Self:
        # init Processor class with yaml
        return cls("yaml", yaml.safe_load_all)

    def process_files(self) -> None:
        try:
            # init Filer class
            filer = Filer()
            # init DataLoader class
            data_loader = DataLoader(filer, self.filetype, self.parse_fn)
            # init Renderer class
            renderer = Renderer(filer, data_loader)
            # render document(s)
            renderer.render_documents()
        # on error
        except Exception as e:
            # notify error message
            print(e)
            # notify traceback
            TracebackNotifier(e).notify_traceback()
