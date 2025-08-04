
# ML Detection of Metabolic Thresholds Using HR

## Project Summary

Progressive exercise testing (“progex”) provides physiological insights via cardiopulmonary metrics like VO₂max and lactate threshold (LT). But these tests require complex lab equipment. Replicating a progex protocol in the field where often only heart rate data is available would offer considerable advantages. This project explores whether machine learning (ML) can extract key metabolic thresholds from HR data alone in near-real time.

Real-time or near-real-time identification of LT could enhance performance feedback and decision-making during testing in the lab or in training using field tests. It would avoid than waiting for full analysis after lab test completion or avoid the need for lab attendance.

This study will use HR and time-series data from 40 subjects undergoing standardised progex protocols, along with VO₂, VCO₂, and RQ data for ground truth. The task is to compare different ML models for detecting and predicting metabolic thresholds using only HR-derived features. We begin with a relatively easy retrospective classification task and move toward more ambitious goals like VO₂max prediction and real-time LT detection.

All development will be in Python using Jupyter notebooks. You’re encouraged to commit your work to the 2025 SSRA course GitHub repository:  
[https://github.com/seamus-linnane/ssra_2025](https://github.com/seamus-linnane/ssra_2025)

---

## Data Description

For each of 40 subjects, you’ll have the following time-series data collected during a ramped progressive exercise test:
- Time (mm:ss)  
- Heart Rate (HR, bpm)  
- VO₂ (mL/kg/min)  
- VCO₂ (mL/kg/min)  
- RQ (VCO₂/VO₂)  
- Technician-determined LT point  
- Demographics: Age, Gender  

### Derived features to be extracted include — you may add more:
- HR slope is essentially the first derivative of HR over time  
- HR accel is the second derivative of HR over time  
- Rolling HR average (10s, 20s, 30s)  
- Delta from baseline  
- HR/MaxHR using standard prediction equations  
- auc_hr the cumulative area under HR-time curve from start to current time  

---

## Project Phases

### 1. Retrospective LT Classification
- Task: Predict whether the subject has crossed the LT in the past 30 seconds.
- Ground truth: RQ ≥ 1.0, optionally technician-labeled LT
- Models: Logistic Regression, Random Forest, Gradient Boosting
- Evaluation: Binary classification (F1, AUC)

### 2. Window Comparison: How Close to Real-Time Can We Get?
- Repeat the LT+ classification task with shrinking retrospective windows: 30s → 20s → 10s
- Goal: Determine the smallest window that still gives acceptable performance
- Evaluate model drop-off and latency tradeoffs

### 3. LT Time Prediction (Per Subject)
- Predict the time of LT for each subject as a regression task
- Evaluate absolute error against true LT time (from RQ or technician)

### 4. VO₂max Prediction
- Task: Predict VO₂max using HR-derived features
- Start by predicting HRmax, then VO₂max
- Include standard prediction equations for VO₂max as baselines (age, gender)
- Use: Linear Regression, Gradient Boosting, Random Forest
- Evaluate: MAE (Mean Absolute Error), R²

### 5. VO₂ at LT Prediction
- Predict the VO₂ value at LT per subject using HR and derived features
- Regression framing, evaluated with MAE and R²

---

## Modeling Consistency

To encourage fair model comparison:
- Use the same set of models for all tasks, even if not ideal for each (Logistic Regression, Random Forest, Gradient Boosting, Linear Regression for regression targets)

---

## Classification Framing

Use both binary and multi-class classification:
- Binary: LT+ vs LT−
- Multiclass: Pre-LT, Approaching LT, Post-LT (if labelable)

---

## Optional Add-Ons

- Implement LSTM or 1D CNN sequence models  
- Justify their use (sequence memory, trend detection)  
- Compare against classical models  
- Real-time prediction loop simulation  
- Feed data point by point to model to simulate online detection  

---

## Feature Exploration

- Explore feature importance via model interpretability tools (e.g., SHAP, RF feature importances)  
- Rank HR-derived features for LT and VO₂max prediction  

---

## Outputs

- Jupyter notebooks for each major section  
- Visualizations: HR/RQ traces, LT prediction overlays, model comparisons  
- Performance summaries across models and window sizes  
- GitHub commits with clear documentation and markdown commentary  

---

## Project Goals

- Write up findings for departmental presentation  
- Target conference submission - follow up of previous work  
- Use GitHub repo as future reference for academic or employment review  
- Draft full paper based on work across two years of experimentation  
