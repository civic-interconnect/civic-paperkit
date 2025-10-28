# civic-paperkit

[![PyPI](https://img.shields.io/pypi/v/civic-paperkit.svg)](https://pypi.org/project/civic-paperkit/)
[![Python versions](https://img.shields.io/pypi/pyversions/civic-paperkit.svg)](https://pypi.org/project/civic-paperkit/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/civic-interconnect/civic-paperkit/actions/workflows/ci.yml/badge.svg)](https://github.com/civic-interconnect/civic-paperkit/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blue)](https://civic-interconnect.github.io/civic-paperkit/)

> Automatically download research data linked to your bibliography references.

**civic-paperkit** fetches datasets, CSVs, and supplementary materials referenced in your academic papers.
It reads your `.bib` file and a companion metadata file to archive all your sources.


---

## Installation

```shell
pip install civic-paperkit
```
---

## Quick Start

1. Create a `refs_meta.yaml` file mapping your BibTeX keys to data sources:
```yaml
# refs_meta.yaml
cdc_pmdr:
  notes: "CDC Maternal Mortality Rates 2018-2022"
  assets:
    - url: "https://data.cdc.gov/api/views/e2d5-ggg7/rows.csv"
      filename: "maternal_mortality.csv"

smith2024:
  assets:
    - page_url: "https://example.org/supplementary"
      allow_ext: [".csv", ".xlsx", ".zip"]
```

2. Run the tool:
```shell
ci-paperkit --bib paper/refs.bib --meta paper/refs_meta.yaml
```

3. Find your data in `data/raw/<bibkey>/`

## Features

- Download direct file URLs (CSV, Excel, PDF, etc.)
- Scrape pages for data files
- Organize downloads by citation key
- Checksum verification (optional)
- Configurable output directories

## Requirements

- Python 3.12+
- A BibTeX file with your references
- A YAML metadata file mapping references to data sources

## License

MIT
