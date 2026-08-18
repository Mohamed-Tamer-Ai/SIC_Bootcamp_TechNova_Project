# 📗 TechNova Excel Development Guide — Day 1 & Day 2

> **SIC Data Analysis Bootcamp | Day 1: Foundations & Excel Mastery | Day 2: Statistics & Business Metrics**  
> **Workbook Reference:** `TechNova_Excel.xlsx` (5-Sheet Architecture)  
> **Target Audience:** Instructors, Teaching Assistants, and Bootcamp Students

---

## 📌 1. Project Overview & Business Context

**TechNova Retail** is an omnichannel consumer tech and electronics retailer experiencing rapid sales growth but facing unexplained margin fluctuations and rising customer churn. 

This guide walks you step-by-step through transforming **5,000 rows of raw, messy transactional records** into an executive-ready, interactive Excel Sales & Churn Dashboard.

### 🎯 Key Learning Objectives:
1. **Data Cleaning & Integrity:** Standardizing casing, resolving typos, parsing mixed date formats, and filling missing financial values.
2. **Dynamic Financial Modeling:** Calculating realized revenue, COGS, gross profit, and individual order margins.
3. **Statistical Analysis & Outlier Detection:** Computing Central Tendency (Mean vs. Median), Spread (StdDev, Variance), Quartiles, and IQR outlier boundaries.
4. **Pivot Table Mastery:** Summarizing thousands of records by Category, Timeline, Geography, and Customer Lifetime Value.
5. **Interactive Dashboard Design:** Building KPI cards, dynamic Pivot Charts, and multi-slicer synchronization.

---

## 🗂️ 2. Workbook Architecture (5-Sheet Structure)

The workbook `TechNova_Excel.xlsx` follows professional financial and BI spreadsheet design principles, separating data layers from calculation and presentation layers:

```text
TechNova_Excel.xlsx
├── 1. Raw Data          # Unaltered messy source data (5,000 transaction rows)
├── 2. Cleaned Data      # Sanitized table with calculated financial metrics (A:T)
├── 3. Pivot Analysis    # 4 dedicated summary Pivot Tables for multi-angle reporting
├── 4. KPI Summary       # Formula-driven KPI scorecard & statistical benchmarks
└── 5. Dashboard         # Executive visual interface with KPI cards, charts & slicers
```

---

## 🧹 3. Step-by-Step Data Cleaning (Sheet: `2. Cleaned Data`)

Import the messy dataset from `1. Raw Data` into `2. Cleaned Data` and apply the following cleaning functions:

| # | Target Column | Problem Identified in Raw Data | Excel Formula / Solution | Cleaned Example |
|---|---------------|--------------------------------|--------------------------|-----------------|
| **1** | `FullName` | Inconsistent casing (`CUSTOMER_0`, `customer_0`) & extra spaces | `=PROPER(TRIM('1. Raw Data'!B2))` | `Customer_0` |
| **2** | `Age` | Impossible outlier ages (`-5`, `180`) | `=IF(OR(C2<18, C2>100), MEDIAN($C$2:$C$5001), C2)` | `35` |
| **3** | `Category` | Typos and abbreviations (`Elec`, `elect`) | `=IF(OR(L2="Elec", L2="elect"), "Electronics", L2)` | `Electronics` |
| **4** | `Cost` | Missing values (nulls) | `=IF(ISBLANK('1. Raw Data'!N2), MEDIAN($N$2:$N$5001), '1. Raw Data'!N2)` | `$334.36` |
| **5** | `Discount` | Blank cells for orders without discounts | `=IF(ISBLANK('1. Raw Data'!P2), 0.0, '1. Raw Data'!P2)` | `0.00%` |
| **6** | `OrderDate` | Mixed formats (`MM/DD/YYYY` vs `DD-MM-YYYY`) | `=DATEVALUE(...)` or **Data → Text to Columns** (Date: MDY) | `2023-02-08` |

### 🧮 Financial Calculations Added (Columns S & T):

1. **Realized Revenue (Column S):**
   ```excel
   =Price * Quantity * (1 - Discount)
   # Excel Formula in Cell S2:
   =M2 * O2 * (1 - P2)
   ```
2. **Gross Profit (Column T):**
   ```excel
   =Revenue - (Cost * Quantity)
   # Excel Formula in Cell T2:
   =S2 - (N2 * O2)
   ```
3. **Profit Margin %:**
   ```excel
   =Profit / Revenue
   # Excel Formula:
   =T2 / S2
   ```

---

## 📈 4. Descriptive Statistics & Outlier Detection (Day 2 Focus)

To understand customer distribution and detect anomalous spending behavior, compute descriptive statistics across the customer base:

### A. Measures of Central Tendency & Spread
| Metric | Excel Formula | TechNova Benchmark Value | Business Interpretation |
|--------|---------------|--------------------------|-------------------------|
| **Mean Revenue** | `=AVERAGE('2. Cleaned Data'!S2:S5001)` | `$2,279.72` | Average order transaction size |
| **Median Revenue** | `=MEDIAN('2. Cleaned Data'!S2:S5001)` | `$1,824.50` | Midpoint spending (resistant to whale buyers) |
| **Standard Deviation** | `=STDEV.S('2. Cleaned Data'!S2:S5001)` | `$1,465.18` | High variability in order basket sizes |
| **Variance** | `=VAR.S('2. Cleaned Data'!S2:S5001)` | `2,146,752.4` | Squared dispersion from the mean |
| **Min / Max Spend** | `=MIN(...)` / `=MAX(...)` | `$48.50` / `$14,850.00` | Full range of single-order transactions |

### B. Outlier Detection using Interquartile Range (IQR)
1. **First Quartile (Q1 - 25th Percentile):**
   ```excel
   =QUARTILE.INC('2. Cleaned Data'!S2:S5001, 1)
   ```
2. **Third Quartile (Q3 - 75th Percentile):**
   ```excel
   =QUARTILE.INC('2. Cleaned Data'!S2:S5001, 3)
   ```
3. **Interquartile Range (IQR):**
   ```excel
   =Q3_Cell - Q1_Cell
   ```
4. **Outlier Threshold Limits:**
   - **Upper Outlier Boundary:** `=Q3 + (1.5 * IQR)`
   - **Lower Outlier Boundary:** `=Q1 - (1.5 * IQR)`
   *(Any transaction above the upper boundary represents an enterprise/bulk wholesale purchase).*

---

## 📊 5. Pivot Table Construction (Sheet: `3. Pivot Analysis`)

Create 4 core Pivot Tables to feed into the executive dashboard:

### 🔹 Pivot Table 1: Category Performance
- **Source:** `'2. Cleaned Data'!$A$1:$T$5001`
- **Rows:** `Category`
- **Values:**
  - `Sum of Revenue` (Format: Currency `$#,##0`)
  - `Sum of Profit` (Format: Currency `$#,##0`)
  - `Average of Discount` (Format: Percentage `0.0%`)
  - `Count of OrderID` (Format: Number `#,##0`)
- **Calculated Field:** `Profit Margin = Profit / Revenue` (Format: Percentage `0.0%`)

### 🔹 Pivot Table 2: Monthly Revenue & Order Trend
- **Rows:** `OrderDate` $\rightarrow$ Right-click $\rightarrow$ **Group by: Years and Months**
- **Values:**
  - `Sum of Revenue` (Format: Currency `$#,##0`)
  - `Count of OrderID` (Format: Number `#,##0`)

### 🔹 Pivot Table 3: Top 15 Customers by Profitability
- **Rows:** `FullName`
- **Values:** `Sum of Profit`, `Sum of Revenue`
- **Filter:** Click Row Labels dropdown $\rightarrow$ **Value Filters $\rightarrow$ Top 10... $\rightarrow$ Top 15 by Sum of Profit**

### 🔹 Pivot Table 4: Regional Geographic Performance
- **Rows:** `City`
- **Columns:** `ShipMode`
- **Values:** `Sum of Revenue`

---

## 🎯 6. Executive KPI Summary (Sheet: `4. KPI Summary`)

Build a dynamic KPI summary table using standard Excel aggregation formulas:

```excel
========================================================================================
KPI METRIC                       EXCEL FORMULA                           RESULT VALUE
========================================================================================
Total Revenue                    =SUM('2. Cleaned Data'!S2:S5001)        $11,398,597.08
Total Profit                     =SUM('2. Cleaned Data'!T2:T5001)        $4,869,126.93
Gross Profit Margin (%)          =B4 / B3                                42.72%
Total Orders (Volume)            =COUNTA('2. Cleaned Data'!G2:G5001)-1   5,000
Unique Customers                 =COUNTA(UNIQUE('2. Cleaned Data'!A2:A5001)) 1,433
Average Order Value (AOV)        =AVERAGE('2. Cleaned Data'!S2:S5001)    $2,279.72
Average Discount Given           =AVERAGE('2. Cleaned Data'!P2:P5001)    3.46%
Overall Customer Churn Rate      =COUNTIF('2. Cleaned Data'!F:F, 1)/5000 28.92%
Active Customer Count            =COUNTIF('2. Cleaned Data'!F:F, 0)      872 Customers
Churned Customer Count           =COUNTIF('2. Cleaned Data'!F:F, 1)      561 Customers
========================================================================================
```

---

## 🖥️ 7. Dashboard Design & Layout (Sheet: `5. Dashboard`)

Construct an executive presentation layout in Sheet `5. Dashboard`:

### 🎨 Visual Layout Map:
```text
+---------------------------------------------------------------------------------------+
|  TECHNOVA RETAIL SALES & PROFITABILITY DASHBOARD                                      |
+---------------------------------------------------------------------------------------+
| [ CARD 1 ]          | [ CARD 2 ]          | [ CARD 3 ]          | [ CARD 4 ]          |
| Total Revenue       | Total Profit        | Profit Margin       | Total Orders        |
| $11.40M             | $4.87M              | 42.7%               | 5,000               |
+---------------------+---------------------+---------------------+---------------------+
| [ CHART 1 ]                               | [ CHART 2 ]                               |
| Revenue & Profit by Product Category      | Monthly Revenue Trend (2020 - 2023)       |
| (Clustered Column Chart)                  | (Line Chart with Data Markers)            |
+-------------------------------------------+-------------------------------------------+
| [ CHART 3 ]                               | [ SLICERS & TIMELINE CONTROLS ]           |
| Top 15 Most Profitable Customers          | 🔹 Category Slicer (Multi-Select)         |
| (Horizontal Bar Chart)                    | 🔹 City / Region Slicer                   |
|                                           | 🔹 Ship Mode Slicer                       |
|                                           | 📅 Order Date Timeline Slider             |
+-------------------------------------------+-------------------------------------------+
```

### 🔗 Connecting Slicers to Multiple Pivot Tables:
1. Insert Slicers for **Category**, **City**, and **ShipMode**.
2. Right-click each Slicer $\rightarrow$ **Report Connections...** (or Slicer Connections).
3. Check the boxes for **all 4 Pivot Tables** in `3. Pivot Analysis`.
4. Now, filtering any slicer will instantly update all KPI cards and charts simultaneously!

---

## 👨‍🏫 8. Instructor Delivery & Workshop Timing

| Session Segment | Duration | Topic & Student Milestone |
|-----------------|:--------:|---------------------------|
| **Part 1: Crash Course** | 45 min | Excel UI, absolute references (`$A$1`), text cleaning formulas (`TRIM`, `PROPER`). |
| **Part 2: Cleaning Lab** | 45 min | Hands-on data cleaning, date parsing, and calculating `Revenue` & `Profit`. |
| **Break** | 30 min | Rest & Q&A. |
| **Part 3: Stats & Pivots** | 40 min | Mean/Median spread, IQR outlier detection, creating the 4 Pivot Tables. |
| **Part 4: Dashboard Build** | 50 min | Designing KPI cards, Pivot Charts, formatting palettes, and linking Slicers. |

---

### 💡 Golden Rules for Students:
- ❌ **Never type raw numbers inside formulas** — always reference cell headers or named ranges.
- 🔒 **Always lock lookup ranges** using `F4` (`$A$2:$T$5001`) to avoid range shifting during autofill.
- 🎯 **80/20 Rule:** 80% of data errors come from messy text and improper date formats; master `TRIM`, `PROPER`, and `DATEVALUE`.
