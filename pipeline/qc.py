import pandas as pd

def run_qc_report(file_path, output_path):
    df = pd.read_csv(file_path)

    # Prepare report content
    report_lines = []

    report_lines.append("📋 QC Report")
    report_lines.append("=" * 40)

    # 1. Missing values
    report_lines.append("\n🧩 Missing Values:")
    report_lines.append(df.isnull().sum().to_string())

    # 2. Age outliers
    report_lines.append("\n🎯 Age Outliers (age < 5 or > 100):")
    age_outliers = df[(df["age"] < 5) | (df["age"] > 100)]
    if age_outliers.empty:
        report_lines.append("No age outliers.")
    else:
        report_lines.append(age_outliers.to_string(index=False))

    # 3. Site distribution
    report_lines.append("\n🏥 Site Distribution:")
    report_lines.append(df["site"].value_counts().to_string())

    # 4. IQ summary
    report_lines.append("\n🧠 IQ Summary:")
    report_lines.append(df["IQ"].describe().to_string())

    # Combine all lines
    full_report = "\n".join(report_lines)

    # Print to console
    print(full_report)

    # Save to file
    with open(output_path, "w") as f:
        f.write(full_report)

    print(f"\n✅ Report saved to {output_path}")

if __name__ == "__main__":
    run_qc_report("data/cleaned/clinical_data_cleaned.csv", "data/cleaned/qc_report.txt")

