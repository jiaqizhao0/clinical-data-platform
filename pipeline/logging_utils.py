import hashlib
import datetime
import os

def hash_file(filepath):
    """Generate MD5 hash of a file"""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def log_data_change(input_file, log_file="docs/data_change_log.csv"):
    """Log the hash and timestamp of data input"""
    file_hash = hash_file(input_file)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.basename(input_file)

    log_entry = f"{timestamp},{filename},{file_hash}\n"

    # Append to the log file
    with open(log_file, "a") as f:
        f.write(log_entry)

    print(f"🔐 Logged hash for {filename}")

def append_version_comparison_to_changelog(version1, version2, added, removed, changelog_path="CHANGELOG.md"):
    log_id = f"`{version1}` → `{version2}`"

    # Read existing log content
    if os.path.exists(changelog_path):
        with open(changelog_path, "r") as f:
            changelog = f.read()
    else:
        changelog = ""

    # Skip if already logged
    if log_id in changelog:
        print(f"⚠️ Comparison {log_id} already logged. Skipping.")
        return False

    # Generate new log entry
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

    with open(changelog_path, "a") as f:
        f.write(log_entry)

    print("✅ CHANGELOG.md updated from dashboard.")
    return True
