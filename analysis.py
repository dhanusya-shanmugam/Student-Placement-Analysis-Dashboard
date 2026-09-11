import pandas as pd
import matplotlib.pyplot as plt

print("Student Placement Analytics Project Started")

# Load Dataset
df = pd.read_excel("Student_Placement_Analytics_Dataset_500.xlsx")

print("Rows:", len(df))
print("Columns:", len(df.columns))

# Data Quality
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())
print("Duplicate Student IDs:", df["Student_ID"].duplicated().sum())

# Overall Placement
placement_counts = df["Placement_Status"].value_counts()
placed = (df["Placement_Status"] == "Placed").sum()
total = len(df)

placement_rate = placed / total * 100

print("\nPlacement Status:")
print(placement_counts)
print("Overall Placement Rate:", round(placement_rate, 2), "%")

# Department Analysis
dept_summary = df.groupby("Department").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Status",
                     lambda x: (x == "Placed").sum()),
    Average_CGPA=("CGPA", "mean")
).reset_index()

dept_summary["Placement_Rate"] = (
    dept_summary["Placed_Students"] /
    dept_summary["Total_Students"] * 100
).round(2)

print("\nDepartment-wise Analysis:")
print(dept_summary.round(2))

# Internship Analysis
internship_summary = df.groupby("Internship").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Status",
                     lambda x: (x == "Placed").sum())
).reset_index()

internship_summary["Placement_Rate"] = (
    internship_summary["Placed_Students"] /
    internship_summary["Total_Students"] * 100
).round(2)

print("\nInternship vs Placement:")
print(internship_summary)

# CGPA Analysis
cgpa_summary = df.groupby("Placement_Status")["CGPA"].mean().round(2)

print("\nAverage CGPA by Placement Status:")
print(cgpa_summary)

# Backlog Analysis
backlog_summary = df.groupby("Backlogs").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Status",
                     lambda x: (x == "Placed").sum())
).reset_index()

backlog_summary["Placement_Rate"] = (
    backlog_summary["Placed_Students"] /
    backlog_summary["Total_Students"] * 100
).round(2)

print("\nBacklogs vs Placement:")
print(backlog_summary)

# Certification Analysis
cert_summary = df.groupby("Certifications").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Status",
                     lambda x: (x == "Placed").sum())
).reset_index()

cert_summary["Placement_Rate"] = (
    cert_summary["Placed_Students"] /
    cert_summary["Total_Students"] * 100
).round(2)

print("\nCertifications vs Placement:")
print(cert_summary)

# Score Analysis
score_summary = df.groupby("Placement_Status").agg(
    Average_Aptitude=("Aptitude_Score", "mean"),
    Average_Communication=("Communication_Score", "mean"),
    Average_Interview=("Interview_Score", "mean")
).round(2)

print("\nSkill/Test Score Comparison:")
print(score_summary)

# Company Analysis
company_summary = (
    df[df["Placement_Status"] == "Placed"]
    .groupby("Company")
    .size()
    .reset_index(name="Students_Recruited")
    .sort_values("Students_Recruited", ascending=False)
)

print("\nCompany Recruitment:")
print(company_summary)

# Salary Analysis
salary_summary = (
    df[df["Placement_Status"] == "Placed"]
    .groupby("Department")
    .agg(
        Average_Salary_LPA=("Salary_LPA", "mean"),
        Highest_Salary_LPA=("Salary_LPA", "max")
    )
    .reset_index()
    .round(2)
)

print("\nSalary by Department:")
print(salary_summary)

# Export files for Power BI
dept_summary.to_csv("department_summary.csv", index=False)
internship_summary.to_csv("internship_summary.csv", index=False)
backlog_summary.to_csv("backlog_summary.csv", index=False)
cert_summary.to_csv("certification_summary.csv", index=False)
company_summary.to_csv("company_summary.csv", index=False)
salary_summary.to_csv("salary_summary.csv", index=False)

# Chart 1
plt.figure(figsize=(8, 5))
placement_counts.plot(kind="bar")
plt.title("Placement Status")
plt.xlabel("Placement Status")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig("placement_status.png")
plt.close()

# Chart 2
plt.figure(figsize=(9, 5))
dept_summary.sort_values("Placement_Rate").plot(
    x="Department",
    y="Placement_Rate",
    kind="barh",
    legend=False
)

plt.title("Department-wise Placement Rate")
plt.xlabel("Placement Rate (%)")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig("department_placement_rate.png")
plt.close()

print("\n===================================")
print("PROJECT PYTHON ANALYSIS COMPLETED")
print("===================================")