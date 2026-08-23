# 🗄️ TechNova SQL Development Guide — Day 3

> **SIC Bootcamp | Day 3: SQL for Data Analysis**
> This guide walks instructors and students through transforming a flat transactional dataset into a robust relational database and extracting business intelligence using SQL.

---

## 📌 1. Project Overview & Business Context

**TechNova Retail** is an omnichannel consumer tech and electronics retailer experiencing rapid sales growth but facing unexplained margin fluctuations and rising customer churn. 

In this session, we transition from analyzing **5,000 messy rows** in flat files to managing them in a structured **Relational Database**. By leveraging SQL, students will build queries that answer critical business questions, calculate financial KPIs on the fly, and uncover deep customer insights.

### 🎯 Key Learning Objectives:
1. **Database Creation & Schema Design:** Normalizing flat files into a Star Schema (Fact and Dimension tables).
2. **Foundational Querying:** Using `SELECT`, `WHERE`, and arithmetic operations to filter and calculate data.
3. **Data Aggregation:** Summarizing large datasets using `GROUP BY` and filtering aggregates with `HAVING`.
4. **Relational Analysis:** Combining tables using `JOIN` to uncover cross-dimensional insights.
5. **Advanced Analytics:** Utilizing Common Table Expressions (CTEs) for modular logic and Window Functions for time-series analysis (Running Totals, MoM Growth).

---

## 🏗️ 2. Database Architecture (ERD & Schema Design)

To avoid data redundancy and ensure integrity, we will normalize our original flat file into a simple **Star Schema**. 

Below are the Data Definition Language (DDL) statements used to create our tables in the SQL database.

```sql
-- 1. Create the Customers Dimension Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FullName VARCHAR(100),
    Age INT,
    City VARCHAR(50),
    JoinDate DATE,
    Churn INT -- 1 for Churned, 0 for Active
);

-- 2. Create the Products Dimension Table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50)
);

-- 3. Create the Transactions Fact Table
CREATE TABLE Transactions (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    OrderDate DATE,
    Price DECIMAL(10, 2),
    Quantity INT,
    Cost DECIMAL(10, 2),
    Discount DECIMAL(4, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
```

---

## 🔍 3. Foundational Business Queries (Level 1)

These queries tackle basic data retrieval, filtering, and row-level financial calculations.

**Q1: Data Cleaning & Filtering**  
*Business Question: Who are our active adult customers?*
```sql
SELECT 
    CustomerID, 
    FullName, 
    Age, 
    City
FROM Customers
WHERE Age >= 18 
  AND Churn = 0;
```

**Q2: Financial Calculation**  
*Business Question: What is the Realized Revenue and Gross Profit for Order #1005?*
```sql
SELECT 
    OrderID,
    (Price * Quantity * (1 - Discount)) AS RealizedRevenue,
    ((Price * Quantity * (1 - Discount)) - (Cost * Quantity)) AS GrossProfit
FROM Transactions
WHERE OrderID = 1005;
```

---

## 📊 4. Aggregation & Grouping (Level 2)

Here we move from row-level detail to high-level business summaries.

**Q3: Category Performance**  
*Business Question: What is the total revenue, profit, and order volume for each product category?*
```sql
SELECT 
    p.Category,
    SUM(t.Price * t.Quantity * (1 - t.Discount)) AS TotalRevenue,
    SUM((t.Price * t.Quantity * (1 - t.Discount)) - (t.Cost * t.Quantity)) AS TotalProfit,
    COUNT(t.OrderID) AS TotalOrders
FROM Transactions t
JOIN Products p ON t.ProductID = p.ProductID
GROUP BY p.Category;
```

**Q4: Churn Analysis**  
*Business Question: How many customers have churned versus stayed active?*
```sql
SELECT 
    CASE 
        WHEN Churn = 1 THEN 'Churned'
        ELSE 'Active' 
    END AS CustomerStatus,
    COUNT(CustomerID) AS TotalCustomers
FROM Customers
GROUP BY Churn;
```

**Q5: Filtering Groups**  
*Business Question: Which cities are generating more than $50,000 in total revenue?*
```sql
SELECT 
    c.City,
    SUM(t.Price * t.Quantity * (1 - t.Discount)) AS TotalRevenue
FROM Transactions t
JOIN Customers c ON t.CustomerID = c.CustomerID
GROUP BY c.City
HAVING SUM(t.Price * t.Quantity * (1 - t.Discount)) > 50000;
```

---

## 🔗 5. JOINs & Relational Analysis (Level 3)

Combining dimension and fact tables to find relationships across different data domains.

**Q6: Customer Spending**  
*Business Question: Who are our top 10 most valuable customers based on total revenue?*
```sql
SELECT 
    c.CustomerID,
    c.FullName,
    SUM(t.Price * t.Quantity * (1 - t.Discount)) AS TotalSpend
FROM Customers c
JOIN Transactions t ON c.CustomerID = t.CustomerID
GROUP BY c.CustomerID, c.FullName
ORDER BY TotalSpend DESC
LIMIT 10;
```

**Q7: Category by City Matrix**  
*Business Question: Which product category generates the most profit in each city?*
```sql
SELECT 
    c.City,
    p.Category,
    SUM((t.Price * t.Quantity * (1 - t.Discount)) - (t.Cost * t.Quantity)) AS TotalProfit
FROM Transactions t
JOIN Customers c ON t.CustomerID = c.CustomerID
JOIN Products p ON t.ProductID = p.ProductID
GROUP BY c.City, p.Category
ORDER BY c.City ASC, TotalProfit DESC;
```

---

## 🚀 6. Advanced Analytics: CTEs & Window Functions (Level 4)

These advanced techniques allow for multi-step logic and time-series analysis without messy subqueries.

**Q8: CTE (Common Table Expression)**  
*Business Question: What is the average age of our "High-Value Customers" (those who have spent over $5,000)?*
```sql
WITH HighValueCustomers AS (
    SELECT 
        c.CustomerID, 
        c.Age,
        SUM(t.Price * t.Quantity * (1 - t.Discount)) AS TotalSpend
    FROM Customers c
    JOIN Transactions t ON c.CustomerID = t.CustomerID
    GROUP BY c.CustomerID, c.Age
    HAVING SUM(t.Price * t.Quantity * (1 - t.Discount)) > 5000
)
SELECT 
    ROUND(AVG(Age), 1) AS AvgHighValueCustomerAge
FROM HighValueCustomers;
```

**Q9: Window Function**  
*Business Question: What is the Month-Over-Month (MoM) Revenue Growth?*
```sql
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', OrderDate) AS OrderMonth,
        SUM(Price * Quantity * (1 - Discount)) AS Revenue
    FROM Transactions
    GROUP BY DATE_TRUNC('month', OrderDate)
)
SELECT 
    OrderMonth,
    Revenue,
    LAG(Revenue, 1) OVER (ORDER BY OrderMonth) AS PrevMonthRevenue,
    ROUND(((Revenue - LAG(Revenue, 1) OVER (ORDER BY OrderMonth)) / 
            LAG(Revenue, 1) OVER (ORDER BY OrderMonth)) * 100, 2) AS MoMGrowthPercent
FROM MonthlyRevenue;
```

---

## 👨‍🏫 7. Instructor Delivery & Workshop Timing

| Session Segment | Duration | Topic & Student Milestone |
|-----------------|:--------:|---------------------------|
| **Part 1: SQL Fundamentals** | 60 min | Database architecture, basic `SELECT`, `WHERE`, `ORDER BY`, and mathematical operations. |
| **Part 2: Aggregations & JOINs** | 60 min | Moving from row-level to summary-level using `GROUP BY`, `HAVING`, and `INNER/LEFT JOIN`s. |
| **Break** | 30 min | Rest & Q&A. |
| **Part 3: Advanced SQL & Workshop** | 150 min | Introduction to `CTE`s and Window Functions. Students complete the TechNova business queries independently. |

---

## 💡 8. Golden Rules for Students

- ❌ **Avoid `SELECT *` in Production:** Always explicitly state the columns you need. It reduces memory usage, improves query speed, and prevents application crashes if schema changes occur.
- 📐 **Format and Indent Your Code:** SQL doesn't care about whitespace, but humans do. Capitalize clauses (`SELECT`, `FROM`, `WHERE`) and indent columns/conditions for readability.
- 🧠 **Remember the Order of Execution:** SQL processes commands differently than they are written. The mental model is: `FROM` $\rightarrow$ `JOIN` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `SELECT` $\rightarrow$ `ORDER BY` $\rightarrow$ `LIMIT`.
- 🔍 **Test Joins Carefully:** Always check row counts before and after joining tables to ensure you haven't created a Cartesian product (accidental duplication of rows).
