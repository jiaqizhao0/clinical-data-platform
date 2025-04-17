# 🔐 Privacy Risk Assessment

**Purpose:**  
To ensure that all clinical research data sharing complies with HIPAA and GCP guidelines.

---

## 1. Data De-Identification
- Remove direct identifiers (e.g., names, emails)
- Convert `DOB` → `age`
- Replace `subject_id` with randomized pseudonyms if needed

---

## 2. Data Storage & Access
- Stored locally or on secure cloud (e.g., encrypted S3 bucket)
- Access controlled via GitHub + permissions-based directories

---

## 3. Sharing with Third Parties
- All external sharing must be governed by a signed DUA
- Verify platform security (e.g., AWS, REDCap, Synapse)

---

## 4. Audit & Training
- Maintain logs of all file transfers
- Provide onboarding documentation to all data users
