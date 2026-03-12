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
        # Init Processor class with json
        return cls("json", json.load)

    @classmethod
    def yaml_processor(cls) -> Self:
        """Initialize Processor class with yaml."""
        # Init Processor class with yaml
        return cls("yaml", yaml.safe_load_all)

    def process_files(self) -> None:
        """Process files and render documents."""
        try:
            # Init Filer class
            filer: Filer = Filer()

            # Init DataLoader class
            data_loader: DataLoader = DataLoader(filer, self.filetype, self.parse_fn)

            # Init Renderer class
            renderer: Renderer = Renderer(filer, data_loader)

            # Render document(s)
            renderer.render_documents()

        # On error
        except Exception as e:
            # Notify error message
            print(e)  # noqa: T201

            # Traceback
            TracebackNotifier(e).notify_traceback()
