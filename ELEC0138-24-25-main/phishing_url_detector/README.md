# Phishing URL Detector

A machine learning-powered web application that analyzes URLs to detect potential phishing attempts, providing a risk assessment score.

## Features

- Real-time URL analysis
- Phishing probability score calculation
- Risk level categorization (Low, Medium, High, Extremely High)
- User-friendly web interface

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run detector.py
```

Then open your browser and go to [http://localhost:8501](http://localhost:8501) to access the application.

## How it Works

The application uses a machine learning model to analyze various features of a URL, including:
- Domain name characteristics
- URL length
- Presence of special characters (hyphens, underscores)
- Path structure
- Subdomain analysis
- TLD (Top-Level Domain) analysis

The model has been trained on a dataset of known phishing and legitimate URLs, and outputs a probability score indicating the likelihood that a given URL is a phishing attempt.

## Project Structure

- `detector.py`: Main Streamlit application
- `predict_helper.py`: Helper functions for URL feature extraction and prediction
- `requirements.txt`: Project dependencies
- `models/`: Contains the trained machine learning models
  - `logreg_pipeline_model.pkl`: Logistic Regression model (primary)
  - `nb_pipeline_model.pkl`: Naive Bayes model (alternative)
- `data/`: Contains the datasets used for training
  - `phishing_site_urls.csv`: Raw phishing URLs dataset
  - `processed_url_data.csv`: Processed dataset with extracted features

## Risk Levels

- 🟩 **Low Risk** (0.0-0.4): Likely safe
- 🟨 **Medium Risk** (0.4-0.7): Exercise caution
- 🟧 **High Risk** (0.7-0.9): Potentially dangerous
- 🟥 **Extremely High Risk** (0.9-1.0): Highly likely to be a phishing attempt

## Dependencies

- streamlit: Web application framework
- scikit-learn: Machine learning library
- pandas: Data manipulation
- nltk: Natural language processing
- tldextract: Domain extraction
- joblib: Model serialization/deserialization

## Note

This tool is intended for educational and informational purposes only. While it aims to identify potential phishing URLs, it should not be the sole basis for security decisions. Always exercise caution when clicking on unfamiliar links. 