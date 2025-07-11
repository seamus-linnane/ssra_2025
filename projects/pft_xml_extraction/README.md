# PFT XML Extraction

This folder contains a small utility to convert pulmonary function test (PFT) XML files into structured JSON and CSV formats.

The logic was originally developed in `pft_xml.ipynb` and is now packaged as the command line script `pft_extractor.py`.

## Getting Started

1. Install the dependencies listed in `requirements.txt`.
2. Place your PFT XML files in the `input/` directory.
3. Run the script:

```bash
python pft_extractor.py input/*.xml --output output
```

Results for each XML file are saved in the `output/` folder as `{name}_extracted.json` and `{name}_extracted.csv`.

## Dependencies

- pandas
- lxml
- matplotlib (only required if you use the notebook for plotting)

## License

This project is released under the same Creative Commons Attribution-NonCommercial 4.0 license as the rest of the repository.
