"""
Hybrid Intelligent Troubleshooting System
==========================================

Main entry point for the application.
Run with: streamlit run main.py

This system combines:
1. Machine Learning (TF-IDF + Logistic Regression) for problem classification
2. Expert System (90+ rules) for diagnosis and recommendations
3. Interactive Chatbot for guided troubleshooting
4. Streamlit Web Interface for user interaction
"""

import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check if running as script or via streamlit
def main():
    """Main entry point - launches Streamlit app."""
    print("=" * 60)
    print("Hybrid Intelligent Troubleshooting System")
    print("=" * 60)
    print("\nStarting application...")
    print("Please run with: streamlit run main.py")
    print("\nOr run the GUI directly with: streamlit run src/gui.py")
    print("=" * 60)
    
    # Import and run Streamlit app
    try:
        from src.gui import main as run_gui
        run_gui()
    except ImportError as e:
        print(f"\nError importing GUI module: {e}")
        print("\nMake sure you have all dependencies installed:")
        print("  pip install -r requirements.txt")
        print("\nThen run:")
        print("  streamlit run main.py")


def train_model():
    """Train the ML model."""
    print("Training ML Model...")
    from src.ml_model import TroubleshootingClassifier
    
    classifier = TroubleshootingClassifier()
    metrics = classifier.train_model()
    
    print(f"\nTraining complete!")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    return metrics


def test_inference():
    """Test the inference engine."""
    print("Testing Inference Engine...")
    from src.inference_engine import InferenceEngine
    
    engine = InferenceEngine()
    
    # Test case
    symptoms = {
        "fan_noise": "loud",
        "hot_surface": True
    }
    
    result = engine.diagnose(
        device_type="computer",
        category="overheating",
        symptoms=symptoms
    )
    
    print(f"\nDiagnosis: {result['diagnosis']['cause']}")
    print(f"Confidence: {result['diagnosis']['confidence']:.0%}")
    print(f"Solutions: {result['diagnosis']['solutions']}")
    
    return result


def test_chatbot():
    """Interactive chatbot test."""
    print("Starting Chatbot Test...")
    from src.chatbot import TroubleshootingChatbot
    
    chatbot = TroubleshootingChatbot()
    
    # Start conversation
    print("\n" + chatbot.get_greeting())
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            continue
        
        response = chatbot.process_message(user_input)
        print(f"\nAssistant: {response}")
        
        if "goodbye" in response.lower():
            break


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Hybrid Intelligent Troubleshooting System"
    )
    parser.add_argument(
        "--train", 
        action="store_true",
        help="Train the ML model"
    )
    parser.add_argument(
        "--test-inference",
        action="store_true",
        help="Test the inference engine"
    )
    parser.add_argument(
        "--test-chatbot",
        action="store_true",
        help="Run interactive chatbot test"
    )
    
    args = parser.parse_args()
    
    if args.train:
        train_model()
    elif args.test_inference:
        test_inference()
    elif args.test_chatbot:
        test_chatbot()
    else:
        main()
