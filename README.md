[README.md](https://github.com/user-attachments/files/31162272/README.md)
# 🚀 TechNova Retail & Customer Churn
### SIC Bootcamp — End-to-End Data Analysis Project

---

## 📖 The Business Problem

**TechNova** is a global e-commerce electronics retailer operating across 6 cities in Egypt. Recently, the company has noticed:
- 📉 A significant **drop in profitability** across certain product categories
- 🚪 A **high rate of customer churn** (~40% of customers have stopped purchasing)
- 🎯 No data-driven system to **predict** which customers are at risk

The CEO has tasked the data team to:
1. Clean and standardize the raw transaction data
2. Perform statistical analysis to identify anomalies and KPIs
3. Query the relational database for deep business insights
4. Build automated, interactive BI dashboards for executives
5. Develop a Machine Learning model to predict churn before it happens
6. Deploy the model as a web application for the marketing team

---

## 🗓️ Bootcamp Day Mapping

This project serves as the **unified case study** across all 5 technical days of the SIC Bootcamp:

| Day | Topic | Deliverable | Key Skills |
|-----|-------|-------------|------------|
| **Day 1** | Foundations & Excel | `TechNova_Excel.xlsx` | Data cleaning, PROPER/TRIM, IF, XLOOKUP, Pivot Tables, Charts, Slicers |
| **Day 2** | Statistics & Metrics | `TechNova_Excel.xlsx` (KPI sheet) | Mean, Median, Mode, IQR, Z-scores, AOV, Churn Rate, Profit Margin |
| **Day 3** | SQL for Data Analysis | `TechNova_Queries.sql` | SELECT, WHERE, GROUP BY, JOINs, CTEs, Window Functions, CASE |
| **Day 4** | Business Intelligence | Power BI Dashboards | Star Schema, DAX, Time Intelligence, Interactive Dashboards |
| **Day 5** | Python & ML | `TechNova_Python_EDA.ipynb` + `streamlit_app.py` | Pandas, Seaborn, Feature Engineering, Logistic Regression, Streamlit |
| **Day 6** | Hackathon | Team presentations | Full pipeline: Clean → Analyze → Visualize → Present |

---

## 📂 Project Structure

```
SIC_Bootcamp_TechNova_Project/
│
├── data/
│   ├── dataset_raw.csv              # 5,000-row synthetic dataset with intentional messy data
│   └── dataset_cleaned.csv          # Pre-cleaned version with Revenue & Profit calculated
│
├── day1_2_excel/
│   └── TechNova_Excel.xlsx          # 5 sheets: Raw Data, Cleaned Data, Pivot Analysis, KPIs, Dashboard
│   └── Excel_Development_Guide.md   # Step-by-step instructions for Excel
│
├── day3_sql/
│   └── TechNova_Queries.sql         # 7 queries covering SELECT, JOINs, CTEs, Window Functions, CASE
│
├── day4_bi/
│   ├── TechNova_PowerBI_V1.pbix     # Power BI Initial version
│   ├── TechNova_PowerBI_V2.pbix     # Power BI Advanced version
│   └── BI_Development_Guide.md      # Step-by-step instructions for Power BI
│
├── day5_python_ml/
│   ├── TechNova_Python_EDA.ipynb    # Jupyter Notebook: EDA, Feature Engineering, Model Training
│   ├── streamlit_app.py             # Web app for real-time churn prediction
│   └── models/                      # Contains trained Logistic Regression model and scaler
│
├── scripts/
│   └── Project Generation Files/    # Python scripts used to generate the project data and structure
│
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

---

## 🧪 Dataset Schema

The raw dataset simulates a **denormalized view** of 4 relational tables:

### Customers (Dimension)
| Column | Type | Notes |
|--------|------|-------|
| `CustomerID` | INT | Primary Key (1000-2500) |
| `FullName` | TEXT | ⚠️ Messy: inconsistent casing, extra spaces |
| `Age` | INT | ⚠️ Messy: some negative values or >100 |
| `City` | TEXT | Cairo, Alexandria, Giza, Mansoura, Luxor, Aswan |
| `JoinDate` | DATE | ⚠️ Messy: mixed formats (MM/DD/YYYY and DD-MM-YYYY) |
| `Churn` | BINARY | Target variable: 1 = Churned, 0 = Active |

### Products (Dimension)
| Column | Type | Notes |
|--------|------|-------|
| `ProductID` | INT | Primary Key (101-149) |
| `ProductName` | TEXT | Format: "Product_XXX" |
| `Category` | TEXT | ⚠️ Messy: "Elec" and "elect" instead of "Electronics" |
| `Price` | FLOAT | Retail price ($50-$1,500) |
| `Cost` | FLOAT | ⚠️ Messy: ~5% missing values |

### Orders (Fact)
| Column | Type | Notes |
|--------|------|-------|
| `OrderID` | INT | Primary Key (10000-14000) |
| `OrderDate` | DATE | Same as JoinDate (simplified) |
| `ShipMode` | TEXT | Standard, Express, Same Day |

### OrderDetails (Fact Line Items)
| Column | Type | Notes |
|--------|------|-------|
| `Quantity` | INT | 1-5 items per order |
| `Discount` | FLOAT | ⚠️ Messy: ~70% are NULL (should be 0) |

### Derived Features (in cleaned data)
| Column | Type | Formula |
|--------|------|---------|
| `Revenue` | FLOAT | `Price × Quantity × (1 - Discount)` |
| `Profit` | FLOAT | `Revenue - (Cost × Quantity)` |
| `Days_Since_Last_Order` | INT | Days since last purchase (ML feature) |
| `Total_Orders` | INT | Total distinct orders (ML feature) |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ installed
- Jupyter Notebook or VS Code with Jupyter extension
- Power BI Desktop (Windows)

### Step 1: Install Python Dependencies
```bash
cd "C:\Users\MOHAMED TAMER\Desktop\SIC\SIC_Bootcamp_TechNova_Project"
pip install -r requirements.txt
```

### Step 2: Explore the EDA Notebook
```bash
cd day5_python_ml
jupyter notebook TechNova_Python_EDA.ipynb
```

### Step 3: Launch the Churn Prediction Web App
```bash
cd day5_python_ml
streamlit run streamlit_app.py
```
This opens a browser window where you can input customer data and get real-time churn predictions.

### Step 4: Build the BI Dashboards
Navigate to the `day4_bi` folder and follow the detailed instructions in `BI_Development_Guide.md` to build the Power BI dashboard.

---

## 📈 ML Model Performance

| Metric | Value |
|--------|-------|
| **Algorithm** | Logistic Regression |
| **Accuracy** | 81.88% |
| **AUC-ROC** | 0.8815 |
| **Features** | Age, Total_Spent, Days_Since_Last_Order, Total_Orders, Avg_Discount, Avg_Profit |
| **Scaling** | StandardScaler |
| **Training Config** | random_state=42, max_iter=500 |

---

## 🎓 Instructor Notes: The "Baton Pass" Technique

To make the bootcamp feel like one continuous journey rather than 5 disjointed workshops:

| Day | Opening Line | Closing "Baton Pass" |
|-----|-------------|---------------------|
| **Day 1** | *"TechNova is losing money. Let's clean their data and find out why."* | *"We built a dashboard, but we still don't know WHY profits are dropping. Tomorrow: Statistics."* |
| **Day 2** | *"Yesterday we cleaned the data. Today we interrogate it."* | *"Excel is great, but what if TechNova scales to 5 million rows? Tomorrow: SQL."* |
| **Day 3** | *"Spreadsheets can't handle big data. Let's talk to databases directly."* | *"We have answers in SQL, but executives don't read code. Tomorrow: BI dashboards."* |
| **Day 4** | *"Yesterday's SQL answers become today's interactive dashboards."* | *"We know what HAPPENED. But can we predict what WILL happen? Tomorrow: Python & ML."* |
| **Day 5** | *"We've cleaned, queried, and visualized. Now we PREDICT the future."* | *"You are now full-stack Data Analysts. Tomorrow: prove it in the Hackathon."* |

---

*Prepared by: SIC Head of Data Analysis | Science in Code Community*
