from pathlib import Path
import pandas as pd
import json

from pft_xml_extraction.pft_extraction import process_file


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


def test_process_file(tmp_path: Path):
    xml_file = tmp_path / "sample.xml"
    create_sample_xml(xml_file)

    csv_path, json_path = process_file(xml_file, tmp_path)

    assert csv_path.exists()
    assert json_path.exists()

    df = pd.read_csv(csv_path)
    assert not df.empty

    data = json.loads(json_path.read_text())
    assert data.get("Subject", {}).get("SubjectID") == "123"
