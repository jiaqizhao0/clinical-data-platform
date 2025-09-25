import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import glob
import subprocess
import numpy as np
from scipy.stats import norm

st.set_page_config(page_title="Clinical Data QC Dashboard", layout="centered")

# --- Upload Dataset ---
st.sidebar.markdown("### 📤 Upload a New Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    uploaded_name = uploaded_file.name.replace(" ", "_")
    save_path = os.path.join("data/raw", uploaded_name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        df_uploaded = pd.read_csv(save_path)
        required_cols = {"subjectkey", "age", "IQ", "diagnosis"}
        if not required_cols.issubset(df_uploaded.columns):
            st.sidebar.error("Missing required columns.")
            os.remove(save_path)
            st.stop()
        else:
            st.sidebar.success(f"✅ Uploaded and saved as: {uploaded_name}")
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")
        os.remove(save_path)
        st.stop()

# --- Dataset Selection ---
available_datasets = sorted(glob.glob("data/raw/*.csv"))
dataset_choices = [os.path.basename(f) for f in available_datasets]

if not dataset_choices:
    st.stop()

# Retain selection across reruns
if "selected_dataset" not in st.session_state:
    st.session_state["selected_dataset"] = dataset_choices[0]

selected_file = st.sidebar.selectbox("📂 Select a Dataset", dataset_choices, index=dataset_choices.index(st.session_state["selected_dataset"]))
st.session_state["selected_dataset"] = selected_file
dataset_id = selected_file.replace(".csv", "")

# --- Paths ---
raw_path = f"data/raw/{dataset_id}.csv"
cleaned_path = f"data/cleaned/{dataset_id}_cleaned.csv"
qc_report_path = f"data/cleaned/{dataset_id}_qc_report.txt"
flagged_path = f"data/cleaned/{dataset_id}_qc_flags.csv"
diff_log_path = f"data/audit/{dataset_id}_column_diff_history.csv"
hash_log_path = "docs/data_change_log.csv"

# --- Preprocessing Runner (only runs once per dataset switch) ---
if st.session_state.get("last_run_dataset") != dataset_id:
    try:
        subprocess.run(["python", "pipeline/preprocess_qc_runner.py", dataset_id], check=True)
        subprocess.run(["python", "pipeline/snapshot_compare.py", dataset_id], check=True)
        st.session_state["last_run_dataset"] = dataset_id
    except Exception as e:
        st.warning(f"⚠️ Pipeline error: {e}")

# --- Tab Navigation ---
tabs = ["📋 Data Overview", "🧪 Data QC", "🧾 Data Audit Trail"]
selected_tab = st.sidebar.radio("Choose a Page", tabs)

# --- Page 1: Data Overview ---
if selected_tab == "📋 Data Overview":
    st.title("📋 Data Overview")
    

    try:
        
        df_raw = pd.read_csv(raw_path)
        df_clean = pd.read_csv(cleaned_path)

        st.subheader("🆚 Raw vs Cleaned Dataset Preview")

        st.markdown("###  Raw Dataset")
        st.dataframe(df_raw, height=300)

        st.markdown("###  Cleaned Dataset")
        st.dataframe(df_clean, height=300)

        st.markdown("---")
        st.subheader("🎯 Age Distribution (Cleaned Data)")

        fig_age, ax_age = plt.subplots()
        df_clean["age"].dropna().hist(bins=15, density=True, alpha=0.6, ax=ax_age, color="skyblue", edgecolor="black")

        # Overlay normal distribution curve
        age_mean = df_clean["age"].mean()
        age_std = df_clean["age"].std()
        x_vals = np.linspace(df_clean["age"].min(), df_clean["age"].max(), 100)
        ax_age.plot(x_vals, norm.pdf(x_vals, age_mean, age_std), color="red", lw=2, label="Normal Dist")
        ax_age.set_title("Age Histogram with Normal Curve")
        ax_age.legend()
        st.pyplot(fig_age)

        st.subheader("🧠 IQ Distribution (Cleaned Data)")

        fig_iq, ax_iq = plt.subplots()
        df_clean["IQ"].dropna().hist(bins=15, density=True, alpha=0.6, ax=ax_iq, color="lightgreen", edgecolor="black")

        # Overlay normal distribution curve
        iq_mean = df_clean["IQ"].mean()
        iq_std = df_clean["IQ"].std()
        x_vals = np.linspace(df_clean["IQ"].min(), df_clean["IQ"].max(), 100)
        ax_iq.plot(x_vals, norm.pdf(x_vals, iq_mean, iq_std), color="red", lw=2, label="Normal Dist")
        ax_iq.set_title("IQ Histogram with Normal Curve")
        ax_iq.legend()
        st.pyplot(fig_iq)

        st.subheader("🏥 Site, Scanner, and Sex Distributions")

        # --- Site Distribution ---
        fig_site, ax_site = plt.subplots()
        df_clean["site"].value_counts().plot(kind="barh", ax=ax_site, color="lightcoral", edgecolor="black")
        ax_site.set_title("Site Distribution")
        st.pyplot(fig_site)

        # --- Scanner Type Distribution ---
        if "scanner_type" in df_clean.columns:
            fig_scanner, ax_scanner = plt.subplots()
            df_clean["scanner_type"].value_counts().plot(kind="barh", ax=ax_scanner, color="mediumseagreen", edgecolor="black")
            ax_scanner.set_title("Scanner Type Distribution")
            st.pyplot(fig_scanner)

        # --- Sex Distribution (as pie chart) ---
        fig_sex, ax_sex = plt.subplots()
        sex_counts = df_clean["sex"].map({1: "Male", 2: "Female"}).value_counts()
        ax_sex.pie(sex_counts, labels=sex_counts.index, autopct="%1.1f%%", startangle=90, colors=["#8ecae6", "#f7a1a1"])
        ax_sex.set_title("Sex Distribution")
        st.pyplot(fig_sex)

        # --- ASD vs TD Pie Chart ---
        st.subheader("🧠 ASD Diagnosis Distribution")
        if "diagnosis" in df_clean.columns:
            fig_diag, ax_diag = plt.subplots()
            diag_counts = df_clean["diagnosis"].map({1: "ASD", 0: "TD"}).value_counts()
            ax_diag.pie(diag_counts, labels=diag_counts.index, autopct="%1.1f%%", startangle=90, colors=["#ffb703", "#8ecae6"])
            ax_diag.set_title("ASD vs TD Distribution")
            st.pyplot(fig_diag)

    except Exception as e:
        st.warning(f"Could not load datasets: {e}")

# --- Tab: QC ---
elif selected_tab == "🧪 Data QC":
    st.title("🧪 Data Quality Control")

    try:
        with open(qc_report_path) as f:
            st.text_area("📋 QC Report", f.read(), height=300)

        with open(qc_report_path, "rb") as f:
            st.download_button(label="📥 Download QC Report", data=f, 
            file_name=os.path.basename(qc_report_path))

        df_flags = pd.read_csv(flagged_path)
        if not df_flags.empty:
            st.subheader("⚠️ Flagged Rows")
            st.dataframe(df_flags)
        else:
            st.success("No missing or outlier rows.")

    except Exception as e:
        st.warning(f"Could not load QC report: {e}")

# --- Tab: Audit Trail ---
elif selected_tab == "🧾 Data Audit Trail":
    st.title("🧾 Data Audit Trail")
    st.markdown("This section tracks all pipeline activity, version comparisons, and column-level changes.")
    
    
    # --- Column-level change history ---
    st.subheader("🔄 Change History")

    
    diff_path = diff_log_path

    if os.path.exists(diff_path):
        df_diff = pd.read_csv(diff_path)
        if not df_diff.empty and "column" in df_diff.columns:
            # Corrected filter logic with parentheses
            added = df_diff[(df_diff["column"] == "ROW_STATUS") & (df_diff["new_value"] == "🆕 ADDED")]
            removed = df_diff[(df_diff["column"] == "ROW_STATUS") & (df_diff["old_value"] == "❌ REMOVED")]
            modified = df_diff[df_diff["column"] != "ROW_STATUS"]

            if not added.empty:
                st.markdown("### Newly Added Subjects")
                st.dataframe(added[["timestamp", "subjectkey"]])

            if not removed.empty:
                st.markdown("### Removed Subjects")
                st.dataframe(removed[["timestamp", "subjectkey"]])

            if not modified.empty:
                st.markdown("### Modified Cell Values")
                st.dataframe(modified[["timestamp", "subjectkey", "column", "old_value", "new_value"]])
        else:
            st.info("No changes detected.")
    else:
        st.info("🔍 No column-level change history available yet for this dataset.")
    
    # Show file hash log
    st.subheader("🔐 File Hash Log")
    try:
        df_hash = pd.read_csv("docs/data_change_log.csv", names=["Timestamp", "Filename", "File Hash"], header=None)
        df_hash = df_hash[df_hash["Filename"].str.contains(dataset_id)]
        st.dataframe(df_hash.reset_index(drop=True))
    except FileNotFoundError:
        st.warning("No data change log found.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Jiaqi")
