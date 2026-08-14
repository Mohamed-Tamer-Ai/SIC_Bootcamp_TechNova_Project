-- ====================================================================
-- TECHNOVA RETAIL & CUSTOMER CHURN — SQL ANALYSIS
-- SIC Bootcamp | Day 3: SQL for Data Analysis
-- ====================================================================
--
-- OVERVIEW:
-- This file contains 7 SQL queries that demonstrate progressively
-- advanced SQL concepts, all applied to the TechNova e-commerce database.
--
-- The database schema consists of 4 related tables:
--   • Customers   (Dimension) — CustomerID, FullName, Age, City, JoinDate, Churn
--   • Products    (Dimension) — ProductID, ProductName, Category, Price, Cost
--   • Orders      (Fact)      — OrderID, CustomerID, OrderDate, ShipMode
--   • OrderDetails(Fact)      — OrderDetailID, OrderID, ProductID, Quantity, Discount
--
-- TOPICS COVERED:
--   Q1: SELECT + WHERE          (Basic Filtering)
--   Q2: GROUP BY + Aggregation  (SUM, AVG, COUNT)
--   Q3: Multi-Table JOINs       (INNER JOIN across 4 tables)
--   Q4: LEFT JOIN + Subquery    (Finding records with NO match)
--   Q5: Common Table Expressions (CTEs)
--   Q6: Window Functions        (RANK, PARTITION BY)
--   Q7: Advanced CTE + CASE     (Segmentation)
-- ====================================================================


-- ====================================================================
-- Q1: BASIC FILTERING (SELECT + WHERE)
-- ====================================================================
-- BUSINESS QUESTION:
--   "Which customers have already churned in Cairo?"
--
-- WHY THIS MATTERS:
--   The marketing team wants to prioritize a retention campaign
--   specifically targeting churned customers in our highest-value city.
--
-- SQL CONCEPTS:
--   • SELECT: Choose which columns to display
--   • FROM:   Specify the table to query
--   • WHERE:  Filter rows based on conditions (AND combines two filters)
-- ====================================================================

SELECT 
    CustomerID,
    FullName, 
    Age, 
    City 
FROM Customers 
WHERE Churn = 1 
  AND City = 'Cairo'
ORDER BY 
    Age DESC;


-- ====================================================================
-- Q2: AGGREGATION (GROUP BY + Aggregate Functions)
-- ====================================================================
-- BUSINESS QUESTION:
--   "What is the total revenue and average discount for each product category?"
--
-- WHY THIS MATTERS:
--   Understanding which categories generate the most revenue — and
--   whether heavy discounting is eroding those margins.
--
-- SQL CONCEPTS:
--   • JOIN:      Combine Products and OrderDetails on ProductID
--   • SUM():     Calculate total revenue per group
--   • AVG():     Calculate average discount per group
--   • COALESCE:  Replace NULL values with a default (NULL discount → 0)
--   • GROUP BY:  Group rows by Category before aggregating
--   • ORDER BY:  Sort results (DESC = highest first)
-- ====================================================================

SELECT 
    p.Category, 
    COUNT(*)                                                          AS TotalOrders,
    SUM(od.Quantity * p.Price * (1 - COALESCE(od.Discount, 0)))       AS TotalRevenue, 
    ROUND(AVG(COALESCE(od.Discount, 0)) * 100, 2)                    AS AvgDiscountPct
FROM Products AS p
INNER JOIN OrderDetails AS od 
    ON p.ProductID = od.ProductID
GROUP BY 
    p.Category
ORDER BY 
    TotalRevenue DESC;


-- ====================================================================
-- Q3: MULTI-TABLE JOINS (INNER JOIN across 4 tables)
-- ====================================================================
-- BUSINESS QUESTION:
--   "Who are the top 5 most profitable customers?"
--
-- WHY THIS MATTERS:
--   Identifying our VIP customers helps the sales team allocate
--   resources and loyalty rewards appropriately.
--
-- SQL CONCEPTS:
--   • Multiple INNER JOINs: Chain 4 tables together via Foreign Keys
--     Customers → Orders → OrderDetails → Products
--   • SUM():     Aggregate profit across all orders for each customer
--   • COALESCE:  Handle NULL Cost values (fallback: 50% of Price)
--   • LIMIT:     Restrict output to top N rows
-- ====================================================================

SELECT 
    c.CustomerID,
    c.FullName,
    c.City,
    SUM(
        (p.Price - COALESCE(p.Cost, p.Price * 0.5)) * od.Quantity
    )                                                                 AS TotalProfit
FROM Customers AS c
INNER JOIN Orders AS o 
    ON c.CustomerID = o.CustomerID
INNER JOIN OrderDetails AS od 
    ON o.OrderID = od.OrderID
INNER JOIN Products AS p 
    ON od.ProductID = p.ProductID
GROUP BY 
    c.CustomerID, 
    c.FullName,
    c.City
ORDER BY 
    TotalProfit DESC 
LIMIT 5;


-- ====================================================================
-- Q4: LEFT JOIN + IS NULL (Finding "Ghost" Customers)
-- ====================================================================
-- BUSINESS QUESTION:
--   "Which customers signed up but never placed a single order?"
--
-- WHY THIS MATTERS:
--   These "ghost" users represent lost potential. The marketing team
--   can target them with onboarding emails or first-purchase discounts.
--
-- SQL CONCEPTS:
--   • LEFT JOIN: Returns ALL rows from the left table (Customers),
--     even if there's no matching row in the right table (Orders).
--   • IS NULL:   Filters for customers where no matching order exists.
--   • This is a classic pattern for "find records with NO match."
-- ====================================================================

SELECT 
    c.CustomerID,
    c.FullName, 
    c.City,
    c.Age
FROM Customers AS c
LEFT JOIN Orders AS o 
    ON c.CustomerID = o.CustomerID
WHERE o.OrderID IS NULL
ORDER BY 
    c.City, 
    c.FullName;


-- ====================================================================
-- Q5: COMMON TABLE EXPRESSIONS (CTEs)
-- ====================================================================
-- BUSINESS QUESTION:
--   "Which customers spent more than the global average?"
--
-- WHY THIS MATTERS:
--   Identifying above-average spenders helps classify VIP customers
--   for exclusive loyalty programs and premium support.
--
-- SQL CONCEPTS:
--   • WITH ... AS (): Defines a CTE — a temporary named result set
--     that makes complex queries readable and reusable.
--   • Subquery in WHERE: (SELECT AVG(Spend) FROM CustomerSpend)
--     compares each customer's spend against the global average.
--   • Why CTE over Subquery? CTEs are more readable, can be referenced
--     multiple times, and are easier to debug.
-- ====================================================================

WITH CustomerSpend AS (
    SELECT 
        o.CustomerID, 
        SUM(
            p.Price * od.Quantity * (1 - COALESCE(od.Discount, 0))
        )                                                             AS Spend
    FROM Orders AS o 
    INNER JOIN OrderDetails AS od 
        ON o.OrderID = od.OrderID 
    INNER JOIN Products AS p 
        ON od.ProductID = p.ProductID
    GROUP BY 
        o.CustomerID
)
SELECT 
    c.CustomerID,
    c.FullName, 
    ROUND(cs.Spend, 2)                                                AS TotalSpend,
    ROUND(
        (SELECT AVG(Spend) FROM CustomerSpend), 2
    )                                                                 AS GlobalAvgSpend
FROM Customers AS c 
INNER JOIN CustomerSpend AS cs 
    ON c.CustomerID = cs.CustomerID
WHERE cs.Spend > (SELECT AVG(Spend) FROM CustomerSpend)
ORDER BY 
    cs.Spend DESC;


-- ====================================================================
-- Q6: WINDOW FUNCTIONS (RANK + PARTITION BY)
-- ====================================================================
-- BUSINESS QUESTION:
--   "Rank customers by spending within each city."
--
-- WHY THIS MATTERS:
--   Regional managers need to know who their top spenders are
--   within their specific city/territory, not globally.
--
-- SQL CONCEPTS:
--   • Window Function: Performs a calculation ACROSS a set of rows
--     that are related to the current row — WITHOUT collapsing them.
--   • RANK(): Assigns a rank number (1, 2, 3...) within each partition.
--     Ties receive the same rank; next rank skips (1, 1, 3, ...).
--   • PARTITION BY: Divides rows into groups (by City). The RANK()
--     function restarts at 1 for each new city.
--   • ORDER BY inside OVER(): Determines the ranking order.
-- ====================================================================

WITH CustomerSpend AS (
    SELECT 
        c.City, 
        c.CustomerID,
        c.FullName,
        SUM(
            p.Price * od.Quantity * (1 - COALESCE(od.Discount, 0))
        )                                                             AS TotalSpend
    FROM Customers AS c
    INNER JOIN Orders AS o 
        ON c.CustomerID = o.CustomerID
    INNER JOIN OrderDetails AS od 
        ON o.OrderID = od.OrderID
    INNER JOIN Products AS p 
        ON od.ProductID = p.ProductID
    GROUP BY 
        c.City, 
        c.CustomerID,
        c.FullName
)
SELECT 
    City, 
    CustomerID,
    FullName, 
    ROUND(TotalSpend, 2)                                              AS TotalSpend,
    RANK() OVER (PARTITION BY City ORDER BY TotalSpend DESC)          AS RankInCity
FROM CustomerSpend
ORDER BY 
    City, 
    RankInCity;


-- ====================================================================
-- Q7: ADVANCED CTE + CASE (Customer Segmentation)
-- ====================================================================
-- BUSINESS QUESTION:
--   "Segment customers into High / Medium / Low value tiers."
--
-- WHY THIS MATTERS:
--   Customer segmentation is fundamental to targeted marketing.
--   Different tiers receive different communication strategies.
--
-- SQL CONCEPTS:
--   • CASE WHEN ... THEN ... END: SQL's equivalent of IF/ELSE.
--     Creates a new column based on conditional logic.
--   • Combining CTE + CASE: First compute the spend, then classify.
-- ====================================================================

WITH CustomerSpend AS (
    SELECT 
        o.CustomerID, 
        SUM(
            p.Price * od.Quantity * (1 - COALESCE(od.Discount, 0))
        )                                                             AS Spend
    FROM Orders AS o 
    INNER JOIN OrderDetails AS od 
        ON o.OrderID = od.OrderID 
    INNER JOIN Products AS p 
        ON od.ProductID = p.ProductID
    GROUP BY 
        o.CustomerID
)
SELECT 
    c.CustomerID,
    c.FullName,
    c.City,
    ROUND(cs.Spend, 2)                                                AS TotalSpend,
    CASE 
        WHEN cs.Spend >= 10000 THEN '🟢 High Value'
        WHEN cs.Spend >= 5000  THEN '🟡 Medium Value'
        ELSE                        '🔴 Low Value'
    END                                                               AS CustomerTier
FROM Customers AS c
INNER JOIN CustomerSpend AS cs 
    ON c.CustomerID = cs.CustomerID
ORDER BY 
    cs.Spend DESC;
