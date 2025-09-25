import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime
import hashlib


if len(sys.argv) < 2:
    print("Usage: python snapshot_compare.py <dataset_name>")
    sys.exit(1)

dataset_id = sys.argv[1].replace(".csv", "")
raw_path = f"data/raw/{dataset_id}.csv"
snapshot_path = f"data/snapshots/{dataset_id}_snapshot.csv"
audit_path = f"data/audit/{dataset_id}_column_diff_history.csv"
hash_log_path = "docs/data_change_log.csv"

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Load current version
df_current = pd.read_csv(raw_path)
df_current["subjectkey"] = df_current["subjectkey"].astype(str).str.strip()
df_current = df_current[df_current["subjectkey"] != "nan"]
df_current.set_index("subjectkey", inplace=True)

# Check for existing snapshot and log initial hash
if not os.path.exists(snapshot_path):
    df_current.to_csv(snapshot_path)
    print("📥 Initial snapshot created.")

    # ➕ Log hash even if no changes
    file_hash = hash_file(raw_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp},{raw_path},{file_hash}\n"

    # Append safely to hash log
    if os.path.exists(hash_log_path):
        with open(hash_log_path, "rb+") as f:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            if last_char != b"\n":
                log_line = "\n" + log_line
    with open(hash_log_path, "a") as f:
        f.write(log_line)
    print("🔐 Initial file hash logged.")
    sys.exit(0)  # Done for new upload
    

# Load previous snapshot
df_prev = pd.read_csv(snapshot_path)
df_prev["subjectkey"] = df_prev["subjectkey"].astype(str).str.strip()
df_prev = df_prev[df_prev["subjectkey"] != "nan"]
df_prev.set_index("subjectkey", inplace=True)

# Detect changes
changes = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

old_keys = set(df_prev.index)
new_keys = set(df_current.index)

added_keys = new_keys - old_keys
removed_keys = old_keys - new_keys
common_keys = old_keys & new_keys

for subject in added_keys:
    changes.append({
        "timestamp": timestamp,
        "subjectkey": subject,
        "column": "ROW_STATUS",
        "old_value": "N/A",
        "new_value": "🆕 ADDED"
    })

for subject in removed_keys:
    changes.append({
        "timestamp": timestamp,
        "subjectkey": subject,
        "column": "ROW_STATUS",
        "old_value": "❌ REMOVED",
        "new_value": "N/A"
    })

df_old_common = df_prev.loc[list(common_keys)]
df_new_common = df_current.loc[list(common_keys)]

for subject in common_keys:
    row_old = df_old_common.loc[subject]
    row_new = df_new_common.loc[subject]
    for col in df_current.columns:
        old_val = row_old.get(col)
        new_val = row_new.get(col)
        if pd.isnull(old_val) and pd.isnull(new_val):
            continue
        if old_val != new_val:
            changes.append({
                "timestamp": timestamp,
                "subjectkey": subject,
                "column": col,
                "old_value": old_val,
                "new_value": new_val
            })

# Save results
if changes:
    df_changes = pd.DataFrame(changes)
    if os.path.exists(audit_path):
        df_existing = pd.read_csv(audit_path)
        df_combined = pd.concat([df_existing, df_changes], ignore_index=True)
        df_combined.to_csv(audit_path, index=False)
    else:
        df_changes.to_csv(audit_path, index=False)
    print(f"🔍 Changes detected in dataset `{dataset_id}` and logged to: {audit_path}")

    # Generate and log hash with timestamp
    file_hash = hash_file(raw_path)
    log_line = f"{timestamp},{raw_path},{file_hash}\n"
    if os.path.exists(hash_log_path):
        with open(hash_log_path, "rb+") as f:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            if last_char != b"\n":
                log_line = "\n" + log_line
    with open(hash_log_path, "a") as f:
        f.write(log_line)
    print("🔐 File hash logged.")
else:
    print("✅ No column-level changes detected.")

# Update snapshot
df_current.to_csv(snapshot_path)
print("📸 Snapshot updated.")
