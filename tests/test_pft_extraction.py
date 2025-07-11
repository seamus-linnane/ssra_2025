from pathlib import Path
import csv
import json

import importlib
import sys


def create_sample_xml(path: Path):
    xml_content = """
<Root>
  <Subject>
    <ID>123</ID>
    <FirstName>Test</FirstName>
    <LastName>User</LastName>
    <DayOfBirth ExtendedInfo="1990-01-01" />
    <GenderID ExtendedInfo="M">1</GenderID>
    <ethnicID ExtendedInfo="Other" />
    <Visit>
      <RecordID>rec1</RecordID>
      <CreatedOn ExtendedInfo="2025-01-01" />
      <Smoker>0</Smoker>
      <CigDie>10</CigDie>
      <SmokeYears>5</SmokeYears>
      <SmokeWhat>cigars</SmokeWhat>
      <NonSmokeYears>2</NonSmokeYears>
      <Height>180</Height>
      <Weight>70</Weight>
      <HRMax>170</HRMax>
      <Technician>tech</Technician>
      <Physician>doc</Physician>
      <ReferringPhysician>ref</ReferringPhysician>
      <VisitReason>routine</VisitReason>
      <Diabetes>No</Diabetes>
      <Test>
        <TestType ExtendedInfo="Spirometry">1</TestType>
        <AdditionalData>
          <Parameter Name="FEV1" Value="3.1" Units="L" />
          <Graph1 X="V (L)" Y="F (L/s)" Count="2" SamplingInterval="1">
            <Point X="0" Y="0"/>
            <Point X="1" Y="2"/>
          </Graph1>
        </AdditionalData>
      </Test>
    </Visit>
  </Subject>
</Root>
"""
    path.write_text(xml_content)


def test_process_xml_files(tmp_path: Path):
    xml_file = tmp_path / "sample.xml"
    create_sample_xml(xml_file)

    class DummyDataFrame:
        def __init__(self, rows):
            self.rows = rows

        def to_csv(self, path, index=False):
            if not self.rows:
                header = []
            else:
                header = list(self.rows[0].keys())
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                for row in self.rows:
                    writer.writerow(row)

    class DummyPandas:
        @staticmethod
        def DataFrame(rows):
            return DummyDataFrame(rows)

    sys.modules["pandas"] = DummyPandas()

    import types
    import xml.etree.ElementTree as ET
    class DummyEtree(types.SimpleNamespace):
        parse = staticmethod(ET.parse)
        Element = ET.Element
        _Element = ET.Element

    lxml_stub = types.SimpleNamespace(etree=DummyEtree())
    sys.modules["lxml"] = lxml_stub
    sys.modules["lxml.etree"] = lxml_stub.etree

    root_dir = Path(__file__).resolve().parents[1]
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    process_xml_files = importlib.import_module(
        "pft_xml_extraction.pft_extractor"
    ).process_xml_files

    process_xml_files([xml_file], tmp_path)

    csv_path = tmp_path / f"{xml_file.stem}_extracted.csv"
    json_path = tmp_path / f"{xml_file.stem}_extracted.json"

    assert csv_path.exists()
    assert json_path.exists()

    with open(csv_path, newline="") as f:
        rows = list(csv.reader(f))
    assert len(rows) > 1

    data = json.loads(json_path.read_text())
    assert data.get("Subject", {}).get("SubjectID") == "123"
