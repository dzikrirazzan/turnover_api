# load_data.py

# 📦 Load training data from CSV for ML prediction
# The CSV file is located in /ml_data/training_data.csv
# Assume project structure:
# ├── manage.py
# ├── ml_data/
# │   └── training_data.csv
# ├── predictions/
# │   └── load_data.py  ← you are here
# Use pandas to load the CSV and return a DataFrame

import pandas as pd
from pathlib import Path
from django.conf import settings

# Define the base directory of the Django project
# BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define the path to the CSV file
CSV_PATH = settings.BASE_DIR / "backend" / "ml_data" / "training_data.csv"

# Load the CSV into a pandas DataFrame
def load_training_data():
    try:
        df = pd.read_csv(CSV_PATH)
        print(f"✅ Loaded {len(df)} records from {CSV_PATH}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] File not found: {CSV_PATH}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return None

# Function to get sample data for testing
def get_sample_data(n=10):
    df = load_training_data()
    if df is not None:
        return df.head(n)
    return None
