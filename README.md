[README.md](https://github.com/user-attachments/files/31162522/README.md)
# 🚀 TechNova Retail & Customer Churn Analytics
### Science in Code (SIC) Bootcamp — End-to-End Data Analysis Capstone Project

---

## 📖 The Business Problem

**TechNova** is a rapidly growing omni-channel electronics and consumer technology retailer operating across 6 major cities in Egypt. Recently, executive leadership identified several critical challenges:
- 📉 A noticeable **drop in profitability** across specific product lines despite steady revenue growth.
- 🚪 A **rising customer churn rate** (~29% of customers haven't made a purchase in over 6 months).
- 🎯 The absence of an integrated, data-driven system to **predict and prevent** customer churn before it occurs.

### 🎯 Project Mission:
1. **Clean & Standardize** 5,000 messy transactional records (handling missing costs/discounts, casing, and date formats).
2. **Perform Statistical Analysis** to detect anomalies, quantify variance, and compute core business KPIs.
3. **Query the Relational Database** using advanced SQL (JOINs, CTEs, Window Functions) to uncover behavioral insights.
4. **Build Interactive Power BI Dashboards** with a normalized Star Schema and DAX time intelligence.
5. **Train a Logistic Regression Machine Learning Model** to accurately predict customer churn probability.
6. **Deploy an Interactive Streamlit Web Application** for real-time risk scoring and batch data analysis.

---

## 🗓️ Bootcamp Curriculum & Day-by-Day Mapping

This project serves as the **unified capstone case study** across the 6-day intensive SIC Data Analysis Bootcamp:

| Day | Track Module | Key Deliverable | Core Tools & Skills |
|:---:|:---|:---|:---|
| **Day 1** | **Foundations & Excel Mastery** | [`TechNova_Excel.xlsx`](Day_1%262_Excel/TechNova_Excel.xlsx) | Data cleaning, `PROPER`/`TRIM`, `IF`, `XLOOKUP`, Pivot Tables, Charts, Slicers |
| **Day 2** | **Statistics & Business Metrics** | `TechNova_Excel.xlsx` (KPI sheet) | Mean, Median, Mode, StdDev, IQR Outliers, AOV, Churn Rate, Margins |
| **Day 3** | **SQL for Data Analysis** | [`TechNova_Queries.sql`](Day_3_SQL/TechNova_Queries.sql) | `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `JOIN`s, CTEs, Window Functions |
| **Day 4** | **Business Intelligence (BI)** | Power BI Dashboards (`.pbix`) | Star Schema Data Modeling, DAX Measures, Slicers, Interactive Reporting |
| **Day 5** | **Python, EDA & Machine Learning** | [`TechNova_Python_EDA.ipynb`](Day_5_Python_ML/TechNova_Python_EDA.ipynb) + [`streamlit_app.py`](Day_5_Python_ML/streamlit_app.py) | Pandas, Seaborn, Feature Engineering, Logistic Regression, Streamlit Web App |
| **Day 6** | **Hackathon & Presentations** | Executive Presentations | End-to-End Delivery: Data $\rightarrow$ Insight $\rightarrow$ Business Action |

---

## 📂 Project Directory Structure

```text
SIC_Bootcamp_TechNova_Project/
│
├── Datasets/
│   ├── dataset_raw.csv                 # 5,000-row synthetic dataset with intentional real-world anomalies
│   └── dataset_cleaned.csv             # Sanitized dataset with calculated Revenue & Profit
│
├── Day_1&2_Excel/
│   ├── TechNova_Excel.xlsx             # 5 sheets: Raw Data, Cleaned Data, Pivot Analysis, KPIs, Dashboard
│   └── Excel_Development_Guide.md      # Step-by-step development & instructor guide for Excel
│
├── Day_3_SQL/
│   └── TechNova_Queries.sql            # 7 SQL queries (Basics, Aggregations, JOINs, CTEs, Window Funcs)
│
├── Day_4_BI/
│   ├── TechNova_PowerBI_V1.pbix        # Power BI Baseline Dashboard
│   ├── TechNova_PowerBI_V2.pbix        # Power BI Advanced Star Schema Dashboard
│   └── BI_Development_Guide.md         # Step-by-step Power BI development guide
│
├── Day_5_Python_ML/
│   ├── TechNova_Python_EDA.ipynb       # Jupyter Notebook: 9-step EDA, Feature Engineering & Logistic Regression
│   ├── streamlit_app.py                # Multi-tab interactive Streamlit web application
│   └── models/
│       ├── churn_model.pkl             # Trained Logistic Regression model
│       ├── scaler.pkl                  # Fitted StandardScaler
│       └── model_metadata.json         # Model parameters, accuracy & feature schema
│
├── README.md                           # Main project documentation (this file)
└── requirements.txt                    # Project Python dependencies
```

---

## 🧪 Dataset Schema & Data Dictionary

The dataset represents a denormalized enterprise retail schema consisting of 5,000 transactional rows:

### 👤 Customers (Dimension)
| Column | Type | Description / Anomalies |
|---|:---:|---|
| `CustomerID` | `INT` | Unique identifier per customer (PK: 1000–2500) |
| `FullName` | `TEXT` | ⚠️ *Messy:* Inconsistent casing and extra leading/trailing whitespace |
| `Age` | `INT` | ⚠️ *Messy:* Contains unrealistic outlier values ($<18$ or $>100$) |
| `City` | `TEXT` | Customer location (Cairo, Alexandria, Giza, Mansoura, Luxor, Aswan) |
| `JoinDate` | `DATE` | ⚠️ *Messy:* Mixed date formats (`MM/DD/YYYY` vs. `DD-MM-YYYY`) |
| `Churn` | `BINARY` | Target label: `1` = Churned (inactive), `0` = Active |

### 📦 Products (Dimension)
| Column | Type | Description / Anomalies |
|---|:---:|---|
| `ProductID` | `INT` | Unique product identifier (PK: 101–149) |
| `ProductName` | `TEXT` | Product SKU name (e.g., `Product_135`) |
| `Category` | `TEXT` | ⚠️ *Messy:* Typographical variations (e.g., `Elec`, `elect` $\rightarrow$ `Electronics`) |
| `Price` | `FLOAT` | Retail unit price ($50.00 – $1,500.00) |
| `Cost` | `FLOAT` | ⚠️ *Messy:* ~5% missing values (requires median imputation) |

### 🛒 Orders & Details (Fact Records)
| Column | Type | Description / Anomalies |
|---|:---:|---|
| `OrderID` | `INT` | Unique transaction ID (10000–14000) |
| `OrderDate` | `DATE` | Date of purchase transaction |
| `ShipMode` | `TEXT` | Delivery speed (`Standard`, `Express`, `Same Day`) |
| `Quantity` | `INT` | Basket items ordered (1–5 items) |
| `Discount` | `FLOAT` | ⚠️ *Messy:* ~70% nulls (imputed as `0.0` for full-price purchases) |

### 🧮 Engineered & Calculated Metrics
| Derived Column | Type | Formula / Logic |
|---|:---:|---|
| `Revenue` | `FLOAT` | `Price × Quantity × (1 - Discount)` |
| `Profit` | `FLOAT` | `Revenue - (Cost × Quantity)` |
| `Profit_Margin` | `FLOAT` | `Profit / Revenue` |
| `Days_Since_Last_Order` | `INT` | Recency metric (days elapsed since most recent transaction) |
| `Total_Orders` | `INT` | Frequency metric (lifetime order count per customer) |

---

## 📈 Machine Learning Model Performance

The churn prediction model is built using **Logistic Regression** and **StandardScaler** to ensure high interpretability and robust generalization:

| Metric | Score / Configuration |
|---|:---:|
| **Algorithm** | **Logistic Regression** (`sklearn.linear_model.LogisticRegression`) |
| **Optimization Solver** | L-BFGS (`max_iter=500, random_state=42`) |
| **Preprocessing** | `StandardScaler` (Z-score normalization: $\mu=0, \sigma=1$) |
| **Test Accuracy** | **81.88%** |
| **AUC-ROC Score** | **0.8815** |
| **F1-Score** | **0.7476** |
| **Feature Inputs (6)** | `Age`, `Total_Spent`, `Days_Since_Last_Order`, `Total_Orders`, `Avg_Discount`, `Avg_Profit` |
| **Target Variable** | `Churn` (`1` = Churned, `0` = Active) |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Power BI Desktop (for Day 4 `.pbix` files)
- Microsoft Excel 2016+ or Microsoft 365

### 2. Installation
Clone the repository and install all required Python libraries:
```bash
git clone https://github.com/ScienceInCode/SIC_Bootcamp_TechNova_Project.git
cd SIC_Bootcamp_TechNova_Project
pip install -r requirements.txt
```

### 3. Launching the Interactive Streamlit Web App
```bash
cd Day_5_Python_ML
streamlit run streamlit_app.py
```

### 4. Running the EDA Notebook
```bash
cd Day_5_Python_ML
jupyter notebook TechNova_Python_EDA.ipynb
```

### 5. Accessing Development Guides
- **Excel Guide (Day 1 & 2):** [`Day_1&2_Excel/Excel_Development_Guide.md`](Day_1%262_Excel/Excel_Development_Guide.md)
- **Power BI Guide (Day 4):** [`Day_4_BI/BI_Development_Guide.md`](Day_4_BI/BI_Development_Guide.md)

---

## 🎓 Instructor Delivery Notes: The "Baton Pass" Method

To provide students with a unified narrative across the 6-day bootcamp, instructors can use the **Baton Pass** technique to seamlessly bridge each day to the next:

| Day | Opening Transition | Closing "Baton Pass" |
|---|---|---|
| **Day 1** | *"TechNova is experiencing profit drops. Let's clean their raw data and build a sales dashboard to see what's happening."* | *"We organized the numbers, but we still don't know WHY profits fluctuate. Tomorrow: Statistics & Outlier Detection."* |
| **Day 2** | *"Yesterday we cleaned the data. Today we interrogate it with descriptive statistics and business metrics."* | *"Excel is powerful for 5,000 rows, but what if TechNova scales to 5 million records? Tomorrow: SQL Databases."* |
| **Day 3** | *"Spreadsheets hit scale limits. Today we talk directly to databases with SQL."* | *"We answered deep business questions with SQL, but executives want visual stories. Tomorrow: Power BI Dashboards."* |
| **Day 4** | *"Yesterday's SQL queries become today's dynamic executive dashboards in Power BI."* | *"We know what HAPPENED in the past. But can we PREDICT who will leave next? Tomorrow: Python & Machine Learning."* |
| **Day 5** | *"We've cleaned, queried, and visualized. Today we build a live ML model to predict customer churn."* | *"You now have the full modern data stack. Tomorrow: Hackathon & Executive Presentations!"* |

---

*Developed for the **Science in Code (SIC)** Community | Data Analysis Track*
