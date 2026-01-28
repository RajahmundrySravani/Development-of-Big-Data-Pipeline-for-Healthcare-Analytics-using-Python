# 📊 Power BI Dashboard Setup Guide

**Healthcare Analytics Platform - Power BI Integration**

---

## 🎯 Overview

This guide will help you create professional Power BI dashboards using the cleaned CSV files from S3.

**Data Sources:**
- S3: `s3://sravani-healthcare-data/processed/cleaned/`
  - `patients_cleaned.csv` (12,000 records)
  - `visits_cleaned.csv` (5 records)
  - `prescriptions_cleaned.csv` (5 records)

---

## 📥 Step 1: Download Data from S3

### Option A: Using AWS CLI
```bash
# Install AWS CLI if not already installed
# Download cleaned CSV files
aws s3 cp s3://sravani-healthcare-data/processed/cleaned/patients_cleaned.csv ./powerbi_data/
aws s3 cp s3://sravani-healthcare-data/processed/cleaned/visits_cleaned.csv ./powerbi_data/
aws s3 cp s3://sravani-healthcare-data/processed/cleaned/prescriptions_cleaned.csv ./powerbi_data/
```

### Option B: Using Python Script
Run the provided `download_s3_for_powerbi.py` script (see below)

### Option C: Manual Download
1. Open AWS S3 Console
2. Navigate to `sravani-healthcare-data` bucket
3. Go to `processed/cleaned/` folder
4. Download all 3 CSV files

---

## 🔌 Step 2: Import Data into Power BI

### 2.1 Open Power BI Desktop
- Launch Power BI Desktop
- Click **Get Data** → **Text/CSV**

### 2.2 Import Patients Data
1. Select `patients_cleaned.csv`
2. Click **Transform Data** (Power Query Editor)
3. **Data Type Corrections:**
   - `patient_id` → Text
   - `age` → Whole Number
   - `gender` → Text
   - `bmi` → Decimal Number
   - `smoker_status` → Text
   - `alcohol_use` → Text
   - `age_group` → Text
4. Click **Close & Apply**

### 2.3 Import Visits Data
1. Select `visits_cleaned.csv`
2. **Data Type Corrections:**
   - `visit_id` → Text
   - `patient_id` → Text
   - `visit_date` → Date
   - `diagnosis_code` → Text
   - `severity_score` → Whole Number
   - `length_of_stay` → Whole Number
3. Click **Close & Apply**

### 2.4 Import Prescriptions Data
1. Select `prescriptions_cleaned.csv`
2. **Data Type Corrections:**
   - `prescription_id` → Text
   - `visit_id` → Text
   - `patient_id` → Text
   - `medication_name` → Text
   - `dosage` → Text
3. Click **Close & Apply**

---

## 🔗 Step 3: Create Relationships

### Go to Model View (left sidebar icon)

**Create these relationships:**

1. **Patients → Visits**
   - From: `Patients[patient_id]`
   - To: `Visits[patient_id]`
   - Cardinality: One to Many (1:*)
   - Cross filter direction: Both

2. **Visits → Prescriptions**
   - From: `Visits[visit_id]`
   - To: `Prescriptions[visit_id]`
   - Cardinality: One to Many (1:*)
   - Cross filter direction: Both

---

## 📐 Step 4: Create Measures (DAX Formulas)

### Go to **Report View** → **Modeling** → **New Measure**

Copy these DAX formulas:

```dax
// Basic Counts
Total Patients = COUNT(Patients[patient_id])

Total Visits = COUNT(Visits[visit_id])

Total Prescriptions = COUNT(Prescriptions[prescription_id])

// Demographics
Average Age = AVERAGE(Patients[age])

Average BMI = AVERAGE(Patients[bmi])

Male Patients = CALCULATE(COUNT(Patients[patient_id]), Patients[gender] = "Male")

Female Patients = CALCULATE(COUNT(Patients[patient_id]), Patients[gender] = "Female")

Smokers Count = CALCULATE(COUNT(Patients[patient_id]), Patients[smoker_status] = "yes")

Smokers Percentage = 
DIVIDE(
    CALCULATE(COUNT(Patients[patient_id]), Patients[smoker_status] = "yes"),
    COUNT(Patients[patient_id]),
    0
) * 100

// Risk Categories (BMI-based)
Underweight = CALCULATE(COUNT(Patients[patient_id]), Patients[bmi] < 18.5)

Normal Weight = CALCULATE(COUNT(Patients[patient_id]), Patients[bmi] >= 18.5 && Patients[bmi] < 25)

Overweight = CALCULATE(COUNT(Patients[patient_id]), Patients[bmi] >= 25 && Patients[bmi] < 30)

Obese = CALCULATE(COUNT(Patients[patient_id]), Patients[bmi] >= 30)

// Visit Analytics
Average Length of Stay = AVERAGE(Visits[length_of_stay])

Average Severity Score = AVERAGE(Visits[severity_score])

High Severity Visits = CALCULATE(COUNT(Visits[visit_id]), Visits[severity_score] >= 7)

// Calculated Columns (Create in Table View)
// In Patients table, create new column:
BMI Category = 
SWITCH(
    TRUE(),
    Patients[bmi] < 18.5, "Underweight",
    Patients[bmi] < 25, "Normal",
    Patients[bmi] < 30, "Overweight",
    "Obese"
)

Risk Level = 
SWITCH(
    TRUE(),
    Patients[bmi] >= 30 && Patients[smoker_status] = "yes", "High Risk",
    Patients[bmi] >= 25 && Patients[smoker_status] = "yes", "Medium Risk",
    Patients[bmi] >= 30 || Patients[smoker_status] = "yes", "Medium Risk",
    "Low Risk"
)
```

---

## 📊 Step 5: Dashboard Visualizations

### Dashboard 1: **Patient Demographics Overview**

#### Page Layout:

**Top Row - KPI Cards:**
1. **Total Patients** (Card visual)
   - Value: `[Total Patients]`
   - Format: 12,000

2. **Average Age** (Card visual)
   - Value: `[Average Age]`
   - Format: 0 decimal

3. **Average BMI** (Card visual)
   - Value: `[Average BMI]`
   - Format: 1 decimal

4. **Smokers %** (Card visual)
   - Value: `[Smokers Percentage]`
   - Format: % with 1 decimal

**Middle Row - Charts:**

5. **Age Distribution** (Column Chart)
   - Axis: `age_group`
   - Values: `[Total Patients]`
   - Sort by: age_group ascending

6. **Gender Distribution** (Donut Chart)
   - Legend: `gender`
   - Values: `[Total Patients]`
   - Data labels: Category, Value, Percentage

7. **BMI Categories** (Bar Chart)
   - Axis: `BMI Category` (calculated column)
   - Values: `[Total Patients]`
   - Colors: Green (Normal), Yellow (Overweight), Red (Obese)

**Bottom Row:**

8. **Risk Level Distribution** (Pie Chart)
   - Legend: `Risk Level`
   - Values: `[Total Patients]`
   - Colors: Red (High), Orange (Medium), Green (Low)

9. **Smoker vs Alcohol Use** (Stacked Bar Chart)
   - Axis: `smoker_status`
   - Legend: `alcohol_use`
   - Values: `[Total Patients]`

---

### Dashboard 2: **Clinical Analytics**

#### Page Layout:

**Top Row - KPI Cards:**
1. **Total Visits** → `[Total Visits]`
2. **Avg Length of Stay** → `[Average Length of Stay]`
3. **Avg Severity Score** → `[Average Severity Score]`
4. **High Severity Visits** → `[High Severity Visits]`

**Middle Row:**

5. **Severity Score Distribution** (Histogram)
   - Axis: `severity_score`
   - Values: Count of visits
   - Bins: 1-3 (Low), 4-6 (Medium), 7-10 (High)

6. **Length of Stay Analysis** (Box Plot or Column Chart)
   - Axis: `length_of_stay` (grouped: 1-3, 4-7, 8-14, 15+)
   - Values: Count of visits

7. **Top 10 Diagnoses** (Bar Chart)
   - Axis: `diagnosis_description`
   - Values: Count of visits
   - Sort: Descending by count
   - Top N filter: 10

**Bottom Row:**

8. **Visit Trends Over Time** (Line Chart)
   - Axis: `visit_date` (by month)
   - Values: Count of visits
   - Data labels: Show values

9. **Prescriptions per Visit** (Table)
   - Columns: visit_id, patient_id, medication_name, dosage
   - Filter: Top 20 visits

---

### Dashboard 3: **Risk Assessment Dashboard**

**Top Row:**

1. **High Risk Patients** (Card)
   - Value: COUNT where `Risk Level` = "High Risk"

2. **Medium Risk Patients** (Card)
   - Value: COUNT where `Risk Level` = "Medium Risk"

3. **Low Risk Patients** (Card)
   - Value: COUNT where `Risk Level` = "Low Risk"

**Middle Section:**

4. **Risk Factors Matrix** (Matrix visual)
   - Rows: `BMI Category`
   - Columns: `smoker_status`
   - Values: `[Total Patients]`
   - Conditional formatting: Color scale (red = high count)

5. **Age vs BMI Scatter Plot** (Scatter chart)
   - X-axis: `age`
   - Y-axis: `bmi`
   - Legend: `gender`
   - Size: Count of patients (aggregated)
   - Colors: Blue (Male), Pink (Female), Gray (Other)

**Bottom Row:**

6. **Risk Distribution by Age Group** (Stacked Column Chart)
   - Axis: `age_group`
   - Legend: `Risk Level`
   - Values: `[Total Patients]`
   - 100% Stacked: Yes

7. **Comorbidity Analysis** (Table)
   - Columns: 
     - `age_group`
     - `smoker_status`
     - `alcohol_use`
     - `BMI Category`
     - Count of patients
   - Filters: BMI >= 30 OR smoker = yes

---

## 🎨 Step 6: Design Best Practices

### Color Scheme (Healthcare Theme):
- **Primary:** #0078D4 (Azure Blue)
- **Success:** #107C10 (Green)
- **Warning:** #FFB900 (Yellow)
- **Danger:** #D13438 (Red)
- **Neutral:** #737373 (Gray)

### Typography:
- **Title:** Segoe UI Semibold, 18pt
- **Headers:** Segoe UI, 14pt
- **Body:** Segoe UI, 11pt

### Layout:
- Use consistent spacing (20px margins)
- Align visuals in grids
- Group related visuals with rectangles/backgrounds
- Add dashboard title with logo placeholder

---

## 🔄 Step 7: Add Interactivity

### Slicers (Filters):
Add these slicers to each dashboard page:

1. **Age Group** (Dropdown)
2. **Gender** (Buttons)
3. **Risk Level** (Buttons)
4. **Smoker Status** (Toggle)
5. **BMI Category** (List)

### Cross-filtering:
- Enable cross-filtering between all visuals
- Click on chart segments to filter other visuals

### Drill-through:
Create drill-through page for individual patient details:
- Right-click on patient_id → Drill through → Patient Details
- Show: All patient info, visit history, prescriptions

---

## 📤 Step 8: Publish & Share

### Save Report:
1. File → Save As → `Healthcare_Analytics_Dashboard.pbix`

### Publish to Power BI Service:
1. Click **Publish** button (top ribbon)
2. Select workspace (create "Healthcare Analytics" workspace)
3. View in browser

### Create Dashboard:
1. In Power BI Service, pin visuals from report to new dashboard
2. Arrange tiles in logical order
3. Add text boxes for context

### Share:
1. Share → Get Link (read-only)
2. Or: Share → Grant access to specific users
3. Set up automatic refresh (if data source supports)

---

## 📊 Sample DAX Queries for Advanced Analytics

### Month-over-Month Visit Growth:
```dax
Visit Growth = 
VAR CurrentMonthVisits = CALCULATE([Total Visits], DATESMTD(Visits[visit_date]))
VAR PreviousMonthVisits = CALCULATE([Total Visits], DATEADD(Visits[visit_date], -1, MONTH))
RETURN
DIVIDE(CurrentMonthVisits - PreviousMonthVisits, PreviousMonthVisits, 0) * 100
```

### Readmission Rate (if you add readmission data):
```dax
Readmission Rate = 
DIVIDE(
    CALCULATE(COUNT(Visits[visit_id]), Visits[readmitted_within_30_days] = 1),
    COUNT(Visits[visit_id]),
    0
) * 100
```

### Patient Risk Score:
```dax
Patient Risk Score = 
VAR BMIScore = IF(Patients[bmi] >= 30, 3, IF(Patients[bmi] >= 25, 2, 1))
VAR SmokerScore = IF(Patients[smoker_status] = "yes", 2, 0)
VAR AlcoholScore = IF(Patients[alcohol_use] = "yes", 1, 0)
VAR AgeScore = IF(Patients[age] >= 65, 2, IF(Patients[age] >= 45, 1, 0))
RETURN BMIScore + SmokerScore + AlcoholScore + AgeScore
```

---

## 🎯 Dashboard Checklist

### Before Presentation:
- [ ] All data loaded correctly
- [ ] Relationships validated
- [ ] Measures calculated properly
- [ ] Visuals formatted consistently
- [ ] Slicers working
- [ ] Cross-filtering enabled
- [ ] Dashboard title and branding added
- [ ] Data refreshed to latest
- [ ] Tested on different screen sizes
- [ ] Published to Power BI Service

### For Internship Demo:
- [ ] Prepare talking points for each dashboard
- [ ] Practice navigating between pages
- [ ] Demonstrate filtering capabilities
- [ ] Show drill-through functionality
- [ ] Explain insights and trends
- [ ] Have backup screenshots ready

---

## 💡 Key Insights to Highlight

When presenting your Power BI dashboards, emphasize:

1. **Scale:** "12,000+ patient records analyzed"
2. **Risk Identification:** "X% of patients classified as high risk"
3. **Trends:** "Average BMI is X, with Y% obese patients"
4. **Clinical Metrics:** "Average length of stay: X days, severity score: Y"
5. **Interactive:** "Filters allow drill-down by age, gender, risk level"
6. **Data Pipeline:** "Automated processing with PySpark → S3 → Power BI"

---

## 📚 Additional Resources

- **Power BI Documentation:** https://docs.microsoft.com/power-bi/
- **DAX Reference:** https://dax.guide/
- **Healthcare Dashboard Templates:** Search Power BI gallery
- **Color Accessibility:** Use colorblind-friendly palettes

---

**Created:** January 19, 2026  
**For:** Healthcare Analytics Internship Project  
**Data Source:** S3 Cleaned CSVs (PySpark processed)
