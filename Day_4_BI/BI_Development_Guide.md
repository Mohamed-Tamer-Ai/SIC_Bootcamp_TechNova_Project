# 📊 TechNova BI Development Guide — Day 4

> **SIC Bootcamp | Day 4: Business Intelligence**
> This guide provides detailed, step-by-step instructions for instructors and students to build professional BI dashboards using Power BI. This version has been fully updated to include advanced Data Modeling (Star Schema) and corrected DAX measures.

---

## 📁 Data Sources

| File | Description | Use For |
|------|-------------|---------|
| `dataset_raw.csv` | Original messy data (5,000 rows) | Power Query cleaning exercise |
| `dataset_cleaned.csv` | Pre-cleaned data with Revenue & Profit | Quick import for dashboards |

> **Instructor Tip:** For the full learning experience, have students import `dataset_raw.csv` and clean it in Power Query. The steps below guide you through splitting this flat file into a professional Star Schema.

---

## 🟢 POWER BI IMPLEMENTATION

### Step 1: Data Import & Power Query Cleaning

1. Open **Power BI Desktop**
2. Click **Home → Get Data → Text/CSV**
3. Select `dataset_raw.csv` → Click **Transform Data**

**In Power Query Editor, apply these transformations to your initial query:**

| # | Column | Transformation | How |
|---|--------|---------------|-----|
| 1 | `FullName` | Fix casing & spaces | Select column → Transform → Format → **Trim** → then **Capitalize Each Word** |
| 2 | `Cost` | Fill missing values | Select column → Transform → **Replace Values** (null → `350`) |
| 3 | `Discount` | Fill missing values | Select column → Transform → **Replace Values** (null → `0`) |
| 4 | `Category` | Fix abbreviations | Select column → Transform → **Replace Values**: `Elec` → `Electronics`, `elect` → `Electronics` |
| 5 | `OrderDate` | Parse as Date | Add Custom Column: `try Date.From([OrderDate], "en-US") otherwise Date.From([OrderDate], "en-GB")`. Remove old column, rename new to `OrderDate`, set type to Date. |
| 6 | `Age` | Remove outliers | Select column → **Remove Rows → Remove Errors**, then Filter: `Age >= 18 AND Age <= 100` |

---

### Step 2: Data Modeling (Star Schema)

To avoid Many-to-Many relationship errors and build a robust model, split the flat table into Dimension tables and a Fact table.

**A. Create the Customers Dimension:**
1. Right-click the original query and select **Duplicate**. Rename it to `Customers`.
2. Select only the customer attributes: `CustomerID`, `FullName`, `Age`, `City`, `JoinDate`, and `Churn`.
3. Right-click a selected header → **Remove Other Columns**.
4. Right-click `CustomerID` → **Remove Duplicates**.

**B. Create the Products Dimension:**
1. Right-click the original query and select **Duplicate**. Rename it to `Products`.
2. Select only the product attributes: `ProductID`, `ProductName`, and `Category`.
3. Right-click a selected header → **Remove Other Columns**.
4. Right-click `ProductID` → **Remove Duplicates**.

**C. Clean the Fact Table:**
1. Rename the original query to `dataset_cleaned`.
2. Remove the descriptive columns you just moved (e.g., `FullName`, `Age`, `City`, `JoinDate`, `Churn`, `ProductName`, `Category`). Keep only the IDs (`CustomerID`, `ProductID`) and the transactional data (`OrderDate`, `OrderID`, `Price`, `Quantity`, `Cost`, `Discount`).
3. Click **Close & Apply**.

**D. Create the Calendar Dimension:**
1. Go to **Model View**.
2. Click Modeling → **New Table** and enter this DAX:

```dax
Calendar = 
ADDCOLUMNS(
    CALENDAR(MIN('dataset_cleaned'[OrderDate]), MAX('dataset_cleaned'[OrderDate])),
    "Year",  YEAR([Date]),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNum", MONTH([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "YearMonth", FORMAT([Date], "YYYY-MM")
)
```

3. Mark as Date Table: Select `Calendar` → Table tools → **Mark as date table** → Select `Date`.

**E. Build Relationships (Drag and Drop in Model View):**
*   `Calendar[Date]` → `dataset_cleaned[OrderDate]` (1-to-Many)
*   `Customers[CustomerID]` → `dataset_cleaned[CustomerID]` (1-to-Many)
*   `Products[ProductID]` → `dataset_cleaned[ProductID]` (1-to-Many)

---

### Step 3: DAX Measures

Create a dedicated **Measures Table** to organize your calculations:
1. Click Modeling → **New Table**.
2. Enter: `_Measures = {BLANK()}` (Using the underscore prevents reserved name errors).
3. Do not hide the blank column yet. Right-click `_Measures` → **New Measure** to add the formulas below one by one. Once the first measure is added, you can hide the original blank column.

```dax
-- REVENUE MEASURES
Total Revenue = 
SUMX('dataset_cleaned', 'dataset_cleaned'[Price] * 'dataset_cleaned'[Quantity] * (1 - 'dataset_cleaned'[Discount]))

Total Cost = 
SUMX('dataset_cleaned', 'dataset_cleaned'[Cost] * 'dataset_cleaned'[Quantity])

Total Profit = 
[Total Revenue] - [Total Cost]

Profit Margin % = 
DIVIDE([Total Profit], [Total Revenue], 0)

-- CUSTOMER MEASURES
Total Customers = 
DISTINCTCOUNT('dataset_cleaned'[CustomerID])

Churned Customers = 
CALCULATE(DISTINCTCOUNT('dataset_cleaned'[CustomerID]), 'Customers'[Churn] = 1)

Churn Rate % = 
DIVIDE([Churned Customers], [Total Customers], 0)

-- AVERAGE MEASURES
Avg Order Value = 
DIVIDE([Total Revenue], COUNTROWS('dataset_cleaned'), 0)

-- TIME INTELLIGENCE (requires Calendar table)
Revenue YTD = 
TOTALYTD([Total Revenue], 'Calendar'[Date])

Revenue MoM Growth % = 
VAR Current_Month = [Total Revenue]
VAR Prev_Month = CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))
RETURN DIVIDE(Current_Month - Prev_Month, Prev_Month, 0)
```

---

### Step 4: Dashboard Layout

Build the dashboard in **Report View** with this layout. 

> **Design Tip:** To create a highly engaging interface, apply a dark theme background with neon cyberpunk visual aesthetics (e.g., neon purple and blue lighting accents) paired with clean, technical layouts for your visuals.

```text
┌────────────────────────────────────────────────────────┐
│  [CARD]        [CARD]        [CARD]        [CARD]      │
│  Revenue       Profit        Margin%       Churn%      │
├────────────────────────┬───────────────────────────────┤
│                        │                               │
│  [LINE CHART]          │  [CLUSTERED BAR CHART]        │
│  Revenue Trend by      │  Revenue & Profit by          │
│  Month (Time Intel.)   │  Category                     │
│                        │                               │
├────────────────────────┼───────────────────────────────┤
│                        │                               │
│  [MAP VISUAL]          │  [MATRIX TABLE]               │
│  Revenue by City       │  Category × City breakdown    │
│  (Bubble size =        │  with Data Bars &             │
│   Revenue)             │  Conditional Formatting       │
│                        │                               │
├────────────────────────┴───────────────────────────────┤
│  [SLICER: City]  [SLICER: Category]  [SLICER: Year]    │
└────────────────────────────────────────────────────────┘
```

**Visual-by-Visual Instructions:**

| # | Visual Type | Field Mapping | Formatting |
|---|------------|---------------|------------|
| 1 | **Card** (×4) | One card each for: `Total Revenue`, `Total Profit`, `Profit Margin %`, `Churn Rate %` | Format → Display units: Auto. Font size: 28 |
| 2 | **Line Chart** | X-axis: `Calendar[YearMonth]`, Y-axis: `Total Revenue` | Add trend line. Marker ON |
| 3 | **Clustered Bar** | X-axis: `Products[Category]`, Y-axis: `Total Revenue` + `Total Profit` | Sort by Revenue DESC |
| 4 | **Map** | Location: `Customers[City]`, Size: `Total Revenue` | Use Bing Maps. Bubble color: custom theme |
| 5 | **Matrix** | Rows: `Products[Category]`, Columns: `Customers[City]`, Values: `Total Profit` | Turn on Conditional Formatting → Data Bars |
| 6 | **Slicers** (×3) | One each for `Customers[City]`, `Products[Category]`, `Calendar[Year]` | Style: Dropdown |