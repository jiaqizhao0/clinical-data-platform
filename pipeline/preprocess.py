import pandas as pd
import os

# Load raw data
df = pd.read_csv("data/raw/clinical_data.csv")

# Remove invalid IQ values
df_clean = df[df["IQ"] != -9999].copy()

# Convert sex to binary
df_clean["sex"] = df_clean["sex"].map({"F": 0, "M": 1})

# Save cleaned file
os.makedirs("data/cleaned", exist_ok=True)
df_clean.to_csv("data/cleaned/clinical_data_cleaned.csv", index=False)

print("✅ Preprocessing complete. Cleaned data saved.")

