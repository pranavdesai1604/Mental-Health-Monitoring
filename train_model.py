# train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle

# Sample data (for demonstration purposes)
data = {
    'mood': ['happy', 'sad', 'angry', 'content', 'anxious', 'happy', 'sad', 'content'],
    'activity': [
        'went for a run', 
        'watched a sad movie', 
        'had an argument', 
        'read a book', 
        'felt nervous about work', 
        'went to a party', 
        'missed a deadline', 
        'spent time with family'
    ],
    'sleep': [7, 5, 6, 8, 4, 7, 6, 8],
    'label': ['positive', 'negative', 'negative', 'positive', 'negative', 'positive', 'negative', 'positive']
}

# Create DataFrame
df = pd.DataFrame(data)

# Combine text features into a single feature
df['combined'] = df['mood'] + " " + df['activity'] + " " + df['sleep'].astype(str)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df['combined'], df['label'], test_size=0.2, random_state=42)

# Pipeline for text processing and classification
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model
model_filename = 'models/mood_predictor.pkl'
with open(model_filename, 'wb') as model_file:
    pickle.dump(pipeline, model_file)

print(f"Model saved to {model_filename}")
