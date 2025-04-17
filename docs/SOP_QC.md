# 🔍 SOP: Data Quality Control (QC)

**Purpose:**  
To standardize quality control practices for multi-site clinical data.

---

## 1. QC Pipeline Overview
- Executed using `pipeline/qc.py`
- Outputs terminal report + `qc_report.txt`

---

## 2. QC Checks Performed
- Missing value analysis
- Age range validation (5–100 years)
- Site distribution balance
- IQ summary statistics

---

## 3. Actionable Thresholds
- If more than 10% of rows have missing IQ, raise issue
- Outlier age values must be flagged for follow-up

---

## 4. Review & Documentation
- Run `qc.py` after each data update
- Upload `qc_report.txt` to `data/cleaned/` and log changes in `CHANGELOG.md`
