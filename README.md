# Hybrid Intelligent Troubleshooting System

A comprehensive hybrid system combining Expert System, Machine Learning, and Interactive Chatbot for diagnosing computer and mobile device problems.

## Features

- **ML-Powered Classification**: TF-IDF + Logistic Regression for problem categorization
- **Expert System**: 90+ rules with forward/backward chaining inference
- **Interactive Chatbot**: Guided troubleshooting conversation
- **Explanation Facility**: Clear reasoning for diagnoses
- **Streamlit GUI**: Modern, user-friendly interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run main.py
```

## Project Structure

```
├── src/
│   ├── knowledge_base.py    # Rules and facts storage
│   ├── inference_engine.py  # Forward/backward chaining
│   ├── ml_model.py          # TF-IDF + Logistic Regression
│   ├── chatbot.py           # Conversation logic
│   └── gui.py               # Streamlit interface
├── data/
│   ├── training_data.json   # ML training examples
│   ├── computer_rules.json  # Computer troubleshooting rules
│   └── mobile_rules.json    # Mobile troubleshooting rules
├── models/                  # Saved ML models
├── main.py                  # Application entry point
└── requirements.txt
```

## Categories

The system recognizes these problem categories:
- Overheating
- Slow Performance
- Battery Issues
- Network Issues
- Startup Failure
- Screen Problems
- Storage Issues
- Audio Problems
- App Crashes
- Hardware Failure

## License

MIT License

