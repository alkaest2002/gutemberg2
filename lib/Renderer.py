from pathlib import Path
from weasyprint import HTML
from lib import jinja_env, LIB_CUSTOM_PATH
from lib.Filer import Filer
from lib.DataLoader import DataLoader

class Renderer(object):

    def __init__(self, filer: Filer, data_loader: DataLoader):
        self.filer = filer
        self.data_loader = data_loader

    def render_documents(self) -> None:
        # get documents to render
        documents_to_render = self.data_loader.load_documents()
        # loop through documents to render
        for no_document, document in enumerate(documents_to_render, 1):
            # notify number of documents to render
            print(no_document, "documents will be rendered of", len(documents_to_render), end="\r", flush=True)
            # determine jinja template to load
            template_to_get = self.filer.get_template_filepath(document, "html").relative_to(LIB_CUSTOM_PATH)
            # load jinja template
            jinja_template = jinja_env.get_template(str(template_to_get))
            # render jinja template with current document
            rendered_template = jinja_template.render(document)
            # determine output filepath
            output_filepath = self.filer.get_folderpath("xerox") / f"{document['document_filename']}.pdf" # type: ignore
            # write rendered jinja template to output filepath
            HTML(string=rendered_template).write_pdf(output_filepath)
        # notify end of rendering
        print("Rendering job is done.", len(documents_to_render), "processed document(s).")
