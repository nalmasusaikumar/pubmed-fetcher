# PubMed Fetcher

Fetches research papers from PubMed with authors affiliated to pharma/biotech companies.

## Code Organization
- `pubmed_fetcher.py`: Core module for fetching and parsing papers.
- `cli.py`: Command-line interface to use the module.

## Installation
1. Clone the repo: `git clone <github-url>`
2. Install Poetry: `pip install poetry`
3. Run: `poetry install`

## Usage
```bash
poetry run get-papers-list "cancer treatment" -f results.csv -d