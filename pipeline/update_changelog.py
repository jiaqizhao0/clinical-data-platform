import pandas as pd
from datetime import datetime
import os

def get_subject_diff(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    df1["subject_id"] = df1["subject_id"].str.strip()
    df2["subject_id"] = df2["subject_id"].str.strip()

    ids1 = set(df1["subject_id"])
    ids2 = set(df2["subject_id"])

    added = ids2 - ids1
    removed = ids1 - ids2

    return added, removed

def append_to_changelog(version1, version2, added, removed):
    log_path = "CHANGELOG.md"
    log_id = f"`{version1}` → `{version2}`"

    # Read existing log content
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            changelog = f.read()
    else:
        changelog = ""

    # Check if this comparison is already logged
    if log_id in changelog:
        print(f"⚠️ Comparison {log_id} already exists in CHANGELOG. Skipping.")
        return

    # Append log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n## 🔄 Comparison: {log_id} — {timestamp}\n"

    body = []
    if added:
        body.append(f"- 🆕 Added subjects: {', '.join(sorted(added))}")
    if removed:
        body.append(f"- ❌ Removed subjects: {', '.join(sorted(removed))}")
    if not body:
        body.append("- ✅ No changes in subject IDs")

    log_entry = header + "\n".join(body) + "\n"

    with open(log_path, "a") as f:
        f.write(log_entry)

    print("✅ CHANGELOG.md updated!")


if __name__ == "__main__":
    file1 = "data/cleaned/clinical_data_cleaned.csv"
    file2 = "data/cleaned/clinical_data_v2_cleaned.csv"

    added, removed = get_subject_diff(file1, file2)
    append_to_changelog(os.path.basename(file1), os.path.basename(file2), added, removed)

