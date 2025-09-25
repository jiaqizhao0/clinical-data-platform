import pandas as pd
import numpy as np
import sys
import os

# --- Get dataset name from CLI ---
if len(sys.argv) < 2:
    print("Usage: python preprocess.py <dataset_name.csv>")
    sys.exit(1)

dataset_name = sys.argv[1].replace(".csv", "")
raw_path = f"data/raw/{dataset_name}.csv"
cleaned_path = f"data/cleaned/{dataset_name}_cleaned.csv"


# Load dataset and treat -9999 and blanks as NaN
df = pd.read_csv(raw_path, na_values=["", " ", "-9999"])

df["subjectkey"] = df["subjectkey"].astype(str).str.strip()
df = df[df["subjectkey"] != "nan"]

# --- Fix interview date ---
if "interview_date" in df.columns:
    df["interview_date"] = pd.to_datetime(df["interview_date"], errors="coerce").dt.strftime("%m/%d/%Y")

# Convert sex to binary (M = 1, F = 0)
if df["sex"].astype(str).str.upper().isin(["M", "F"]).any():
    df["sex"] = df["sex"].map({"M": 1, "F": 2, "m": 1, "f": 2})

# Convert diagnosis to binary
if df["diagnosis"].astype(str).str.upper().isin(["TD", "ASD"]).any():
    df["diagnosis"] = df["diagnosis"].map({"TD": 0, "ASD": 1, "td": 0, "asd": 1})

# Save cleaned dataset
df.to_csv(cleaned_path, index=False)

print(f"✅ Cleaned dataset saved to {cleaned_path}")
print(f"📌 Rows with missing values are retained for QC review.")
