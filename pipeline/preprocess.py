from pipeline.logging_utils import log_data_change
import pandas as pd
import os
import sys

# Support version argument
input_file = sys.argv[1] if len(sys.argv) > 1 else "data/raw/clinical_data.csv"
output_file = input_file.replace("raw", "cleaned").replace(".csv", "_cleaned.csv")

# Load raw data
df = pd.read_csv(input_file)
df["subject_id"] = df["subject_id"].str.strip()

# Remove invalid IQ values
df_clean = df[df["IQ"] != -9999].copy()

# Convert sex to binary
df_clean["sex"] = df_clean["sex"].map({"F": 0, "M": 1})

# Save cleaned file
os.makedirs("data/cleaned", exist_ok=True)
df_clean.to_csv(output_file, index=False)
log_data_change(input_file)

print("✅ Preprocessing complete. Cleaned data saved.")

