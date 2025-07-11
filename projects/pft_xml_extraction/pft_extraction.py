import json
from pathlib import Path
from typing import Tuple

import pandas as pd
from lxml import etree

from .pft_extractor import (
    parse_xml_to_dict,
    add_tests_from_xml,
    flatten_dict_to_row,
)


def process_file(xml_path: Path, output_dir: Path) -> Tuple[Path, Path]:
    """Process a single XML file and write JSON and CSV outputs."""
    xml_path = Path(xml_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tree = etree.parse(str(xml_path))
    root = tree.getroot()
    visit_elem = root.find(".//Visit")

    data_dict = parse_xml_to_dict(root)
    if visit_elem is not None:
        add_tests_from_xml(data_dict, visit_elem)

    json_path = output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, indent=2)

    csv_path = output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.csv"
    row = flatten_dict_to_row(data_dict)
    pd.DataFrame([row]).to_csv(csv_path, index=False)

    return csv_path, json_path


if __name__ == "__main__":
    input_dir = Path(__file__).parent / "input"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    for xml_file in input_dir.glob("*.xml"):
        print(f"Processing {xml_file.name}")
        process_file(xml_file, output_dir)
