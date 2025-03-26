from typing import List, Dict, Optional
import csv
from Bio import Entrez
import xml.etree.ElementTree as ET

Entrez.email = "saikumar74799@gmail.com" 

def fetch_papers(query: str, debug: bool = False) -> List[Dict[str, str]]:
    """Fetch papers from PubMed based on query."""
    if debug:
        print(f"Querying PubMed with: {query}")
    
    # Search PubMed
    handle = Entrez.esearch(db="pubmed", term=query, retmax=100)
    search_results = Entrez.read(handle)
    handle.close()
    
    ids = search_results["IdList"]
    if not ids:
        if debug:
            print("No papers found.")
        return []
    
    # Fetch details
    handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
    xml_data = handle.read()
    handle.close()
    
    return parse_papers(xml_data, debug)

def parse_papers(xml_data: bytes, debug: bool) -> List[Dict[str, str]]:
    """Parse XML data and filter pharma/biotech papers."""
    root = ET.fromstring(xml_data)
    results = []
    
    for article in root.findall(".//PubmedArticle"):
        paper = {}
        
        # PubmedID
        paper["PubmedID"] = article.find(".//PMID").text
        
        # Title
        paper["Title"] = article.find(".//ArticleTitle").text
        
        # Publication Date
        date = article.find(".//PubDate")
        year = date.find("Year").text if date.find("Year") is not None else "N/A"
        month = date.find("Month").text if date.find("Month") is not None else "01"
        day = date.find("Day").text if date.find("Day") is not None else "01"
        paper["Publication Date"] = f"{year}-{month}-{day}"
        
        # Authors and Affiliations
        authors = []
        affiliations = []
        author_list = article.findall(".//Author")
        for author in author_list:
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            if last_name is not None and fore_name is not None:
                full_name = f"{fore_name.text} {last_name.text}"
                affiliation = author.find(".//Affiliation")
                if affiliation is not None:
                    affiliations.append(affiliation.text)
                    # Heuristic: Pharma/biotech check
                    if is_pharma_affiliation(affiliation.text):
                        authors.append(full_name)
        
        # Filter for pharma/biotech
        if authors:
            paper["Non-academic Author(s)"] = "; ".join(authors)
            paper["Company Affiliation(s)"] = "; ".join(filter(is_pharma_affiliation, affiliations))
        
        # Email (assume first author with email as corresponding)
        email = article.find(".//Author//Affiliation/../..//Email")
        paper["Corresponding Author Email"] = email.text if email is not None else "N/A"
        
        if "Non-academic Author(s)" in paper:
            results.append(paper)
    
    if debug:
        print(f"Found {len(results)} papers with pharma/biotech affiliations.")
    return results

def is_pharma_affiliation(affiliation: str) -> bool:
    """Check if affiliation is pharma/biotech."""
    pharma_keywords = {"Inc", "Pharma", "Biotech", "Pfizer", "Novartis", "GSK"}
    return any(keyword in affiliation for keyword in pharma_keywords)

def save_to_csv(papers: List[Dict[str, str]], filename: Optional[str] = None) -> None:
    """Save results to CSV or print to console."""
    columns = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", 
               "Company Affiliation(s)", "Corresponding Author Email"]
    
    if filename:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(papers)
    else:
        print(",".join(columns))
        for paper in papers:
            print(",".join(f'"{paper.get(col, "N/A")}"' for col in columns))