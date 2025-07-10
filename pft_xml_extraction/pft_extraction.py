import json
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET


def extract_graph(graph_elem):
    """Return graph metadata and points."""
    return {
        "X": graph_elem.get("X"),
        "Y": graph_elem.get("Y"),
        "Count": int(graph_elem.get("Count", "0")),
        "SamplingInterval": float(graph_elem.get("SamplingInterval", "0")),
        "Points": [
            [float(p.get("X")), float(p.get("Y"))]
            for p in graph_elem.findall("Point")
            if p.get("X") is not None and p.get("Y") is not None
        ],
    }


def parse_xml_to_dict(root: ET.Element):
    subject = root.find("Subject")
    visit = subject.find("Visit")
    data = {
        "Subject": {
            "SubjectID": subject.findtext("ID"),
            "FirstName": subject.findtext("FirstName"),
            "LastName": subject.findtext("LastName"),
            "DOB": subject.find("DayOfBirth").get("ExtendedInfo"),
            "Gender": subject.find("GenderID").get("ExtendedInfo"),
            "Ethnicity": subject.find("ethnicID").get("ExtendedInfo"),
        },
        "Visit": {
            "RecordID": visit.findtext("RecordID"),
            "CreatedOn": visit.find("CreatedOn").get("ExtendedInfo"),
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
    return data


def add_tests_from_xml(data_dict, visit_elem):
    for test in visit_elem.findall("Test"):
        test_type_elem = test.find("TestType")
        test_type = test_type_elem.get("ExtendedInfo") if test_type_elem is not None else None
        test_id = test_type_elem.text if test_type_elem is not None else None
        test_record = {
            "TestType": test_type,
            "TestID": test_id,
            "Parameters": [],
            "Graphs": {},
        }
        additional_data = test.find("AdditionalData")
        if additional_data is not None:
            for param in additional_data.findall("Parameter"):
                test_record["Parameters"].append(dict(param.attrib))
            for graph in additional_data:
                if graph.tag.startswith("Graph"):
                    test_record["Graphs"][graph.tag] = extract_graph(graph)
        data_dict["Visit"]["Tests"].append(test_record)


def flatten_dict_to_row(data_dict):
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
        prefix = test.get("TestType", "Unknown").replace(" ", "_")
        for param in test.get("Parameters", []):
            name = param.get("Name", "Unnamed").replace(" ", "_")
            for k, v in param.items():
                if k != "Name":
                    col = f"{prefix}_{name}_{k}".replace(" ", "_")
                    row[col] = v
        for gname, gdata in test.get("Graphs", {}).items():
            if gdata.get("X") == "V (L)" and gdata.get("Y") == "F (L/s)" and gdata.get("Points"):
                row["FlowVolumeLoop"] = gdata["Points"]
                break
    return row


def process_file(xml_path, output_dir):
    xml_path = Path(xml_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    root = ET.parse(xml_path).getroot()
    visit_elem = root.find(".//Visit")
    data_dict = parse_xml_to_dict(root)
    add_tests_from_xml(data_dict, visit_elem)

    json_path = output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, indent=2)

    csv_path = output_dir / f"{xml_path.stem.replace(' ', '_')}_extracted.csv"
    row = flatten_dict_to_row(data_dict)
    pd.DataFrame([row]).to_csv(csv_path, index=False)

    return csv_path, json_path
