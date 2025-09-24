# 🧠📊 Personal Health Dashboard  
*A Quantified-Self Project for KPI Design, Data Storytelling & End-to-End Analytics Using Tableau, SQL and Python*

---

## 📌 Project Overview

This personal project showcases my ability to **think and work like a professional data analyst** by building an **end-to-end data pipeline**—from **raw Apple Health XML extraction** to **dashboard visualization**—while designing and evaluating **custom health-related Key Performance Indicators (KPIs)**.

---

## 🎯 Project Goals

### 1. Define KPIs like a professional analyst to answer a real-world question

> **Business Question:** _"Is my current lifestyle healthy?"_  
I treat my personal health as a “product” and evaluate its performance using custom metrics.

#### 🔑 Custom KPI Design

- **🏆 Activity Score (Main KPI)**  
  A weighted average combining:
  - Daily **steps**
  - **Active calories** burned
  - **Sleep duration**  
  Each component is normalized by personalized targets.  
  → A score **> 1** indicates a "good day" (goal achieved).

- **🎯 Secondary KPIs**
  - Average daily steps
  - Workout frequency and duration
  - Sleep quality breakdown by weekday and sleep stage
  - Hourly calorie burn pattern

These KPIs provide actionable feedback for improving personal habits.

---

### 2. Build a complete analytics pipeline using real-world health data

I designed and implemented a full data workflow using Python, SQL, and Tableau:

| Stage               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| 🗂 **Data Extraction** | Exported `.XML` from **Apple Health** (iPhone).                             |
| 🐍 **Data Processing** | Wrote **Python scripts** to parse, clean, and transform raw XML.            |
| 🗃 **Data Storage**     | Structured cleaned data and stored in a **MySQL** database.                |
| 🔎 **Data Manipulation** | Used **SQL queries** to summarize and join key datasets.                  |
| 📊 **Visualization**     | Connected **Tableau** to MySQL and created dynamic interactive dashboards. |

---

## 💻 Dashboard Highlights (Tableau)

### 🧾 Overview Dashboard
- Select custom **date range**
- View summary KPIs:
  - Daily calories
  - Average steps
  - Total workouts
  - Average sleep duration
- **Activity Score Chart**: stacked bar with goal-based color coding
- **Hourly Calories Heatmap**: identify peak calorie burn hours by day of week

---

### 🏃‍♀️ Exercise Dashboard
- **Workout Frequency**:
  - View top or bottom 5 most/least frequent workout types
- **Average Duration** by workout type
- **Monthly View**: bar chart of workout frequency per day in a selected month

---

### 🛌 Sleep Dashboard
- Filter by **sleep stage** (core, deep, REM)
- Compare average **duration** and **total minutes** across weekdays
- Identify weekly sleep rhythm and inconsistencies

---

## 🧠 Key Insights

- **Steps & Activity Score** peak mid-week and dip on weekends.
- **Most consistent sleep** occurs on Wednesdays and Thursdays.
- **CoreTraining & Walking** are the most frequent and longest workouts.
- **Calories peak between 5–8 PM**, especially on weekdays—likely workout time.

---

---

## 🔄 Reproducibility Instructions

### Step 1: Export Your Own Apple Health Data
- iPhone → Health App → Profile → Export All Health Data
- Unzip the file to extract `.xml`

### Step 2: Preprocess Data in Python
```bash
python pyscript.py
```
### Step 3: Load to MySQL
### Step 4: Connect Tableau to MySQL
```bash
Tableau dashboard.twb
```
- Tableau Desktop is required for this step. Then you can use this dashboard to explore your own health data!
  
---

## 💡 What I Learned
- Thinking like an analyst: designing KPIs and interpreting trends
- Working with messy real-world health data
- Automating ETL workflows with Python and SQL
- Building clear, interpretable Tableau dashboards
- Storytelling with data to generate actionable insights

