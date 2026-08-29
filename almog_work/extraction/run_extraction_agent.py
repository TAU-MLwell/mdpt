import argparse
import json
from pathlib import Path

from extraction_agent import extract_clinical_statements


def main():
    parser = argparse.ArgumentParser(description="Run the local Granite extraction agent on a paper text file.")
    parser.add_argument("--input", required=True, help="Path to a text file containing the article content")
    parser.add_argument("--output", default="extracted_statements.json", help="Output JSON path")
    args = parser.parse_args()

    article_text = Path(args.input).read_text(encoding="utf-8")
    records = extract_clinical_statements(article_text)

    Path(args.output).write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Extracted {len(records)} statements to {args.output}")


if __name__ == "__main__":
    main()

