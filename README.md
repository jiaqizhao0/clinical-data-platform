# 🧠 Clinical Data Platform

An end-to-end data management pipeline for multi-site clinical research projects, built to reflect real-world data manager responsibilities in healthcare and translational neuroscience environments.

> 💼 Created by Jiaqi Zhao | Project duration: April 2025

---

## 🚀 Project Overview

This project simulates a full data management workflow including:
- Multi-site data intake
- Automated preprocessing and QC
- Streamlit-based interactive dashboards
- Git-powered version control and change tracking
- SOPs and compliance documentation

It mimics the responsibilities of a **Computational Health Informatics Data Manager II**.

---

## 🗃️ Folder Structure

```
clinical-data-platform/
├── data/
│   ├── raw/                  # Unprocessed input files
│   ├── cleaned/              # Processed data + QC reports
│   └── metadata/             # Data dictionary & IRB/DUA docs
│
├── pipeline/
│   ├── preprocess.py         # Data cleaning script
│   ├── qc.py                 # QC report generator
│   └── logging_utils.py      # File hashing + changelog
│
├── dashboard/
│   └── app.py                # Streamlit dashboard
│
├── docs/
│   ├── SOP_intake.md
│   ├── SOP_QC.md
│   ├── privacy_risk_assessment.md
│   ├── git_commit_log.txt
│   └── data_change_log.csv
│
├── notebooks/                # Optional: exploratory notebooks
├── .gitignore
├── README.md
└── CHANGELOG.md
```

---

## 🧪 Key Features

- ✅ Clean and validate incoming behavioral and demographic datasets
- ✅ Automatically generate quality control reports
- ✅ Track all data file changes via hash logging
- ✅ Maintain SOPs for compliance and training
- ✅ Visualize data distributions and summaries with Streamlit
- ✅ Include Git-based audit trail in the dashboard

---

## 📊 Live Dashboard

To launch:

```bash
streamlit run dashboard/app.py
```

---

## 📓 Version Tracking

Git history and file hash logs are available under the **🧾 Data Audit Trail** section in the dashboard.

Sample logs:

```
docs/git_commit_log.txt
docs/data_change_log.csv
```

---

## 📚 Documentation

See the `docs/` folder for:

```
SOPs on data intake, QC, and privacy
Version control strategy
Risk assessment policies
```

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

## ✅ To Do (Stretch Goals)

- [ ] Simulate EEG/MRI modality data
- [ ] Integrate automated data validation via `pandera`
- [ ] Add multi-user GitHub-based simulation with pull requests
