import pandas as pd
import numpy as np
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset (Assuming CSV file with 'review' and 'rating' columns)
df = pd.read_csv('review_data.csv')

# Convert ratings into binary labels
def classify_rating(rating):
    return 1 if rating >= 4 else 0 if rating <= 2 else None

df['label'] = df['Rating'].apply(classify_rating)
df.dropna(inplace=True)  # Remove neutral reviews

# Text preprocessing
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text

df['cleaned_review'] = df['Reviews'].apply(clean_text)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['cleaned_review'], df['label'], test_size=0.2, random_state=42)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

joblib.dump(tfidf,"review_vectorizer.joblib")

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Evaluate model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

joblib.dump(model,"review_classifier.joblib")

print("Model and vectorizer saved successfully!")