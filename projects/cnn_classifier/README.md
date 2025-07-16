# 🧠 CNN Classifier for Medical Waveform Images

This project demonstrates how to fine-tune a pretrained ResNet-18 convolutional neural network to classify plethysmography (PPG) waveform images. The running example is either **aortic stenosis (AS)** or **control**. It is built for educational purposes within the SSRA program.


## 🗂️ Project Structure

```
cnn_classifier/
├── input/              # Raw input images (e.g., as_*.jpg, control_*.jpg)
├── output/             # Autogen of train/val/test folders
├── cnn_classifier.ipynb# Main notebook with end-to-end pipeline
├── requirements.txt    # Python 3.10 package requirements
```

---

## 🚀 Workflow

1. **📂 Prepare Images**  
   Name the input files using class names as prefixes (e.g. `as_`, `control_`) and place in `input/`.

2. **🧼 Preprocess**  
   The notebook:
   - Maps class names to numeric labels
   - Splits files into train/val/test (80:10:10)
   - Resizes and saves standardized images to `output/`

3. **🧠 Fine-tune ResNet-18**
   - Freeze pretrained layers
   - Train final layer for a few epochs
   - Unfreeze and fine-tune the full model

4. **📈 Evaluate**
   - Plot loss and accuracy curves
   - Print precision, recall, F1-score
   - Show confusion matrix
   - Perform prediction on unseen test data


## 🔧 Setup

```bash
# Clone repo and navigate
git clone https://github.com/yourname/ssra_2025.git
cd cnn_classifier

# Create conda env (optional)
conda create -n ssra python=3.10
conda activate ssra

# Install packages
pip install -r requirements.txt
```

---

## 📊 Notes

- Uses Metal-accelerated PyTorch on Apple Silicon (`torch.device("mps")`)
- Original dataset is illustrative (e.g., variants of waveform images)
- No external calibration or denoising used in this version


## 🙋 Authors

Developed by [Seamus Linnane](https://github.com/seamus-linnane) as part of undergraduate machine learning supervision for biological signal classification.
