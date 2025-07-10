import json
from pathlib import Path
from typing import Iterable, Dict, Any

import pandas as pd
from lxml import etree


def extract_graph(graph_elem: etree._Element) -> Dict[str, Any]:
    """Extract metadata and point list from a Graph element."""
    return {
        "X": graph_elem.attrib.get("X"),
        "Y": graph_elem.attrib.get("Y"),
        "Count": int(graph_elem.attrib.get("Count", "0")),
        "SamplingInterval": float(graph_elem.attrib.get("SamplingInterval", "0")),
        "Points": [
            [float(p.attrib["X"]), float(p.attrib["Y"])]
            for p in graph_elem.iter("Point")
            if "X" in p.attrib and "Y" in p.attrib
        ],
    }


def parse_xml_to_dict(root: etree._Element) -> Dict[str, Any]:
    """Convert the XML tree into a nested dictionary."""
    subject = root.find("Subject")
    visit = subject.find("Visit")

    return {
        "Subject": {
            "SubjectID": subject.findtext("ID"),
            "FirstName": subject.findtext("FirstName"),
            "LastName": subject.findtext("LastName"),
            "DOB": subject.find("DayOfBirth").attrib.get("ExtendedInfo"),
            "Gender": subject.find("GenderID").attrib.get("ExtendedInfo"),
            "Ethnicity": subject.find("ethnicID").attrib.get("ExtendedInfo"),
        },
        "Visit": {
            "RecordID": visit.findtext("RecordID"),
            "CreatedOn": visit.find("CreatedOn").attrib.get("ExtendedInfo"),
            "Smoker": visit.findtext("Smoker"),
            "CigarettesPerDay": visit.findtext("CigDie"),
            "SmokeYears": visit.findtext("SmokeYears"),
            "SmokeWhat": visit.findtext("SmokeWhat"),
            "NonSmokeYears": visit.findtext("NonSmokeYears"),
            "Height_cm": visit.findtext("Height"),
            "Weight_kg": visit.findtext("Weight"),
            "HRMax": visit.findtext("HRMax"),
            "Technician": visit.findtext("Technician"),
            "Physician": visit.findtext("Physician"),
            "ReferringPhysician": visit.findtext("ReferringPhysician"),
            "VisitReason": visit.findtext("VisitReason"),
            "Diabetes": visit.findtext("Diabetes"),
            "Tests": [],
        },
    }


def add_tests_from_xml(data_dict: Dict[str, Any], visit_elem: etree._Element) -> None:
    """Add test information from the XML into ``data_dict``."""
    for test in visit_elem.findall("Test"):
        test_type_elem = test.find("TestType")
        test_type = test_type_elem.attrib.get("ExtendedInfo") if test_type_elem is not None else None
        test_id = test_type_elem.text if test_type_elem is not None else None

        test_record = {
            "TestType": test_type,
            "TestID": test_id,
            "Parameters": [],
            "Graphs": {},
        }

        additional_data = test.find("AdditionalData")
        if additional_data is not None:
            for param in additional_data.iter("Parameter"):
                test_record["Parameters"].append(dict(param.attrib))
            for graph in additional_data:
                if graph.tag.startswith("Graph"):
                    test_record["Graphs"][graph.tag] = extract_graph(graph)

        data_dict["Visit"]["Tests"].append(test_record)


def flatten_dict_to_row(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten the nested dictionary structure into a single row."""
    subject = data_dict["Subject"]
    visit = data_dict["Visit"]
    row = {
        "SubjectID": subject.get("SubjectID"),
        "FirstName": subject.get("FirstName"),
        "LastName": subject.get("LastName"),
        "DOB": subject.get("DOB"),
        "Gender": subject.get("Gender"),
        "Ethnicity": subject.get("Ethnicity"),
        "VisitRecordID": visit.get("RecordID"),
        "VisitDate": visit.get("CreatedOn"),
        "Smoker": visit.get("Smoker"),
        "CigarettesPerDay": visit.get("CigarettesPerDay"),
        "SmokeYears": visit.get("SmokeYears"),
        "SmokeWhat": visit.get("SmokeWhat"),
        "NonSmokeYears": visit.get("NonSmokeYears"),
        "Height_cm": visit.get("Height_cm"),
        "Weight_kg": visit.get("Weight_kg"),
        "HRMax": visit.get("HRMax"),
        "Technician": visit.get("Technician"),
        "Physician": visit.get("Physician"),
        "ReferringPhysician": visit.get("ReferringPhysician"),
        "VisitReason": visit.get("VisitReason"),
        "Diabetes": visit.get("Diabetes"),
    }

    for test in visit.get("Tests", []):
        test_prefix = test.get("TestType", "Unknown").replace(" ", "_")
        for param in test.get("Parameters", []):
            name = param.get("Name", "Unnamed").replace(" ", "_")
            for k, v in param.items():
                if k != "Name":
                    col = f"{test_prefix}_{name}_{k}".replace(" ", "_")
                    row[col] = v
        for _, gdata in test.get("Graphs", {}).items():
            if gdata.get("X") == "V (L)" and gdata.get("Y") == "F (L/s)" and gdata.get("Points"):
                row["FlowVolumeLoop"] = gdata["Points"]
                break

    return row


def process_xml_files(xml_files: Iterable[Path], output_dir: Path) -> None:
    """Process one or more XML files and write JSON/CSV outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for xml_path in xml_files:
        print(f"\U0001F4C2 Processing: {xml_path.name}")
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        visit_elem = root.find(".//Visit")

        data_dict = parse_xml_to_dict(root)
        add_tests_from_xml(data_dict, visit_elem)

        json_path = output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, indent=2)
        print(f"\u2705 JSON saved to: {json_path}")

        row = flatten_dict_to_row(data_dict)
        df = pd.DataFrame([row])
        csv_path = output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.csv"
        df.to_csv(csv_path, index=False)
        print(f"\u2705 CSV saved to: {csv_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract PFT XML files to CSV and JSON")
    parser.add_argument("xml_files", nargs="+", type=Path, help="Input XML files")
    parser.add_argument("--output", "-o", type=Path, default=Path.cwd(), help="Output directory")
    args = parser.parse_args()
    process_xml_files(args.xml_files, args.output)
