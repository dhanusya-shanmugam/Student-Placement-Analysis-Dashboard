import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Placement Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #1f4e79, #2878b5);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 17px;
}

.kpi {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.kpi-title {
    font-size: 14px;
    color: #666;
}

.kpi-value {
    font-size: 30px;
    font-weight: bold;
    color: #1f4e79;
}

.section-title {
    font-size: 25px;
    font-weight: bold;
    margin-top: 25px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<h1>🎓 Student Placement Analytics</h1>

<p>
Career Insights Dashboard for analyzing academic performance,
skills, internships, placement outcomes and salary trends.
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FILE UPLOAD
# =========================================================

st.subheader("📂 Upload Student Dataset")

uploaded_file = st.file_uploader(
    "Upload your Excel or CSV file",
    type=["xlsx", "csv"],
    help="Upload a student placement dataset to generate the dashboard."
)

# =========================================================
# BEFORE FILE UPLOAD
# =========================================================

if uploaded_file is None:

    st.info(
        "👆 Please upload an Excel (.xlsx) or CSV (.csv) file to start the analysis."
    )

    st.markdown("""
    ### ✨ Dashboard Features

    📊 Placement Overview  
    🏫 Department Analysis  
    💼 Internship Analysis  
    📚 Academic Performance  
    🎯 Skill & Interview Analysis  
    🏢 Company Recruitment  
    💰 Salary Analysis  
    👩‍🎓 Student Search  
    🔎 Interactive Filters  
    💡 Automatic Insights  
    📥 Download Filtered Data
    """)

    st.stop()

# =========================================================
# READ FILE
# =========================================================

try:

    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(f"Unable to read the uploaded file: {e}")
    st.stop()

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()

# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Student_ID",
    "Department",
    "Gender",
    "10th_Percentage",
    "12th_Percentage",
    "CGPA",
    "Attendance",
    "Backlogs",
    "Internship",
    "Certifications",
    "Technical_Skills",
    "Aptitude_Score",
    "Communication_Score",
    "Interview_Score",
    "Placement_Status",
    "Company",
    "Salary_LPA"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error("❌ Your file is missing required columns:")

    for col in missing_columns:
        st.write(f"- {col}")

    st.stop()

# =========================================================
# DATA CLEANING
# =========================================================

numeric_columns = [
    "10th_Percentage",
    "12th_Percentage",
    "CGPA",
    "Attendance",
    "Backlogs",
    "Certifications",
    "Aptitude_Score",
    "Communication_Score",
    "Interview_Score",
    "Salary_LPA"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Placement_Status"] = (
    df["Placement_Status"]
    .astype(str)
    .str.strip()
)

df["Department"] = (
    df["Department"]
    .astype(str)
    .str.strip()
)

df["Internship"] = (
    df["Internship"]
    .astype(str)
    .str.strip()
)

# =========================================================
# SUCCESS MESSAGE
# =========================================================

st.success(
    f"✅ Dataset uploaded successfully — {len(df):,} students found."
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.caption("Use these filters to interact with the dashboard.")

# Department

department_list = sorted(
    df["Department"].dropna().unique().tolist()
)

selected_departments = st.sidebar.multiselect(
    "🏫 Department",
    department_list,
    default=department_list
)

# Gender

gender_list = sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.multiselect(
    "👤 Gender",
    gender_list,
    default=gender_list
)

# Placement

placement_list = sorted(
    df["Placement_Status"].dropna().unique().tolist()
)

selected_placement = st.sidebar.multiselect(
    "📌 Placement Status",
    placement_list,
    default=placement_list
)

# Internship

internship_list = sorted(
    df["Internship"].dropna().unique().tolist()
)

selected_internship = st.sidebar.multiselect(
    "💼 Internship",
    internship_list,
    default=internship_list
)

# CGPA slider

min_cgpa = float(df["CGPA"].min())
max_cgpa = float(df["CGPA"].max())

selected_cgpa = st.sidebar.slider(
    "📚 CGPA Range",
    min_value=min_cgpa,
    max_value=max_cgpa,
    value=(min_cgpa, max_cgpa),
    step=0.1
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["Department"].isin(selected_departments))
    &
    (df["Gender"].isin(selected_gender))
    &
    (df["Placement_Status"].isin(selected_placement))
    &
    (df["Internship"].isin(selected_internship))
    &
    (df["CGPA"].between(selected_cgpa[0], selected_cgpa[1]))
].copy()

# =========================================================
# DASHBOARD HEADER
# =========================================================

st.markdown(
    '<div class="section-title">📊 Placement Overview</div>',
    unsafe_allow_html=True
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_students = len(filtered_df)

placed_students = (
    filtered_df["Placement_Status"]
    .eq("Placed")
    .sum()
)

placement_rate = (
    placed_students / total_students * 100
    if total_students > 0
    else 0
)

placed_df = filtered_df[
    filtered_df["Placement_Status"] == "Placed"
]

average_salary = (
    placed_df["Salary_LPA"].mean()
    if len(placed_df) > 0
    else 0
)

highest_salary = (
    placed_df["Salary_LPA"].max()
    if len(placed_df) > 0
    else 0
)

average_cgpa = (
    filtered_df["CGPA"].mean()
    if total_students > 0
    else 0
)

# =========================================================
# KPI CARDS
# =========================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "👩‍🎓 Total Students",
        f"{total_students:,}"
    )

with c2:
    st.metric(
        "✅ Placed Students",
        f"{placed_students:,}"
    )

with c3:
    st.metric(
        "📈 Placement Rate",
        f"{placement_rate:.2f}%"
    )

with c4:
    st.metric(
        "💰 Average Salary",
        f"{average_salary:.2f} LPA"
    )

with c5:
    st.metric(
        "🏆 Highest Salary",
        f"{highest_salary:.2f} LPA"
    )

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🏫 Department",
        "🎯 Skills & Academics",
        "🏢 Companies & Salary",
        "👩‍🎓 Student Details"
    ]
)

# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with tab1:

    st.subheader("📌 Placement Status")

    col1, col2 = st.columns(2)

    placement_counts = (
        filtered_df["Placement_Status"]
        .value_counts()
        .reset_index()
    )

    placement_counts.columns = [
        "Placement_Status",
        "Student_Count"
    ]

    with col1:

        fig = px.pie(
            placement_counts,
            names="Placement_Status",
            values="Student_Count",
            hole=0.45,
            title="Placed vs Not Placed"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            placement_counts,
            x="Placement_Status",
            y="Student_Count",
            text="Student_Count",
            title="Placement Status Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Internship

    st.subheader("💼 Internship vs Placement")

    internship_summary = filtered_df.groupby(
        "Internship"
    ).agg(
        Total_Students=("Student_ID", "count"),
        Placed_Students=(
            "Placement_Status",
            lambda x: (x == "Placed").sum()
        )
    ).reset_index()

    internship_summary["Placement_Rate"] = (
        internship_summary["Placed_Students"]
        /
        internship_summary["Total_Students"]
        * 100
    )

    fig = px.bar(
        internship_summary,
        x="Internship",
        y="Placement_Rate",
        text_auto=".2f",
        title="Placement Rate by Internship"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # CGPA

    st.subheader("📚 CGPA vs Placement")

    cgpa_summary = filtered_df.groupby(
        "Placement_Status"
    )["CGPA"].mean().reset_index()

    cgpa_summary.columns = [
        "Placement_Status",
        "Average_CGPA"
    ]

    fig = px.bar(
        cgpa_summary,
        x="Placement_Status",
        y="Average_CGPA",
        text_auto=".2f",
        title="Average CGPA by Placement Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# TAB 2 — DEPARTMENT
# =========================================================

with tab2:

    st.subheader("🏫 Department-wise Analysis")

    dept_summary = filtered_df.groupby(
        "Department"
    ).agg(
        Total_Students=("Student_ID", "count"),
        Placed_Students=(
            "Placement_Status",
            lambda x: (x == "Placed").sum()
        ),
        Average_CGPA=("CGPA", "mean"),
        Average_Attendance=("Attendance", "mean")
    ).reset_index()

    dept_summary["Placement_Rate"] = (
        dept_summary["Placed_Students"]
        /
        dept_summary["Total_Students"]
        * 100
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            dept_summary,
            x="Department",
            y="Placement_Rate",
            text_auto=".2f",
            title="Department Placement Rate"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            dept_summary,
            x="Department",
            y="Average_CGPA",
            text_auto=".2f",
            title="Average CGPA by Department"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("📋 Department Summary")

    st.dataframe(
        dept_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# TAB 3 — SKILLS & ACADEMICS
# =========================================================

with tab3:

    st.subheader("🎯 Skill & Interview Performance")

    score_summary = filtered_df.groupby(
        "Placement_Status"
    ).agg(
        Average_Aptitude=("Aptitude_Score", "mean"),
        Average_Communication=("Communication_Score", "mean"),
        Average_Interview=("Interview_Score", "mean")
    ).reset_index()

    score_long = score_summary.melt(
        id_vars="Placement_Status",
        var_name="Score_Type",
        value_name="Average_Score"
    )

    fig = px.bar(
        score_long,
        x="Placement_Status",
        y="Average_Score",
        color="Score_Type",
        barmode="group",
        text_auto=".1f",
        title="Aptitude, Communication & Interview Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Backlogs

    st.subheader("📉 Backlogs vs Placement")

    backlog_summary = filtered_df.groupby(
        "Backlogs"
    ).agg(
        Total_Students=("Student_ID", "count"),
        Placed_Students=(
            "Placement_Status",
            lambda x: (x == "Placed").sum()
        )
    ).reset_index()

    backlog_summary["Placement_Rate"] = (
        backlog_summary["Placed_Students"]
        /
        backlog_summary["Total_Students"]
        * 100
    )

    fig = px.line(
        backlog_summary,
        x="Backlogs",
        y="Placement_Rate",
        markers=True,
        title="Placement Rate by Backlogs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Certifications

    st.subheader("🏆 Certifications vs Placement")

    cert_summary = filtered_df.groupby(
        "Certifications"
    ).agg(
        Total_Students=("Student_ID", "count"),
        Placed_Students=(
            "Placement_Status",
            lambda x: (x == "Placed").sum()
        )
    ).reset_index()

    cert_summary["Placement_Rate"] = (
        cert_summary["Placed_Students"]
        /
        cert_summary["Total_Students"]
        * 100
    )

    fig = px.bar(
        cert_summary,
        x="Certifications",
        y="Placement_Rate",
        text_auto=".2f",
        title="Placement Rate by Certifications"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# TAB 4 — COMPANY & SALARY
# =========================================================

with tab4:

    st.subheader("🏢 Company Recruitment")

    company_summary = (
        filtered_df[
            filtered_df["Placement_Status"] == "Placed"
        ]
        .groupby("Company")
        .size()
        .reset_index(
            name="Students_Recruited"
        )
        .sort_values(
            "Students_Recruited",
            ascending=False
        )
    )

    if len(company_summary) > 0:

        fig = px.bar(
            company_summary,
            x="Company",
            y="Students_Recruited",
            text="Students_Recruited",
            title="Students Recruited by Company"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Salary

    st.subheader("💰 Salary Analysis")

    salary_summary = (
        placed_df
        .groupby("Department")
        .agg(
            Average_Salary_LPA=("Salary_LPA", "mean"),
            Highest_Salary_LPA=("Salary_LPA", "max")
        )
        .reset_index()
    )

    if len(salary_summary) > 0:

        fig = px.bar(
            salary_summary,
            x="Department",
            y="Average_Salary_LPA",
            text_auto=".2f",
            title="Average Salary by Department"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            salary_summary.round(2),
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# TAB 5 — STUDENT DETAILS
# =========================================================

with tab5:

    st.subheader("👩‍🎓 Student Search")

    student_ids = sorted(
        filtered_df["Student_ID"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if student_ids:

        selected_student = st.selectbox(
            "🔎 Select Student ID",
            student_ids
        )

        student = filtered_df[
            filtered_df["Student_ID"].astype(str)
            == selected_student
        ].iloc[0]

        st.markdown("### 📄 Student Profile")

        a, b, c, d = st.columns(4)

        with a:
            st.metric(
                "Department",
                str(student["Department"])
            )

        with b:
            st.metric(
                "CGPA",
                f"{student['CGPA']:.2f}"
            )

        with c:
            st.metric(
                "Placement",
                str(student["Placement_Status"])
            )

        with d:
            st.metric(
                "Salary",
                f"{student['Salary_LPA']:.2f} LPA"
            )

        st.markdown("### 📚 Academic Details")

        st.write(
            f"**10th Percentage:** {student['10th_Percentage']:.2f}%"
        )

        st.write(
            f"**12th Percentage:** {student['12th_Percentage']:.2f}%"
        )

        st.write(
            f"**Attendance:** {student['Attendance']:.2f}%"
        )

        st.write(
            f"**Backlogs:** {int(student['Backlogs'])}"
        )

        st.markdown("### 🎯 Skill Details")

        st.write(
            f"**Technical Skills:** {student['Technical_Skills']}"
        )

        st.write(
            f"**Aptitude Score:** {student['Aptitude_Score']:.2f}"
        )

        st.write(
            f"**Communication Score:** {student['Communication_Score']:.2f}"
        )

        st.write(
            f"**Interview Score:** {student['Interview_Score']:.2f}"
        )

        st.write(
            f"**Internship:** {student['Internship']}"
        )

        st.write(
            f"**Certifications:** {int(student['Certifications'])}"
        )

        if student["Placement_Status"] == "Placed":

            st.success(
                f"🎉 Student placed at **{student['Company']}** "
                f"with **{student['Salary_LPA']:.2f} LPA**."
            )

        else:

            st.warning(
                "This student is currently marked as Not Placed."
            )

# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================

st.divider()

st.subheader("💡 Automatic Career Insights")

if len(filtered_df) > 0:

    dept_analysis = filtered_df.groupby(
        "Department"
    ).agg(
        Total=("Student_ID", "count"),
        Placed=(
            "Placement_Status",
            lambda x: (x == "Placed").sum()
        )
    ).reset_index()

    dept_analysis["Rate"] = (
        dept_analysis["Placed"]
        /
        dept_analysis["Total"]
        * 100
    )

    best_dept = dept_analysis.loc[
        dept_analysis["Rate"].idxmax()
    ]

    st.success(
        f"🏆 **{best_dept['Department']}** has the highest "
        f"placement rate: **{best_dept['Rate']:.2f}%**."
    )

    if len(placed_df) > 0:

        st.info(
            f"💰 Highest salary in the selected data is "
            f"**{highest_salary:.2f} LPA**."
        )

        st.info(
            f"📚 Average CGPA of placed students is "
            f"**{placed_df['CGPA'].mean():.2f}**."
        )

        st.info(
            f"🎯 Average interview score of placed students is "
            f"**{placed_df['Interview_Score'].mean():.2f}**."
        )

# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

st.divider()

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_student_placement_data.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎓 Student Placement Analytics & Career Insights | "
    "Python • Pandas • Plotly • Streamlit"
)