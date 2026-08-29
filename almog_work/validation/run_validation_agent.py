import argparse
import json
from pathlib import Path

from validation_agent import validate_clinical_statements


def main():
    parser = argparse.ArgumentParser(description="Run the local Granite validation agent on extracted statements.")
    parser.add_argument("--input", required=True, help="Path to a JSON file of extracted statements")
    parser.add_argument("--output", default="validated_statements.json", help="Output JSON path")
    args = parser.parse_args()

    statements = json.loads(Path(args.input).read_text(encoding="utf-8"))
    records = validate_clinical_statements(statements)

    Path(args.output).write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Validated {len(records)} statements to {args.output}")


if __name__ == "__main__":
    main()
