# predict_helper.py

import pandas as pd
import re
import tldextract
from urllib.parse import urlparse
from nltk.tokenize import RegexpTokenizer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

# ✅ Custom transformer used in pipeline
class Converter(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X.values.ravel()

# ✅ Tokenizer
tokenizer = RegexpTokenizer(r"[A-Za-z]+")

def parse_url(url: str):
    parsed = urlparse(url if url.startswith("http") else "http://" + url)
    return parsed

def get_num_subdomains(netloc):
    subdomain = tldextract.extract(netloc).subdomain
    return subdomain.count('.') + 1 if subdomain else 0

def tokenize_domain(netloc):
    parts = tldextract.extract(netloc)
    domain_part = f"{parts.subdomain}.{parts.domain}"
    return " ".join(tokenizer.tokenize(domain_part))

def tokenize_path(path):
    return " ".join(tokenizer.tokenize(path))

def predict_url_phishing_proba(url: str, model: Pipeline, show_output: bool = True) -> float:
    parsed = parse_url(url)
    netloc = parsed.netloc
    path = parsed.path

    sample = {
        'length': len(url),
        'tld': tldextract.extract(netloc).suffix or 'None',
        'is_ip': bool(re.fullmatch(r"\d+\.\d+\.\d+\.\d+", netloc)),
        'domain_hyphens': netloc.count('-'),
        'domain_underscores': netloc.count('_'),
        'path_hyphens': path.count('-'),
        'path_underscores': path.count('_'),
        'slashes': path.count('/'),
        'full_stops': path.count('.'),
        'num_subdomains': get_num_subdomains(netloc),
        'domain_tokens': tokenize_domain(netloc),
        'path_tokens': tokenize_path(path),
    }

    df = pd.DataFrame([sample])

    if hasattr(model.named_steps["classifier"], "predict_proba"):
        proba = model.predict_proba(df)[0][1]
    else:
        raise ValueError("Model does not support predict_proba")

    if show_output:
        print(f"\n🔍 URL: {url}")
        print(f"🎯 Phishing Probability: {proba:.3f}")
        if proba >= 0.9:
            print("🟥 Risk: Extremely High")
        elif proba >= 0.7:
            print("🟧 Risk: High")
        elif proba >= 0.4:
            print("🟨 Risk: Medium")
        else:
            print("🟩 Risk: Low")

    return proba