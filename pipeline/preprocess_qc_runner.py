import subprocess
import sys
import hashlib
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python preprocess_qc_runner.py <dataset_name>")
    sys.exit(1)

dataset_id = sys.argv[1].replace(".csv", "")
raw_path = f"data/raw/{dataset_id}.csv"
cleaned_path = f"data/cleaned/{dataset_id}_cleaned.csv"
hash_log_path = "docs/data_change_log.csv"

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Get current hash
current_hash = get_file_hash(raw_path)

# Load last logged hash (if any)
last_hash = None
if os.path.exists(hash_log_path):
    with open(hash_log_path, "r") as f:
        lines = f.readlines()
        for line in reversed(lines):
            if raw_path in line:
                last_hash = line.strip().split(",")[-1]
                break

# Only run preprocess + QC if the raw file has changed
if last_hash != current_hash:
    try:
        print(f"🧠 Raw file for {dataset_id} has changed — running preprocessing and QC...")
        subprocess.run([sys.executable, "pipeline/preprocess.py", dataset_id], check=True)
        subprocess.run([sys.executable, "pipeline/qc.py", cleaned_path], check=True)
        print("✅ Preprocessing and QC completed.")
    except Exception as e:
        print(f"⚠️ Error running preprocessing or QC: {e}")
else:
    print(f"✅ Raw data for {dataset_id} unchanged — skipping preprocess and QC.")
