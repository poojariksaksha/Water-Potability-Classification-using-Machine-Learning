#  Water Potability Prediction using Machine Learning

This project uses machine learning models to classify water samples as **potable (safe to drink)** or **non-potable**, based on various **physico-chemical properties**. With rising water pollution, the need for scalable and intelligent water testing solutions has become critical. Our hybrid approach combining **Random Forest** and **Deep Neural Network (DNN)** demonstrates a strong ability to predict water potability, providing essential tools for policymakers and water management authorities.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Features](#features)
- [Methodology](#methodology)
- [Models Implemented](#models-implemented)
- [Evaluation](#evaluation)
- [Results](#results)
- [How to Use](#how-to-use)
- [Future Work](#future-work)
- [Contributors](#contributors)
- [License](#license)

---

## 🧠 Overview

Access to safe drinking water is a global concern. Traditional water testing methods are often expensive and slow. We offer a **data-driven solution** using machine learning to classify water samples based on features like pH, hardness, solids, and chloramines. This can help identify unsafe water sources and prioritize treatment strategies.

---

## 📊 Dataset

- **Samples:** 3,276 water samples
- **Source:** [Kaggle - Water Potability Dataset](https://www.kaggle.com/datasets/adityakadiwal/water-potability)
- **Target Variable:** `Potability` (1 = potable, 0 = non-potable)
- **Missing Values:** Treated using **median imputation**

---

## 🧪 Features

Key features used in modeling:
- `pH`
- `Hardness`
- `Solids` (Total Dissolved Solids)
- `Chloramines`
- `Sulfate`
- `Conductivity`
- `Organic Carbon`
- `Trihalomethanes`
- `Turbidity`

All features were scaled using **Min-Max Normalization**.

---

## ⚙️ Methodology

1. **Data Cleaning**: Median imputation for missing values
2. **Outlier Detection**: Handled using robust statistics
3. **Feature Scaling**: Min-Max normalization
4. **Exploratory Data Analysis (EDA)**: Correlation analysis, boxplots, heatmaps
5. **Modeling**: Multiple models trained and evaluated
6. **Hybrid Approach**: Used Random Forest for feature extraction and DNN for classification

---

## 🤖 Models Implemented

| Model | Accuracy |
|-------|----------|
| Naive Bayes | ~61% |
| Decision Tree | ~77% |
| Support Vector Machine | Moderate accuracy, low recall |
| Random Forest | ~81% |
| XGBoost | ~79.6% |
| **Hybrid (Random Forest + DNN)** | **83.28%** (Best Performer) |

---

## 📈 Evaluation

Evaluation metrics used:
- **Accuracy**
- **Precision**
- **Recall**
- **F1-Score**
- **Confusion Matrix**

### 🔍 Hybrid Model Performance
- **Accuracy:** 83.28%
- **Precision:** 85.16%
- **Recall:** 81.67%
- **F1-Score:** 83.38%
- **Confusion Matrix:** Balanced classification of potable and non-potable samples

---

