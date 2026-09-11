CREATE DATABASE IF NOT EXISTS placement_analytics;

USE placement_analytics;

-- ==========================================
-- STUDENT PLACEMENT ANALYTICS PROJECT
-- ==========================================

-- Create Students Table
CREATE TABLE IF NOT EXISTS students (
    Student_ID VARCHAR(20),
    Department VARCHAR(50),
    Gender VARCHAR(20),
    Tenth_Percentage DECIMAL(5,2),
    Twelfth_Percentage DECIMAL(5,2),
    CGPA DECIMAL(4,2),
    Attendance DECIMAL(5,2),
    Backlogs INT,
    Internship VARCHAR(20),
    Certifications INT,
    Technical_Skills VARCHAR(100),
    Aptitude_Score DECIMAL(5,2),
    Communication_Score DECIMAL(5,2),
    Interview_Score DECIMAL(5,2),
    Placement_Status VARCHAR(20),
    Company VARCHAR(100),
    Salary_LPA DECIMAL(5,2)
);

-- ==========================================
-- 1. TOTAL NUMBER OF STUDENTS
-- ==========================================

SELECT COUNT(*) AS Total_Students
FROM students;


-- ==========================================
-- 2. PLACEMENT STATUS
-- ==========================================

SELECT
    Placement_Status,
    COUNT(*) AS Student_Count
FROM students
GROUP BY Placement_Status;


-- ==========================================
-- 3. OVERALL PLACEMENT RATE
-- ==========================================

SELECT
    ROUND(
        100 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Overall_Placement_Rate
FROM students;


-- ==========================================
-- 4. DEPARTMENT-WISE PLACEMENT ANALYSIS
-- ==========================================

SELECT
    Department,
    COUNT(*) AS Total_Students,
    SUM(Placement_Status = 'Placed') AS Placed_Students,
    ROUND(
        100 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Placement_Rate
FROM students
GROUP BY Department
ORDER BY Placement_Rate DESC;


-- ==========================================
-- 5. INTERNSHIP VS PLACEMENT
-- ==========================================

SELECT
    Internship,
    COUNT(*) AS Total_Students,
    SUM(Placement_Status = 'Placed') AS Placed_Students,
    ROUND(
        100 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Placement_Rate
FROM students
GROUP BY Internship;


-- ==========================================
-- 6. CGPA VS PLACEMENT
-- ==========================================

SELECT
    Placement_Status,
    ROUND(AVG(CGPA), 2) AS Average_CGPA
FROM students
GROUP BY Placement_Status;


-- ==========================================
-- 7. BACKLOGS VS PLACEMENT
-- ==========================================

SELECT
    Backlogs,
    COUNT(*) AS Total_Students,
    SUM(Placement_Status = 'Placed') AS Placed_Students,
    ROUND(
        100 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Placement_Rate
FROM students
GROUP BY Backlogs
ORDER BY Backlogs;


-- ==========================================
-- 8. CERTIFICATIONS VS PLACEMENT
-- ==========================================

SELECT
    Certifications,
    COUNT(*) AS Total_Students,
    SUM(Placement_Status = 'Placed') AS Placed_Students,
    ROUND(
        100 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Placement_Rate
FROM students
GROUP BY Certifications
ORDER BY Certifications;


-- ==========================================
-- 9. AVERAGE SKILL SCORES
-- ==========================================

SELECT
    Placement_Status,
    ROUND(AVG(Aptitude_Score), 2) AS Average_Aptitude,
    ROUND(AVG(Communication_Score), 2) AS Average_Communication,
    ROUND(AVG(Interview_Score), 2) AS Average_Interview
FROM students
GROUP BY Placement_Status;


-- ==========================================
-- 10. COMPANY-WISE RECRUITMENT
-- ==========================================

SELECT
    Company,
    COUNT(*) AS Students_Recruited
FROM students
WHERE Placement_Status = 'Placed'
GROUP BY Company
ORDER BY Students_Recruited DESC;


-- ==========================================
-- 11. AVERAGE SALARY BY DEPARTMENT
-- ==========================================

SELECT
    Department,
    ROUND(
        AVG(
            CASE
                WHEN Placement_Status = 'Placed'
                THEN Salary_LPA
            END
        ),
        2
    ) AS Average_Salary_LPA
FROM students
GROUP BY Department
ORDER BY Average_Salary_LPA DESC;


-- ==========================================
-- 12. HIGHEST SALARY
-- ==========================================

SELECT
    Student_ID,
    Department,
    Company,
    Salary_LPA
FROM students
WHERE Placement_Status = 'Placed'
ORDER BY Salary_LPA DESC
LIMIT 10;


-- ==========================================
-- 13. INTERNSHIP + CGPA ANALYSIS
-- ==========================================

SELECT
    Internship,
    ROUND(AVG(CGPA), 2) AS Average_CGPA,
    COUNT(*) AS Total_Students,
    SUM(Placement_Status = 'Placed') AS Placed_Students
FROM students
GROUP BY Internship
ORDER BY Average_CGPA DESC;


-- ==========================================
-- 14. DEPARTMENT + SALARY ANALYSIS
-- ==========================================

SELECT
    Department,
    ROUND(AVG(CGPA), 2) AS Average_CGPA,
    ROUND(AVG(Attendance), 2) AS Average_Attendance,
    ROUND(AVG(Salary_LPA), 2) AS Average_Salary
FROM students
WHERE Placement_Status = 'Placed'
GROUP BY Department
ORDER BY Average_Salary DESC;


-- ==========================================
-- 15. TOP PERFORMING STUDENTS
-- ==========================================

SELECT
    Student_ID,
    Department,
    CGPA,
    Aptitude_Score,
    Communication_Score,
    Interview_Score,
    Company,
    Salary_LPA
FROM students
WHERE Placement_Status = 'Placed'
ORDER BY Salary_LPA DESC
LIMIT 10;

-- ==========================================
-- END OF SQL ANALYSIS
-- ==========================================