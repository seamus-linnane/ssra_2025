import json
from pathlib import Path
from lxml import etree
import pandas as pd


def extract_graph(graph_elem: etree._Element) -> dict:
    """Return structured data from a <Graph> element."""
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


def parse_xml_to_dict(root: etree._Element) -> dict:
    """Parse subject and visit details into a nested dict."""
    subject = root.find("Subject")
    visit = subject.find("Visit") if subject is not None else None

    return {
        "Subject": {
            "SubjectID": subject.findtext("ID"),
            "FirstName": subject.findtext("FirstName"),
            "LastName": subject.findtext("LastName"),
            "DOB": subject.find("DayOfBirth").attrib.get("ExtendedInfo") if subject is not None and subject.find("DayOfBirth") is not None else None,
            "Gender": subject.find("GenderID").attrib.get("ExtendedInfo") if subject is not None and subject.find("GenderID") is not None else None,
            "Ethnicity": subject.find("ethnicID").attrib.get("ExtendedInfo") if subject is not None and subject.find("ethnicID") is not None else None,
        },
        "Visit": {
            "RecordID": visit.findtext("RecordID") if visit is not None else None,
            "CreatedOn": visit.find("CreatedOn").attrib.get("ExtendedInfo") if visit is not None and visit.find("CreatedOn") is not None else None,
            "Smoker": visit.findtext("Smoker") if visit is not None else None,
            "CigarettesPerDay": visit.findtext("CigDie") if visit is not None else None,
            "SmokeYears": visit.findtext("SmokeYears") if visit is not None else None,
            "SmokeWhat": visit.findtext("SmokeWhat") if visit is not None else None,
            "NonSmokeYears": visit.findtext("NonSmokeYears") if visit is not None else None,
            "Height_cm": visit.findtext("Height") if visit is not None else None,
            "Weight_kg": visit.findtext("Weight") if visit is not None else None,
            "HRMax": visit.findtext("HRMax") if visit is not None else None,
            "Technician": visit.findtext("Technician") if visit is not None else None,
            "Physician": visit.findtext("Physician") if visit is not None else None,
            "ReferringPhysician": visit.findtext("ReferringPhysician") if visit is not None else None,
            "VisitReason": visit.findtext("VisitReason") if visit is not None else None,
            "Diabetes": visit.findtext("Diabetes") if visit is not None else None,
            "Tests": [],
        },
    }


def add_tests_from_xml(data_dict: dict, visit_elem: etree._Element) -> None:
    """Populate the Visit['Tests'] list with parameters and graphs."""
    for test in visit_elem.findall("Test"):
        test_type_elem = test.find("TestType")
        test_type = test_type_elem.attrib.get("ExtendedInfo") if test_type_elem is not None else None
        test_id = test_type_elem.text if test_type_elem is not None else None

        record = {
            "TestType": test_type,
            "TestID": test_id,
            "Parameters": [],
            "Graphs": {},
        }

        additional_data = test.find("AdditionalData")
        if additional_data is not None:
            for param in additional_data.iter("Parameter"):
                record["Parameters"].append(dict(param.attrib))
            for graph in additional_data:
                if graph.tag.startswith("Graph"):
                    record["Graphs"][graph.tag] = extract_graph(graph)

        data_dict["Visit"]["Tests"].append(record)


def flatten_dict_to_row(data_dict: dict) -> dict:
    """Flatten a full Visit dict into a single table row."""
    subject = data_dict.get("Subject", {})
    visit = data_dict.get("Visit", {})

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
        prefix = test.get("TestType", "Unknown").replace(" ", "_")
        for param in test.get("Parameters", []):
            name = param.get("Name", "Unnamed").replace(" ", "_")
            for k, v in param.items():
                if k != "Name":
                    col = f"{prefix}_{name}_{k}".replace(" ", "_")
                    row[col] = v
        for gname, gdata in test.get("Graphs", {}).items():
            if (
                gdata.get("X") == "V (L)"
                and gdata.get("Y") == "F (L/s)"
                and gdata.get("Points")
            ):
                row["FlowVolumeLoop"] = gdata["Points"]
                break
    return row


def process_file(xml_path: Path, output_dir: Path) -> None:
    """Process a single XML file and write JSON and CSV outputs."""
    tree = etree.parse(str(xml_path))
    root = tree.getroot()
    visit_elem = root.find(".//Visit")

    data_dict = parse_xml_to_dict(root)
    if visit_elem is not None:
        add_tests_from_xml(data_dict, visit_elem)

    json_path = output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, indent=2)

    row = flatten_dict_to_row(data_dict)
    pd.DataFrame([row]).to_csv(
        output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.csv", index=False
    )


if __name__ == "__main__":
    input_dir = Path(__file__).parent / "input"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    xml_files = list(input_dir.glob("*.xml"))
    for xml_file in xml_files:
        print(f"Processing {xml_file.name}")
        process_file(xml_file, output_dir)
