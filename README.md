# ssra_2025
Files and sub-projects to support the Beacon Hospital 2025 SSRA program in medical ML.

This repository collects small utilities and experiments that accompany the 2025
Beacon Hospital Summer School for Research in AI.  The `ecg_extraction`
subdirectory contains a full workflow for digitising ECG rhythm strips,
including a Jupyter notebook. The `pft_xml_extraction` directory provides a
command line tool for turning pulmonary function test (PFT) XML files into
tidy JSON and CSV tables.

## Running the notebook

1. Install the dependencies listed in
   `ecg_extraction/requirements.txt`.
2. Launch Jupyter and open the notebook:

   ```bash
   jupyter notebook ecg_extraction/rhythm_strip_notebook.ipynb
   ```

Follow the steps in the notebook to extract and calibrate traces from your own
ECG PDFs.

## PFT XML extraction

The `pft_xml_extraction` folder contains `pft_extraction.py` which converts PFT
XML files into JSON and CSV tables.

```bash
python pft_xml_extraction/pft_extraction.py
```

Place your XML files in `pft_xml_extraction/input` and the outputs will be
written next to them under `pft_xml_extraction/output`.
