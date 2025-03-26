import pandas as pd
import joblib
import random
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Load Data
df = pd.read_csv("customer_feature.csv")

# Drop unnecessary columns
df.drop(columns=['customer_id'], inplace=True, errors='ignore')
df = df.drop(columns=["occupation", "occupation_vector"], errors='ignore')

# Define Features (X) and Target (y)
X = df.drop(columns=['risk_score'])
y = df['risk_score']

# Handle Missing Values
X.fillna(0, inplace=True)

# Normalize Features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define Hyperparameter Grids
rf_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

xgb_params = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 6, 10],
    'subsample': [0.8, 1.0]
}

lr_params = {
    'C': [0.1, 1, 10, 100],
    'solver': ['liblinear', 'lbfgs']
}

# Define Models
models = {
    "RandomForest": RandomForestClassifier(random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42),
    "LogisticRegression": LogisticRegression(max_iter=500, random_state=42)
}

param_grids = {
    "RandomForest": rf_params,
    "XGBoost": xgb_params,
    "LogisticRegression": lr_params
}

best_model = None
best_score = 0
best_model_name = ""

# Hyperparameter Tuning & Model Selection
for name, model in models.items():
    print(f"\nTuning {name}...")
    search = RandomizedSearchCV(model, param_grids[name], n_iter=10, cv=3, scoring='accuracy', n_jobs=-1, random_state=42)
    search.fit(X_train, y_train)
    
    best_model_for_this = search.best_estimator_
    y_pred = best_model_for_this.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"Best {name} Accuracy: {acc:.4f}")
    
    if acc > best_score:
        best_score = acc
        best_model = best_model_for_this
        best_model_name = name

# Final Model Performance
print(f"\nBest Model Selected: {best_model_name}")
y_pred_best = best_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred_best)
precision = precision_score(y_test, y_pred_best, average='weighted')
recall = recall_score(y_test, y_pred_best, average='weighted')
f1 = f1_score(y_test, y_pred_best, average='weighted')

print(f"\nFinal Model Performance ({best_model_name}):")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred_best))

# Save Best Model
joblib.dump(best_model, "best_risk_classification_model.joblib")
print(f"\nBest model saved as 'best_risk_classification_model.joblib'")

