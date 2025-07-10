# ECG Rhythm Strip Digitiser

This repository contains a structured notebook to extract digitise and calibrate ECG rhythm strip images using Python. The source file is expected to be a 12 lead ECG as PDF. Store these in the output folder. Assumptions are made of the orientation of each lead on the page. You may need to change some of the extraction parameters depending on your dataset. The workflow extracts pixel-based trace data and converts it into physiological units (mV and ms) using the calibration pulse embedded in the image.

## Features

- Converts PDF files to PNG.
- Extracts the twelve lead trace based on a red calibration grid as bounding box  
- Extracts a lead II rhythm strip based on its expected position on the page  
- Converts digitised rhythm strip traces into pixel measured CSV data  
- Automatically detects the calibration pulse  
- Converts pixel coordinates to time (ms) and voltage (mV)  
- Generates clean rhythm strip plots  
- Saves interim data and images to the output folder  

## Getting Started

1. Clone this repository.
2. Set up the environment using `requirements.txt`.  
3. Launch the Jupyter notebook to follow the guided workflow.

Place your own ECGs as PDFs in the `input/` folder.

## Dependencies

Python 3.11.12 with:

- numpy
- pandas
- matplotlib
- opencv-python
- scikit-image
- scipy
- pillow
- pytesseract
- pdf2image

(Exact versions listed in `requirements.txt`.)

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).  
You may use, modify, and share this work for non-commercial purposes with attribution.  
© Seamus Linnane & Tawin Medical, 2025.  
