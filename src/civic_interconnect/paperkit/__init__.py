r"""Download public data assets associated with references in a BibTeX file.

Design:
- BibTeX (.bib) remains the citation source of truth.
- A companion YAML file (refs_meta.yaml) maps bib keys to assets to fetch.
- Each asset can be:
  1) Direct file URL (pdf, csv, xlsx, zip, etc.)
  2) A page URL plus simple extraction rules to find data links on that page.

YAML schema (per bibkey):
  <bibkey>:
    notes: Optional free text
    out_dir: Optional custom subdir under data/raw/<bibkey> (default ".")
    assets:
      - url: https://example.org/data.csv              # direct file
        filename: optional-custom-name.csv
        checksum: optional_sha256_hex
      - page_url: https://example.org/tables.html      # page to scan
        allow_ext: [".csv", ".xlsx", ".zip"]           # whitelist extensions
        href_regex: "\\b(download|data|table)\\b"      # optional regex filter
        limit: 5                                       # optional cap
        base_url: https://example.org                  # optional base

CLI:
  uv run ci-paperkit fetch_bib --bib paper/refs.bib --meta paper/refs_meta.yaml

Outputs:
  data/raw/<bibkey>[/out_dir]/<filename>

Dependencies:
  - bibtexparser
  - pyyaml
  - requests
  - beautifulsoup4

"""
