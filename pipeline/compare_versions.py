import pandas as pd

# Load both versions
v1 = pd.read_csv("data/cleaned/clinical_data_cleaned.csv")
v2 = pd.read_csv("data/cleaned/clinical_data_v2_cleaned.csv")

# Strip and standardize subject_id
v1["subject_id"] = v1["subject_id"].str.strip()
v2["subject_id"] = v2["subject_id"].str.strip()

# Compare sets
v1_ids = set(v1["subject_id"])
v2_ids = set(v2["subject_id"])

added = v2_ids - v1_ids
removed = v1_ids - v2_ids

added_df = v2[v2["subject_id"].isin(added)]
removed_df = v1[v1["subject_id"].isin(removed)]

# Save to CSV for dashboard display
added_df["change_type"] = "Added"
removed_df["change_type"] = "Removed"
diff_df = pd.concat([added_df, removed_df])
diff_df.to_csv("data/version_diff.csv", index=False)

# Optional printout
print("🆕 Subjects Added:")
print(added_df)

print("\n❌ Subjects Removed:")
print(removed_df)


