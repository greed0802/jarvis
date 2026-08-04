# Knowledge Source Inventory

## Discovered Implementations
- `src/jarvis/parsers/costx/workbook_parser.py`: CostX workbook parser via openpyxl. (Reuse)
- `src/jarvis/parsers/costx/boq_extraction.py`: Rule-based extraction of BOQ structures. (Reuse)
- `src/jarvis/parsers/costx/loader.py`: File loader specifically for BOQ. (Reuse/Refactor behind standard API)
- `src/jarvis/parsers/observation.py`: Unused ontology definitions. (Archive)

No generic Document Processor (PDF, DOCX, Img), OCR capability, or semantic chunking pipeline exists yet.
All knowledge ingest components must be established adhering to the new Immutable Domain.
