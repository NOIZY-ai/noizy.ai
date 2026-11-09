#!/usr/bin/env python3
"""
Machine Learning email categorization
"""

import json
import sys
from pathlib import Path

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    import joblib
except ImportError:
    print("Installing ML dependencies...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "scikit-learn", "joblib"], check=False)

class EmailCategorizer:
    def __init__(self, model_path=None):
        self.model_path = model_path or Path(__file__).parent.parent / "data" / "ml_model.pkl"
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.categories = {}

    def train(self, emails_data):
        """Train categorizer on email samples"""
        texts = [email.get("subject", "") + " " + email.get("body", "")[:500] for email in emails_data]
        labels = [email.get("category", "uncategorized") for email in emails_data]

        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)
        self.save()

    def predict(self, subject, body=""):
        """Predict category for email"""
        text = subject + " " + body[:500]
        X = self.vectorizer.transform([text])
        return self.classifier.predict(X)[0]

    def save(self):
        """Save model to disk"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump((self.vectorizer, self.classifier), str(self.model_path))

    def load(self):
        """Load model from disk"""
        if self.model_path.exists():
            self.vectorizer, self.classifier = joblib.load(str(self.model_path))
            return True
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "predict":
        subject = sys.argv[2] if len(sys.argv) > 2 else ""
        body = sys.argv[3] if len(sys.argv) > 3 else ""

        categorizer = EmailCategorizer()
        if categorizer.load():
            category = categorizer.predict(subject, body)
            print(json.dumps({"category": category}))

