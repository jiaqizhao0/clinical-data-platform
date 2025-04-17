# 📥 SOP: Data Intake

**Purpose:**  
To outline standardized procedures for receiving and organizing raw clinical research data from multiple sites.

---

## 1. Folder Naming Convention
- Raw data must be placed in `data/raw/`
- File names must follow the format: `siteID_dataType_date.csv`  
  e.g., `B_behavioral_2025-03-01.csv`

---

## 2. Metadata Requirements
Each dataset must include:
- `subject_id`, `age`, `sex`, `site`, and relevant assessments
- Data dictionary (as separate `.csv` or `.xlsx`)

---

## 3. Validation Checklist
Before processing:
- [ ] Check for required columns
- [ ] Ensure no PHI (e.g., names, DOB)
- [ ] Ensure filename and content match metadata

---

## 4. Version Tracking
- All new intakes must be logged in `CHANGELOG.md`
- Prior versions archived under `data/archived/` if applicable
