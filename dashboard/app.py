import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipeline.logging_utils import append_version_comparison_to_changelog

# Load cleaned data
df = pd.read_csv("data/cleaned/clinical_data_cleaned.csv")

st.set_page_config(page_title="Clinical Data QC Dashboard", layout="centered")

# --- Sidebar navigation ---
page = st.sidebar.selectbox("Choose a page", ["📋 Data Overview", "🧾 Data Audit Trail"])


if page == "📋 Data Overview":
    st.title("🧪 Clinical Data QC Dashboard")
    st.markdown("A quick view of your cleaned dataset, distributions, and summary stats.")

    # Show table
    st.subheader("📋 Cleaned Dataset Preview")
    st.dataframe(df)

    # Site distribution
    st.subheader("🏥 Site Distribution")
    site_counts = df["site"].value_counts()
    st.bar_chart(site_counts)

    # Age histogram
    st.subheader("🎯 Age Distribution")
    fig, ax = plt.subplots()
    df["age"].hist(ax=ax, bins=10, color="skyblue", edgecolor="black")
    st.pyplot(fig)

    # Summary stats
    st.subheader("🧠 IQ Summary Statistics")
    st.write(df["IQ"].describe())

elif page == "🧾 Data Audit Trail":
    st.title("🧾 Data Audit Trail")
    st.markdown("This section tracks all pipeline activity and file history.")

    # Show Git commit log
    st.subheader("📜 Git Commit History")
    try:
        with open("docs/git_commit_log.txt", "r") as f:
            git_log = f.read()
            st.code(git_log, language="markdown")
    except FileNotFoundError:
        st.warning("No git log available.")

    # Show file hash log
    st.subheader("🔐 File Hash Log")
    try:
        df_hash = pd.read_csv("docs/data_change_log.csv", names=["Timestamp", "Filename", "File Hash"])
        st.dataframe(df_hash)
    except FileNotFoundError:
        st.warning("No data change log found.")
    # --- Interactive version comparison ---
    st.subheader("🧬 Dataset Version Comparison")

    # Find available cleaned files
    cleaned_files = sorted(glob.glob("data/cleaned/*_cleaned.csv"))
    file_labels = [os.path.basename(f) for f in cleaned_files]

    if len(cleaned_files) < 2:
        st.warning("Need at least 2 cleaned datasets to compare.")
    else:
        v1_file = st.selectbox("🔹 Select Base Version:", file_labels, index=0)
        v2_file = st.selectbox("🔸 Select Comparison Version:", file_labels, index=1)

        df_v1 = pd.read_csv(f"data/cleaned/{v1_file}")
        df_v2 = pd.read_csv(f"data/cleaned/{v2_file}")

        df_v1["subject_id"] = df_v1["subject_id"].str.strip()
        df_v2["subject_id"] = df_v2["subject_id"].str.strip()

        v1_ids = set(df_v1["subject_id"])
        v2_ids = set(df_v2["subject_id"])

        added_ids = v2_ids - v1_ids
        removed_ids = v1_ids - v2_ids

        df_added = df_v2[df_v2["subject_id"].isin(added_ids)].copy()
        df_removed = df_v1[df_v1["subject_id"].isin(removed_ids)].copy()

        df_added["change_type"] = "🆕 Added"
        df_removed["change_type"] = "❌ Removed"

        if not df_added.empty or not df_removed.empty:
            st.success(f"Comparison result between `{v1_file}` and `{v2_file}`")
            st.dataframe(pd.concat([df_added, df_removed]))

            # Log to CHANGELOG.md (only if not already logged)
            if append_version_comparison_to_changelog(v1_file, v2_file, added_ids, removed_ids):
                st.success("✅ CHANGELOG.md has been updated automatically.")
            else:
                st.info("ℹ️ This comparison was already logged in CHANGELOG.md.")
        else:
            st.info("✅ No differences in subject IDs between versions.")	
    

st.markdown("---")
st.caption("Built with ❤️ by Jiaqi")

