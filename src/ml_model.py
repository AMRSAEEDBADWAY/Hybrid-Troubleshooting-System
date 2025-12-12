"""
Machine Learning Model Module (Transformer Enhanced)
===================================================
This module implements an improved text classification model using:
1. Transformer-based embeddings (SentenceTransformer) if available
2. Fallback to TF-IDF with character n-grams
3. Logistic Regression classifier
"""

import json
import os
import re
import joblib
import numpy as np
import warnings
from typing import Dict, List, Tuple, Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

# Try to import SentenceTransformer
try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMER_AVAILABLE = True
except ImportError:
    TRANSFORMER_AVAILABLE = False
    print("Warning: sentence-transformers not installed. Using TF-IDF fallback.")

# Suppress warnings
warnings.filterwarnings("ignore")


class BilingualTextPreprocessor:
    """Preprocesses English and Arabic text."""
    
    ARABIC_NORMALIZE = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا',
        'ى': 'ي', 'ئ': 'ي', 'ؤ': 'و', 'ة': 'ه', 'گ': 'ك'
    }
    
    ARABIC_STOPWORDS = {
        'في', 'من', 'على', 'إلى', 'عن', 'مع', 'هذا', 'هذه', 'التي', 'الذي',
        'كان', 'قد', 'لقد', 'ما', 'لا', 'أن', 'إن', 'كل', 'بعد', 'قبل',
        'عند', 'بين', 'هو', 'هي', 'هم', 'نحن', 'أنت', 'أنا', 'ذلك', 'تلك',
        'و', 'او', 'ثم', 'لكن', 'بل', 'حتى', 'منذ', 'خلال', 'حول', 'ضد'
    }
    
    def normalize_arabic(self, text: str) -> str:
        for old, new in self.ARABIC_NORMALIZE.items():
            text = text.replace(old, new)
        return re.sub(r'[\u064B-\u0652]', '', text)
    
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = self.normalize_arabic(text)
        text = re.sub(r'http\S+|www\.\S+', '', text)
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()
    
    def remove_stopwords(self, text: str) -> str:
        words = text.split()
        filtered = [w for w in words if w not in self.ARABIC_STOPWORDS]
        return ' '.join(filtered)
    
    def preprocess(self, text: str) -> str:
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        return text


class TransformerEncoder(BaseEstimator, TransformerMixin):
    """Wrapper for SentenceTransformer to use in sklearn Pipeline."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
        
    def fit(self, X, y=None):
        if TRANSFORMER_AVAILABLE:
            if self.model is None:
                self.model = SentenceTransformer(self.model_name)
        return self
        
    def transform(self, X):
        if TRANSFORMER_AVAILABLE and self.model:
            return self.model.encode(X)
        return np.zeros((len(X), 384)) # Fallback/Dummy


class TroubleshootingClassifier:
    """
    Hybrid Classifier that uses Transformer embeddings if available,
    otherwise falls back to enhanced TF-IDF.
    """
    
    CATEGORIES = [
        "overheating", "slow_performance", "battery_issues", "network_issues", 
        "startup_failure", "screen_problems", "storage_issues", "audio_problems",
        "app_crashes", "hardware_failure", "security"  # Added security
    ]
    
    MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'classifier.pkl')
    DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'training_data.json')
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.preprocessor = BilingualTextPreprocessor()
        self.use_transformer = TRANSFORMER_AVAILABLE
        
    def load_training_data(self) -> Tuple[List[str], List[str]]:
        """Load and preprocess training data."""
        if not os.path.exists(self.DATA_PATH):
            raise FileNotFoundError(f"Training data not found at {self.DATA_PATH}")
            
        with open(self.DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle dict format (e.g., {"examples": [...]})
        if isinstance(data, dict) and "examples" in data:
            data = data["examples"]
            
        texts = []
        labels = []
        
        for item in data:
            # Add English text
            if "text" in item:
                texts.append(self.preprocessor.preprocess(item["text"]))
                labels.append(item["category"])
            
            # Add Arabic text if available
            if "text_ar" in item:
                texts.append(self.preprocessor.preprocess(item["text_ar"]))
                labels.append(item["category"])
                
        return texts, labels
    
    def train_model(self) -> Dict:
        """Train the classifier."""
        print("Loading data...")
        X, y = self.load_training_data()
        
        print(f"Training on {len(X)} examples...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        if self.use_transformer:
            print("Using Transformer (Sentence-BERT) embeddings...")
            self.model = Pipeline([
                ('encoder', TransformerEncoder()),
                ('clf', LogisticRegression(max_iter=1000, class_weight='balanced', C=1.0))
            ])
        else:
            print("Using TF-IDF (Fallback)...")
            self.model = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=10000,
                    ngram_range=(1, 3),
                    analyzer='char_wb',
                    min_df=2,
                    sublinear_tf=True
                )),
                ('clf', LogisticRegression(max_iter=1000, class_weight='balanced', solver='saga'))
            ])
            
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        print(f"Model Accuracy: {accuracy:.4f}")
        self.save_model()
        
        return {
            "accuracy": accuracy,
            "report": report,
            "method": "Transformer" if self.use_transformer else "TF-IDF"
        }
    
    def save_model(self):
        """Save the trained model."""
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)
        # We only save the pipeline. TransformerEncoder will reload model on load if needed
        joblib.dump(self.model, self.MODEL_PATH)
        print(f"Model saved to {self.MODEL_PATH}")
        
    def load_model(self) -> bool:
        """Load the trained model."""
        if os.path.exists(self.MODEL_PATH):
            try:
                self.model = joblib.load(self.MODEL_PATH)
                self.is_trained = True
                
                # Check what kind of model it is
                if "encoder" in self.model.named_steps:
                    self.use_transformer = True
                    # Re-initialize the internal transformer model if needed
                    # Sklearn pipeline pickling usually handles this but for safety:
                    encoder = self.model.named_steps['encoder']
                    if encoder.model is None and TRANSFORMER_AVAILABLE:
                        encoder.model = SentenceTransformer(encoder.model_name)
                else:
                    self.use_transformer = False
                    
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        return False
    
    def predict_category(self, text: str) -> str:
        """Predict the category of a problem."""
        if not self.is_trained:
            if not self.load_model():
                raise ValueError("Model is not trained and cannot be loaded")
        
        processed_text = self.preprocessor.preprocess(text)
        return self.model.predict([processed_text])[0]
    
    def predict_with_confidence(self, text: str) -> Dict:
        """Predict category with confidence scores."""
        if not self.is_trained:
            if not self.load_model():
                raise ValueError("Model is not trained")
        
        processed_text = self.preprocessor.preprocess(text)
        probs = self.model.predict_proba([processed_text])[0]
        categories = self.model.classes_
        
        # Create dictionary of category -> probability
        scores = {cat: float(prob) for cat, prob in zip(categories, probs)}
        
        # Get best prediction
        best_category = max(scores, key=scores.get)
        confidence = scores[best_category]
        
        return {
            "predicted_category": best_category,
            "confidence": confidence,
            "all_scores": scores
        }
        
    def get_category_description(self, category: str) -> str:
        """"Get a user-friendly description of the category."""
        descriptions = {
            "overheating": "Device getting too hot / الجهاز بيسخن",
            "slow_performance": "System is slow or lagging / بطء في الجهاز",
            "battery_issues": "Battery drains fast or won't charge / مشاكل البطارية",
            "network_issues": "WiFi or internet connection issues / مشاكل النت",
            "startup_failure": "Device won't turn on or boot / الجهاز مش بيفتح",
            "screen_problems": "Display or screen issues / مشاكل الشاشة",
            "storage_issues": "Disk full or storage errors / المساحة ممتلئة",
            "audio_problems": "Sound or microphone issues / مشاكل الصوت",
            "app_crashes": "Applications freezing or crashing / البرامج بتقفل",
            "hardware_failure": "Physical component failure / عطل في قطع الجهاز",
            "security": "Virus, malware, or hacked account / فيروسات أو اختراق"
        }
        return descriptions.get(category, "Unknown Category")

if __name__ == "__main__":
    clf = TroubleshootingClassifier()
    print("Training model...")
    results = clf.train_model()
    print(f"Training complete. Method: {results['method']}")
    
    # Test
    test_texts = [
        "My laptop is burning hot", 
        "النت فاصل خالص",
        "Battery dies in 1 hour"
    ]
    
    print("\nTesting predictions:")
    for text in test_texts:
        pred = clf.predict_with_confidence(text)
        print(f"'{text}' -> {pred['predicted_category']} ({pred['confidence']:.2%})")
