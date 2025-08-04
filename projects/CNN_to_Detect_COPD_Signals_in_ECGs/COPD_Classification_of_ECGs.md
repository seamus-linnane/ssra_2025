
**Machine Learning Identification of Airway Obstruction Using 12-Lead ECG**

---

## Background

Heart and lung disease share common risk factors and often present with similar symptoms, leading to diagnostic challenges. Chronic Obstructive Pulmonary Disease (COPD) is highly prevalent, yet underdiagnosed, especially in patients being evaluated for cardiac conditions. Electrocardiograms (ECGs) are widely used in clinical practice to assess heart disease, but they may also contain valuable insights into pulmonary pathology.

Hyperinflation in COPD alters cardiac orientation, affecting ECG parameters such as QRS amplitude, P-wave morphology, and cardiac axis. Machine learning (ML) techniques have been successfully applied to ECG analysis for detecting cardiac abnormalities, but limited research has explored their utility in identifying COPD as a comorbid or contributory factor in cardiac presentations.

This project aims to develop an ML-based approach to identify unsuspected COPD using only 12-lead ECG data. By linking hospital ECGs to spirometry-confirmed obstruction, this project will assess the feasibility of an ECG-based screening tool that could improve diagnostic accuracy and patient outcomes in those presenting with overlapping cardiac and pulmonary drivers of their symptoms.

---

## Objective

To train and evaluate a machine learning model that identifies and classifies airway obstruction based on 12-lead ECG features.

---

## Methods

### 1. Data Collection
- Extract 1,000+ lung function test reports (PDF format) from hospital records.  
- Convert these reports into a structured, searchable database with FEV1/FVC ratios.  
- Retrieve corresponding 12-lead ECGs using hospital medical record numbers and store them as high-resolution images.  
- Use automated and human-in-the-loop strategies for high quality data labelling.  

### 2. Model Development
- Fine-tune convolutional neural networks using ECG data.  
- Implement baseline logistic regression and decision tree models for comparison.  

---

## Expected Outcomes
- A validated ML model capable of identifying COPD using ECG alone.  
- Identification of novel ECG features associated with airway obstruction.  
- Insights into the feasibility of integrating ECG-based COPD screening into routine cardiac assessments.  

---

## Significance

This study uses widely available ECG data to facilitate earlier COPD detection in patients undergoing cardiac evaluations. If successful, it could improve diagnostic pathways and facilitate timely intervention for patients with undiagnosed COPD, ultimately enhancing clinical outcomes.

---

## Conclusion

This project will explore the novel application of ML to predict COPD using ECG data, enhancing the clinical utility of a readily available, low-cost, and ubiquitous diagnostic test. The findings could serve as a foundation for future large-scale studies and clinical implementations.
