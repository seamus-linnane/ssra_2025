# 🖼️ Waveform Digitisation Tool (SSRA2025)

This subproject allows you to convert scanned or rasterised biomedical waveforms (e.g. ECGs or plethysmography traces) into digitised pixel coordinates suitable for downstream analysis or machine learning.

It standardises waveform images, extracts clean signal traces, and saves both:
- A high-resolution **CSV file** of trace coordinates
- A **digitised preview image** for verification

---

## 📁 Folder Structure

```
digitise_image/
├── input/               # Place your source waveform images here
├── output/              # Standardised images, digitised plots, CSVs
├── environment.yaml     # Conda environment for reproducibility
├── digitise_wave_image.ipynb  # Main notebook
└── README.md
```

---

## ⚙️ Setup

Create the Conda environment:

```bash
conda env create -f /full/path/to/digitise_image/environment.yaml
conda activate ssra
```

Or if you're already inside the environment and need to update:
```bash
conda env update -f /full/path/to/digitise_image/environment.yaml --prune
```

---

## 🧪 Usage

1. Add one or more `.png` or `.jpg` images to the `input/` folder  
2. Run the notebook: `digitise_wave_image.ipynb`  
3. Outputs appear in the `output/` folder:
   - `_std` images: cleaned, standardised versions of the input
   - `_digitised.png`: visual trace built from digitised data
   - `_trace.csv`: numeric pixel coordinates

---

## ✅ Output Example

| Filename                   | Description                          |
|----------------------------|--------------------------------------|
| `ecg_std.png`              | White background, black trace image  |
| `ecg_std_digitised.png`    | Clean digital render of extracted trace |
| `ecg_std_trace.csv`        | `x_pixel`, `y_pixel` coordinates     |

---

## 📌 Notes

- The trace is extracted from a binarised, preprocessed version of the input image
- The CSV uses all trace pixels, sorted by horizontal (x) position
- This notebook is fully self-contained and ready for adaptation to your ML pipeline

---

## 📚 Authors & Credits

This subproject is part of the **SSRA2025** student research programme under supervision of [Dr. Seamus Linnane](https://github.com/seamus-linnane).  
Contributions by students working on ECG and plethysmography signal modelling.
