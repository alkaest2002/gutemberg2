# Gutemberg2

Generate PDF documents from JSON/YAML data using Jinja templates and WeasyPrint.

## What This Project Does

Gutemberg2 reads document definitions from files in `data/`, enriches each document with:

- base fields (`document_filename`, `document_date`)
- optional shared values from `optional_data.json`
- optional template-specific post-processing (`post_hoc.py`)

Then it renders HTML via Jinja and writes PDFs to `xerox/`.

## Project Structure

- `init.py`: clones a template JSON/YAML file into `data/` with a timestamped filename.
- `process_YAML.py`: processes all YAML files in `data/`.
- `process_JSON.py`: processes all JSON files in `data/`.
- `lib/filer.py`: path handling, template resolution, file discovery.
- `lib/data_loader.py`: parsing + enrichment + post-hoc processing.
- `lib/renderer.py`: Jinja rendering + PDF generation.
- `lib/custom/`: custom template families (`<area>/<template>/...`).

## Requirements

- Python >= 3.14 (as declared in `pyproject.toml`)
- macOS/Linux system libraries required by WeasyPrint



