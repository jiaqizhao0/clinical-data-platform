import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python qc.py <cleaned_dataset_path>")
    sys.exit(1)

cleaned_path = sys.argv[1]
dataset_name = os.path.basename(cleaned_path).replace("_cleaned.csv", "")
df = pd.read_csv(cleaned_path)

# --- Flag missing and outliers ---
df["missing_flag"] = df[["age", "IQ", "diagnosis"]].isnull().any(axis=1)
df["age_outlier"] = (df["age"] < 5) | (df["age"] > 64)
df["IQ_outlier"] = (df["IQ"] < 70) | (df["IQ"] > 145)


# --- Count summaries ---
n_total = len(df)
n_missing = df["missing_flag"].sum()
n_age_outliers = df["age_outlier"].sum()
n_IQ_outliers = df["IQ_outlier"].sum()

# --- Identify missing by field ---
missing_age = df[df["age"].isnull()][["subjectkey"]]
missing_IQ = df[df["IQ"].isnull()][["subjectkey"]]
missing_diag = df[df["diagnosis"].isnull()][["subjectkey"]]

missing_details = []
if not missing_age.empty:
    ids = ", ".join(missing_age["subjectkey"].astype(str).values)
    missing_details.append(f"- Missing age: {len(missing_age)} subject(s) → {ids}")
if not missing_IQ.empty:
    ids = ", ".join(missing_IQ["subjectkey"].astype(str).values)
    missing_details.append(f"- Missing IQ: {len(missing_IQ)} subject(s) → {ids}")
if not missing_diag.empty:
    ids = ", ".join(missing_diag["subjectkey"].astype(str).values)
    missing_details.append(f"- Missing diagnosis: {len(missing_diag)} subject(s) → {ids}")
missing_summary = "\n".join(missing_details) if missing_details else "None"

# --- Site, sex, scanner summaries ---
site_dist = df["site"].value_counts().to_string()
sex_dist = df["sex"].value_counts().to_string()
scanner_dist = df["scanner_type"].value_counts().to_string()
asd_dist = df["diagnosis"].value_counts().to_string()

# --- Assemble report text ---
report_lines = [
    f"🔍 QC Report for {Path(cleaned_path).name}",
    f"Total rows: {n_total}",
    "",
    "🔧 Missing Values Breakdown:",
    missing_summary,
    "",
    f"Age outliers (<5 or >64): {n_age_outliers}",
    f"IQ outliers (<70 or >145): {n_IQ_outliers}",
    "",
    "📊 Site Distribution:",
    site_dist,
    "",
    "📊 Sex Distribution (M = 1, F = 2):",
    sex_dist,
    "",
    "📊 Scanner Type Distribution:",
    scanner_dist,
    "",
    "📊 Diagnosis Distribution (ASD = 1, TD = 0):",
    asd_dist
]

report_text = "\n".join(report_lines)

# --- Save reports ---
report_path = f"data/cleaned/{dataset_name}_qc_report.txt"
with open(report_path, "w") as f:
    f.write("\n".join(report_lines))


flagged_path = f"data/cleaned/{dataset_name}_qc_flags.csv"
df_flags = df[df["missing_flag"] | df["age_outlier"] | df["IQ_outlier"]]
df_flags.to_csv(flagged_path, index=False)

print("✅ QC report generated:")
print(report_text)