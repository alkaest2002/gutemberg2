import json
from collections.abc import Callable
from typing import Any, Self

import yaml

from lib.data_loader import DataLoader
from lib.errors import TracebackNotifier
from lib.filer import Filer
from lib.renderer import Renderer


class Processor:
    """Processor class to process files and render documents.

    Attributes:
        filetype (str): The type of the file to process (e.g., "json", "yaml").
        parse_fn (Callable): The function to parse the file (e.g., json.load, yaml.safe_load_all).
    """

    def __init__(self, filetype: str, parse_fn: Callable) -> None:
        """Initialize Processor class.
        Args:
            filetype (str): The type of the file to process (e.g., "json", "yaml").
            parse_fn (Callable): The function to parse the file (e.g., json.load, yaml.safe_load_all).

        Returns:
            None
        """
        self.filetype: str = filetype
        self.parse_fn: Callable[[Any], Any] = parse_fn

    @classmethod
    def json_processor(cls) -> Self:
        """Initialize Processor class with json."""
        # init Processor class with json
        return cls("json", json.load)

    @classmethod
    def yaml_processor(cls) -> Self:
        """Initialize Processor class with yaml."""
        # init Processor class with yaml
        return cls("yaml", yaml.safe_load_all)

    def process_files(self) -> None:
        """Process files and render documents."""
        try:
            # init Filer class
            filer: Filer = Filer()
            # init DataLoader class
            data_loader: DataLoader = DataLoader(filer, self.filetype, self.parse_fn)
            # init Renderer class
            renderer: Renderer = Renderer(filer, data_loader)
            # render document(s)
            renderer.render_documents()
        # on error
        except Exception as e:
            # notify error message
            print(e)  # noqa: T201
            # notify traceback
            TracebackNotifier(e).notify_traceback()
