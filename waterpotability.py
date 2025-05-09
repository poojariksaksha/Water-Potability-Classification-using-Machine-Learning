# -*- coding: utf-8 -*-
"""
**WATER POTABILITY USING WATER QUALITY METRICS**

*Introduction:* \\
Access to potable water—a fundamental human right—continues to be a pressing issue worldwide. Despite advancements, ensuring safe drinking water remains a challenge in many parts of the world. The aim of the project is to investigate the factors that significantly affect water potability.

The objective is to identify the major contributors to water safety using a dataset containing various water quality parameters and developing a machine learning model that best predicts whether a given water sample is suitable for drinking.

**PART 1:** \\
"Data Exploration" \\


---


*Reading the dataset.*


---

Dataset : "https://www.kaggle.com/datasets/adityakadiwal/water-potability/data"
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#Important libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
sns.set(style='darkgrid')
import warnings
warnings.filterwarnings('ignore')

#Important functions
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler

dataset_path = '/content/drive/My Drive/water_potability.csv'

dataset = pd.read_csv(dataset_path)

"""

---


Loading the data

---

"""

dataset

"""**PART 2:** \\
"Exploratory Data Analysis" \\


---


*The dataset comprises information regarding different water quality parameters, namely pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic Carbon, Trihalomethanes, and Turbidity. The target column is Potability, which represents if the water is fit for drinking: 1 being potable and 0 being non-potable. The dataset contains null values in columns ph, Sulfate, and Trihalomethanes, which need to be cleaned. The objective is to explore these parameters for identification of key drivers that affect potability and a predictive model to identify whether the water is safe to drink or not..*

---

"""

print(dataset.info())

"""

---


*The dataset used in this project contains information about various physical and chemical parameters of water samples, which are used to determine their potability.*


---

"""

dataset

"""

---


*This code counts the number of occurrences of each value ('0' or '1') in the 'Potability' column of the dataset. It then prints the result, showing how many samples are potable and non-potable.*

---

"""

potability_counts = dataset['Potability'].value_counts()
print(potability_counts)

# Number of values for each parameter
dataset.nunique()

"""


---
***Visualizing the data before filling the null values***


---

"""

correlation_with_potability = dataset.corr()['Potability'].sort_values(ascending=False)
plt.figure(figsize=(10, 6))
correlation_with_potability.drop('Potability').plot(kind='bar', color='red')
plt.title('Correlation of Features with Potability')
plt.xlabel('Features')
plt.ylabel('Correlation Coefficient')
plt.xticks(rotation=45, ha='right')
plt.show()

"""

---


*All the correlation values are quite close to zero, indicating that **no individual feature has a strong linear correlation** with whether water is potable or not.*


---

"""

print(correlation_with_potability)

plt.figure(figsize=(10, 8))
sns.heatmap(dataset.corr(), annot=True, linewidths=0.5)
plt.title('Correlation Between Various Attributes', fontsize=18)
plt.show()

"""*Given the poor linear correlations, the best method is to continue with more complex algorithms for the actual potability prediction, as linear models will not do well with this data. Here, the parameter 'Solids' have somewhat correlation with the dependent attribute "Potability".*

**PART 3:** \\
"Data Pre-Processing" \\


---
"""

# Null Values in the dataset
dataset.isnull().sum()

"""*We can see that ph, Sulfate and Trihalomethanes feature contains 491, 781 and 162 null values. The missing values are filled based on the median values for potable and non-potable water separately.*"""

dataset.describe()

# Creating individual boxplots for each feature to show outliers more clearly
numeric_features = dataset.select_dtypes(include=['float64', 'int64']).columns

plt.figure(figsize=(20, 20))

for i, feature in enumerate(numeric_features, 1):
    plt.subplot(4, 3, i)  # Create subplots for each feature
    sns.boxplot(y=feature, data=dataset)
    plt.title(f'Boxplot of {feature}')
    plt.ylabel('Value')

plt.tight_layout()
plt.show()

"""*Since the features are skewed and have outliers, using the median is generally safer for this type of dataset because it is less sensitive to extreme values and provides a more representative central value.*"""

cond=dataset['Potability']==0

dataset['ph'].fillna(cond.map({True:dataset.loc[dataset['Potability']==0]['ph'].median(),
                                False:dataset.loc[dataset['Potability']==1]['ph'].median()
                                }),inplace=True)

dataset['Sulfate'].fillna(cond.map({True:dataset.loc[dataset['Potability']==0]['Sulfate'].median(),
                                False:dataset.loc[dataset['Potability']==1]['Sulfate'].median()
                                }),inplace=True)

dataset['Trihalomethanes'].fillna(cond.map({True:dataset.loc[dataset['Potability']==0]['Trihalomethanes'].median(),
                                False:dataset.loc[dataset['Potability']==1]['Trihalomethanes'].median()
                                }),inplace=True)

dataset.isna().sum()

dataset.to_csv('water_potability_preprocessed.csv', index=False)

dataset_train = pd.read_csv("water_potability_preprocessed.csv")

dataset_train

"""**PART 4:** \\
"Data Scaling" \\


---

Min/Max Scaling:
"""

#Min-Max range before scaling
dataset_train.describe().T[['min','max']].T

input_cols = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
       'Organic_carbon', 'Trihalomethanes', 'Turbidity']

scaler = MinMaxScaler()
scaler.fit(dataset_train[input_cols])
dataset_train[input_cols] = scaler.transform(dataset_train[input_cols])
dataset_train

#Min-Max range after scaling
dataset_train.describe().T[['min','max']].T

"""**PART 5:** \\
"Data Modeling" \\


---

SVM
"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MinMaxScaler

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)

# Creating and fitting the SVM model
svm_model = SVC(kernel='rbf', random_state=41)  # Using RBF kernel (Radial Basis Function) as it's commonly effective for SVM
svm_model.fit(X_train, y_train)

# Making predictions
y_train_pred = svm_model.predict(X_train)
y_test_pred = svm_model.predict(X_test)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred, pos_label=1)
recall = recall_score(y_test, y_test_pred, pos_label=1)
f1 = f1_score(y_test, y_test_pred, pos_label=1)

print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix:\n", cm)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for SVM')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""RANDOM FOREST"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MinMaxScaler

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)

# Creating and fitting the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=41, max_depth=10, min_samples_split=3)
rf_model.fit(X_train, y_train)

# Making predictions
y_train_pred = rf_model.predict(X_train)
y_test_pred = rf_model.predict(X_test)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred, pos_label=1)
recall = recall_score(y_test, y_test_pred, pos_label=1)
f1 = f1_score(y_test, y_test_pred, pos_label=1)

# Printing the evaluation metrics
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

cm_rf = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for Random Forest Model:\n", cm_rf)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_rf, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for Random Forest Model')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""DECISION TREE"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)

# Creating and fitting the Decision Tree model
dt_model = DecisionTreeClassifier(random_state=41, max_depth=10, min_samples_split=3)
dt_model.fit(X_train, y_train)

# Making predictions
y_train_pred = dt_model.predict(X_train)
y_test_pred = dt_model.predict(X_test)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred, pos_label=1)
recall = recall_score(y_test, y_test_pred, pos_label=1)
f1 = f1_score(y_test, y_test_pred, pos_label=1)

# Printing the evaluation metrics
print("Decision Tree Model Evaluation Metrics:")
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix for Decision Tree Model
cm_dt = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for Decision Tree Model:\n", cm_dt)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_dt, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for Decision Tree Model')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""ANN"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)

# Building the ANN model
ann_model = Sequential()
ann_model.add(Dense(16, input_dim=X_train.shape[1], activation='relu'))  # Input layer with 16 nodes
ann_model.add(Dense(8, activation='relu'))  # Hidden layer with 8 nodes
ann_model.add(Dense(1, activation='sigmoid'))  # Output layer with 1 node for binary classification

# Compiling the model
ann_model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
ann_model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1, validation_data=(X_test, y_test))

# Making predictions
y_train_pred_prob = ann_model.predict(X_train)
y_test_pred_prob = ann_model.predict(X_test)

# Converting probabilities to binary predictions
y_train_pred = (y_train_pred_prob > 0.5).astype(int)
y_test_pred = (y_test_pred_prob > 0.5).astype(int)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)

# Printing the evaluation metrics
print("ANN Model Evaluation Metrics:")
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix for ANN Model
cm_ann = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for ANN Model:\n", cm_ann)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_ann, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for ANN Model')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""NAIVE BAYES"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)

# Creating and fitting the Naive Bayes model
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)

# Making predictions
y_train_pred = nb_model.predict(X_train)
y_test_pred = nb_model.predict(X_test)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)

# Printing the evaluation metrics
print("Naive Bayes Model Evaluation Metrics:")
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix for Naive Bayes Model
cm_nb = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for Naive Bayes Model:\n", cm_nb)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_nb, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for Naive Bayes Model')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""RANDOM + DEEP NEURAL NETWORK"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Handling class imbalance with SMOTE
smote = SMOTE(random_state=1)
X_balanced, y_balanced = smote.fit_resample(X_scaled, y)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.25, random_state=1)

# Step 1: Train a Random Forest Model with Hyperparameter Tuning
rf_model = RandomForestClassifier(random_state=41)

# Hyperparameter tuning with RandomizedSearchCV
param_distributions = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 3, 5],
    'max_features': ['sqrt', 'log2', None]
}

random_search = RandomizedSearchCV(rf_model, param_distributions, n_iter=10, cv=3, scoring='accuracy', random_state=1, n_jobs=-1, verbose=1)
random_search.fit(X_train, y_train)

# Train the Random Forest model with the best parameters
rf_model_best = random_search.best_estimator_
rf_model_best.fit(X_train, y_train)

# Step 2: Use Random Forest Model to Generate New Features
X_train_rf_features = rf_model_best.predict_proba(X_train)
X_test_rf_features = rf_model_best.predict_proba(X_test)

# Step 3: Train a Deep Neural Network with the Extracted Features
# Building the DNN Model with Dropout and Batch Normalization
dnn_model = Sequential()
dnn_model.add(Dense(32, input_dim=X_train_rf_features.shape[1], activation='relu'))
dnn_model.add(BatchNormalization())
dnn_model.add(Dropout(0.3))  # Adding dropout to prevent overfitting

dnn_model.add(Dense(16, activation='relu'))
dnn_model.add(BatchNormalization())
dnn_model.add(Dropout(0.3))  # Adding dropout

# Output layer for binary classification
dnn_model.add(Dense(1, activation='sigmoid'))

# Compiling the model
dnn_model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
dnn_model.fit(X_train_rf_features, y_train, epochs=100, batch_size=32, verbose=1, validation_data=(X_test_rf_features, y_test))

# Making predictions using the DNN model
y_train_pred_prob = dnn_model.predict(X_train_rf_features)
y_test_pred_prob = dnn_model.predict(X_test_rf_features)

# Converting probabilities to binary predictions
y_train_pred = (y_train_pred_prob > 0.5).astype(int)
y_test_pred = (y_test_pred_prob > 0.5).astype(int)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)

# Printing the evaluation metrics
print("Hybrid Model (Random Forest + Deep Neural Network) Evaluation Metrics:")
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix for Improved Model
cm_hybrid_improved = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for Hybrid Model:\n", cm_hybrid_improved)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_hybrid_improved, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for Hybrid Model')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""XGB CALSSIFIER WITH HYPERPARAMETER TUNING"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import xgboost as xgb

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)

# Step 1: Hyperparameter Tuning with GridSearchCV
xgb_clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')

# Define the parameter grid
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Using GridSearchCV to find the best hyperparameters
grid_search = GridSearchCV(estimator=xgb_clf, param_grid=param_grid, cv=3, scoring='accuracy', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Retrieve the best parameters and train the model using them
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

# Step 2: Train the XGBoost Classifier with Best Hyperparameters
best_xgb_clf = xgb.XGBClassifier(**best_params, use_label_encoder=False, eval_metric='logloss')
best_xgb_clf.fit(X_train, y_train)

# Making predictions
y_train_pred = best_xgb_clf.predict(X_train)
y_test_pred = best_xgb_clf.predict(X_test)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)

# Printing the evaluation metrics
print("XGBoost Classifier Model Evaluation Metrics:")
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix for XGBoost Classifier
cm_xgb = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for XGBoost Model:\n", cm_xgb)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_xgb, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for XGBoost Classifier')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""QDA"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)

# Creating and fitting the QDA model
qda_model = QuadraticDiscriminantAnalysis()
qda_model.fit(X_train, y_train)

# Making predictions
y_train_pred = qda_model.predict(X_train)
y_test_pred = qda_model.predict(X_test)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)

# Printing the evaluation metrics
print("Quadratic Discriminant Analysis Model Evaluation Metrics:")
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix for QDA Model
cm_qda = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for QDA Model:\n", cm_qda)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_qda, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for QDA Model')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""LSTM & MLP"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Flatten
from tensorflow.keras.optimizers import Adam

# Assuming 'dataset_train' is your DataFrame after handling missing values

# Separating features and target
X = dataset_train.drop('Potability', axis=1)
y = dataset_train['Potability']

# Scaling the features using Min-Max Scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Reshaping the data for LSTM input
# LSTM expects data in 3D shape: (samples, timesteps, features)
X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y, test_size=0.25, random_state=1)

# Building the LSTM + MLP Hybrid Model
model = Sequential()

# LSTM layer for extracting features
model.add(LSTM(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=False))

# Flatten and connect to MLP layers
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))

# Output layer for binary classification
model.add(Dense(1, activation='sigmoid'))

# Compiling the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1, validation_data=(X_test, y_test))

# Making predictions using the LSTM + MLP model
y_train_pred_prob = model.predict(X_train)
y_test_pred_prob = model.predict(X_test)

# Converting probabilities to binary predictions
y_train_pred = (y_train_pred_prob > 0.5).astype(int)
y_test_pred = (y_test_pred_prob > 0.5).astype(int)

# Evaluating the model accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Calculating precision, recall, and f1-score for test data
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)

# Printing the evaluation metrics
print("Hybrid LSTM + MLP Model Evaluation Metrics:")
print("Accuracy of training data:", train_accuracy)
print("Accuracy of test data:", test_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Confusion Matrix for LSTM + MLP Model
cm_lstm_mlp = confusion_matrix(y_test, y_test_pred)
print("Confusion Matrix for LSTM + MLP Model:\n", cm_lstm_mlp)

# Visualizing the Confusion Matrix using Seaborn heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_lstm_mlp, annot=True, cmap='Blues', fmt='g')
plt.title('Confusion Matrix for Hybrid LSTM + MLP Model')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""Analysis of the Models:"""

# Data for the bar chart
models = ['SVM', 'Random Forest', 'Decision Tree', 'ANN', 'Naive Bayes', 'Hybrid Model', 'XGBoost', 'QDA', 'Hybrid LSTM + MLP']
train_accuracies = [0.707, 0.930, 0.893, 0.648, 0.634, 1.0, 0.936, 0.684, 0.695]
test_accuracies = [0.650, 0.810, 0.768, 0.615, 0.612, 0.831, 0.796, 0.676, 0.654]

# Create a bar chart to display training and testing accuracies for each model
plt.figure(figsize=(14, 8))
bar_width = 0.35
x = range(len(models))

# Plotting training accuracies
plt.bar(x, train_accuracies, width=bar_width, color='blue', alpha=0.6, label='Training Accuracy')

# Plotting testing accuracies, offset to the right
plt.bar([p + bar_width for p in x], test_accuracies, width=bar_width, color='orange', alpha=0.6, label='Test Accuracy')

# Labels and title
plt.xlabel('Models', fontsize=14)
plt.ylabel('Accuracy', fontsize=14)
plt.title('Training and Testing Accuracy of Different Models', fontsize=16, weight='bold')
plt.xticks([p + bar_width / 2 for p in x], models, rotation=45, ha='right')
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()

# Model names
models = [
    'SVM', 'Random Forest', 'Decision Tree', 'ANN', 'Naive Bayes',
    'Improved Hybrid (RF + DNN)', 'XGBoost', 'QDA', 'Hybrid LSTM + MLP'
]

precisions = [
    0.7938, 0.9017, 0.7770, 0.7736, 0.6048, 0.8426, 0.8391, 0.7516, 0.6649
]

recalls = [
    0.2238, 0.6134, 0.6279, 0.1192, 0.2180, 0.8246, 0.6366, 0.3430, 0.3576
]

f1_scores = [
    0.3492, 0.7301, 0.6945, 0.2065, 0.3205, 0.8335, 0.7240, 0.4711, 0.4650
]

# Setting up bar width and positions
bar_width = 0.2
index = np.arange(len(models))

# Plotting Precision, Recall, and F1 Scores for Each Model
plt.figure(figsize=(15, 6))

plt.bar(index - bar_width, precisions, bar_width, label='Precision', color='green')
plt.bar(index, recalls, bar_width, label='Recall', color='orange')
plt.bar(index + bar_width, f1_scores, bar_width, label='F1-Score', color='red')

plt.xticks(index, models, rotation=45, ha='right')
plt.ylabel('Scores')
plt.title('Precision, Recall, and F1-Scores of Different Models')
plt.legend()
plt.tight_layout()
plt.show()
