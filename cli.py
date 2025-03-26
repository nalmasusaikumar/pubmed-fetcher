import argparse
from pubmed_fetcher import fetch_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma/biotech affiliations.")
    parser.add_argument("query", help="PubMed search query (e.g., 'cancer treatment')")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug info")
    parser.add_argument("-f", "--file", help="Output CSV filename (default: console)")
    
    args = parser.parse_args()
    
    papers = fetch_papers(args.query, args.debug)
    if papers:
        save_to_csv(papers, args.file)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()