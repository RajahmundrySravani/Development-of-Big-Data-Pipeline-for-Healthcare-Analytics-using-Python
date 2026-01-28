# 📊 Power BI Quick Start Guide

## ⚡ Fast Setup (5 Minutes)

### Step 1: Import Data
1. Open **Power BI Desktop**
2. **Get Data** → **Text/CSV**
3. Navigate to: `D:\moon\BigData\sun_healthcare_final\backend\powerbi_data`
4. Import these files (one at a time):
   - ✅ `patients_cleaned.csv`
   - ✅ `visits_cleaned.csv`
   - ✅ `prescriptions_cleaned.csv`

### Step 2: Set Data Types
For each table, click **Transform Data**:

**Patients:**
- patient_id → Text
- age → Whole Number
- bmi → Decimal Number
- gender, smoker_status, alcohol_use, age_group → Text

**Visits:**
- visit_id, patient_id → Text
- visit_date → Date
- severity_score, length_of_stay → Whole Number

**Prescriptions:**
- All fields → Text

Click **Close & Apply**

### Step 3: Create Relationships
Go to **Model View** (left sidebar):
1. Drag `Patients[patient_id]` → `Visits[patient_id]` (1:*)
2. Drag `Visits[visit_id]` → `Prescriptions[visit_id]` (1:*)

### Step 4: Copy These DAX Measures
Click **New Measure** and paste:

```dax
Total Patients = COUNT(Patients[patient_id])
Average Age = AVERAGE(Patients[age])
Average BMI = AVERAGE(Patients[bmi])
Smokers % = DIVIDE(CALCULATE(COUNT(Patients[patient_id]), Patients[smoker_status] = "yes"), COUNT(Patients[patient_id]), 0) * 100
```

### Step 5: Create Your First Dashboard

**Add 4 Cards (KPIs):**
- Total Patients
- Average Age
- Average BMI
- Smokers %

**Add 3 Charts:**
1. **Donut Chart:** Gender distribution
   - Legend: gender
   - Values: Total Patients

2. **Column Chart:** Age groups
   - Axis: age_group
   - Values: Total Patients

3. **Bar Chart:** BMI by age group
   - Axis: age_group
   - Values: Average BMI

**Add Slicers:**
- Gender (buttons)
- Age Group (dropdown)

---

## 🎯 Dashboard Ideas

### Dashboard 1: **Demographics**
- KPIs: Total patients, avg age, avg BMI, smokers %
- Charts: Age distribution, gender split, BMI categories
- Slicers: Gender, age group, risk level

### Dashboard 2: **Clinical Insights**
- KPIs: Total visits, avg severity, avg length of stay
- Charts: Severity distribution, top diagnoses, visit trends
- Slicers: Diagnosis, severity range

### Dashboard 3: **Risk Assessment**
- KPIs: High/medium/low risk counts
- Charts: Risk by age group, BMI vs age scatter, risk matrix
- Slicers: Risk level, BMI category

---

## 🎨 Design Tips

**Colors (Healthcare Theme):**
- Blue: #0078D4
- Green: #107C10
- Red: #D13438
- Yellow: #FFB900

**Layout:**
- Use 4 columns × 3 rows grid
- Consistent 20px spacing
- Group related visuals with rectangles

---

## 🚀 Advanced DAX (Copy & Paste)

### Calculate BMI Category
Create **New Column** in Patients table:
```dax
BMI Category = 
SWITCH(
    TRUE(),
    Patients[bmi] < 18.5, "Underweight",
    Patients[bmi] < 25, "Normal",
    Patients[bmi] < 30, "Overweight",
    "Obese"
)
```

### Calculate Risk Level
```dax
Risk Level = 
SWITCH(
    TRUE(),
    Patients[bmi] >= 30 && Patients[smoker_status] = "yes", "High Risk",
    Patients[bmi] >= 25 && Patients[smoker_status] = "yes", "Medium Risk",
    Patients[bmi] >= 30 || Patients[smoker_status] = "yes", "Medium Risk",
    "Low Risk"
)
```

### Count by Risk
```dax
High Risk Patients = CALCULATE(COUNT(Patients[patient_id]), Patients[Risk Level] = "High Risk")
```

---

## 📤 Publish & Share

1. **Save:** File → Save As → `Healthcare_Analytics.pbix`
2. **Publish:** Click **Publish** → Select workspace
3. **Share:** Get link from Power BI Service
4. **Screenshot:** For internship report

---

## ✅ Demo Checklist

Before presenting:
- [ ] All data imported correctly (12,000 patients)
- [ ] Relationships working (filter patients → visits)
- [ ] At least 6-8 visuals created
- [ ] Slicers functional
- [ ] Consistent formatting applied
- [ ] Dashboard titled and branded
- [ ] Saved and published
- [ ] Screenshots taken for report

---

## 💡 Key Talking Points

When presenting your dashboard:
1. **"12,000+ patients analyzed with Power BI"**
2. **"Average BMI is X, with Y% smokers"**
3. **"Interactive filters allow drill-down by demographics"**
4. **"Data pipeline: S3 → PySpark → Power BI"**
5. **"Real-time insights for healthcare decision-making"**

---

**Full Guide:** See `POWER_BI_SETUP.md`  
**Data Location:** `backend/powerbi_data/`  
**Project:** Healthcare Analytics Platform
