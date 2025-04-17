# 🧠 Clinical Data Platform

An end-to-end data management pipeline for multi-site clinical research projects, built to reflect real-world data manager responsibilities in healthcare and translational neuroscience environments.

> 💼 Created by Jiaqi Zhao | Project duration: April 2025

---

## 🚀 Project Overview

This project simulates a full data management workflow including:
- Multi-site data intake
- Automated preprocessing and QC
- Streamlit-based interactive dashboards
- Git-powered version control and file tracking
- Versioned dataset comparisons with automatic changelog logging
- SOPs and compliance documentation

---

## 🧪 Key Features

- ✅ Clean and validate incoming clinical/behavioral datasets
- ✅ Automatically generate QC reports (missing values, age range, site balance)
- ✅ Track file-level changes using hashing + timestamps
- ✅ View version history via Git commit logs
- ✅ Interactive dropdown comparison of dataset versions
- ✅ Automatic logging of comparison diffs to `CHANGELOG.md`
- ✅ Live dashboard built with Streamlit

---

## 📊 Live Dashboard

Launch it with:

```bash
streamlit run dashboard/app.py
```

You'll be able to:
- View cleaned dataset summaries
- Visualize distributions
- Compare any two dataset versions via dropdown
- See added/removed subjects
- Audit pipeline activity from Git + file logs

---

## 🔄 Dataset Version Comparison

Use the **🧾 Data Audit Trail** tab to:
- Select any two cleaned datasets
- View which subjects were added or removed
- Automatically log the result in `CHANGELOG.md` (only once per comparison)

---

## 🗃️ Folder Structure

```
clinical-data-platform/
├── data/
│   ├── raw/                  # Unprocessed files
│   ├── cleaned/              # Processed CSVs (v1, v2, etc.)
│   └── metadata/             # Data dictionary & site info
│
├── pipeline/
│   ├── preprocess.py         # Cleaning logic
│   ├── qc.py                 # QC checks
│   ├── logging_utils.py      # File hash + changelog utilities
│   └── compare_versions.py   # CLI version diff tool
│
├── dashboard/
│   └── app.py                # Streamlit dashboard app
│
├── docs/
│   ├── SOP_intake.md
│   ├── SOP_QC.md
│   ├── privacy_risk_assessment.md
│   ├── git_commit_log.txt
│   └── data_change_log.csv
│
├── notebooks/
├── .gitignore
├── README.md
└── CHANGELOG.md
```

---

## 🧾 Version Tracking & Audit Logs

- `CHANGELOG.md`: records dataset comparisons with timestamps
- `docs/git_commit_log.txt`: tracks Git commits
- `docs/data_change_log.csv`: logs file hash/timestamp for processed datasets

---

## 📎 Tech Stack

```
Python 3
Pandas
Matplotlib
Streamlit
Git / GitHub
```

---

## 👩🏻‍💻 About the Author

**Jiaqi Zhao**  
Former Data Core Lead & Clinical Research Coordinator  
Expert in data processing, automation, machine learning, and research infrastructure

---

## ✅ Stretch Goals

- [ ] Integrate modality-level QC (EEG/fMRI placeholders)
- [ ] Add column-level diff detection between dataset versions
- [ ] Export comparison results to PDF or downloadable reports
