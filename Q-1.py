import pyodbc
import time
import matplotlib.pyplot as plt

# Set up the connection parameters
server = 'KATIES-PC'
database = 'AdventureWorks2008R2'

# Use Windows Authentication
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION=yes'
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Define queries from worst to best case scenario
queries = {
    "Base Query": '''WITH YearlySales AS (
    SELECT 
        soh.CustomerID,
        YEAR(soh.OrderDate) AS SaleYear,
        SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS TotalSales
    FROM 
        Sales.SalesOrderHeader soh
    JOIN 
        Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
    GROUP BY 
        soh.CustomerID, YEAR(soh.OrderDate)
),
YearOverYearGrowth AS (
    SELECT 
        ys1.CustomerID,
        ys1.SaleYear,
        ys1.TotalSales,
        ISNULL(((ys1.TotalSales / ys2.TotalSales) - 1) * 100, 0) AS GrowthPercentage
    FROM 
        YearlySales ys1
    LEFT JOIN 
        YearlySales ys2 ON ys1.CustomerID = ys2.CustomerID AND ys1.SaleYear = ys2.SaleYear + 1
)
SELECT 
    yoyg.CustomerID,
    yoyg.SaleYear,
    yoyg.GrowthPercentage
FROM 
    YearOverYearGrowth yoyg
ORDER BY 
    yoyg.SaleYear, yoyg.GrowthPercentage DESC;
''',
"Intermediate Optimization": '''WITH YearlySales AS (
    SELECT 
        soh.CustomerID,
        YEAR(soh.OrderDate) AS SaleYear,
        SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS TotalSales
    FROM 
        Sales.SalesOrderHeader soh
    JOIN 
        Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
    GROUP BY 
        soh.CustomerID, YEAR(soh.OrderDate)
),
YearOverYearGrowth AS (
    SELECT 
        CustomerID,
        SaleYear,
        TotalSales,
        LAG(TotalSales) OVER (PARTITION BY CustomerID ORDER BY SaleYear) AS PreviousYearSales,
        ISNULL(((TotalSales / LAG(TotalSales) OVER (PARTITION BY CustomerID ORDER BY SaleYear)) - 1) * 100, 0) AS GrowthPercentage
    FROM 
        YearlySales
)
SELECT 
    CustomerID,
    SaleYear,
    GrowthPercentage
FROM 
    YearOverYearGrowth
ORDER BY 
    SaleYear, GrowthPercentage DESC;
''',
    "Advanced": '''WITH YearlySales AS (
    SELECT 
        soh.CustomerID,
        YEAR(soh.OrderDate) AS SaleYear,
        SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS TotalSales
    FROM 
        Sales.SalesOrderHeader sohv 
    JOIN 
        Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
    GROUP BY 
        soh.CustomerID, YEAR(soh.OrderDate)
),
YearOverYearGrowth AS (
    SELECT 
        CustomerID,
        SaleYear,
        TotalSales,
        LAG(TotalSales) OVER (PARTITION BY CustomerID ORDER BY SaleYear) AS PreviousYearSales,
        ISNULL(((TotalSales / LAG(TotalSales) OVER (PARTITION BY CustomerID ORDER BY SaleYear)) - 1) * 100, 0) AS GrowthPercentage
    FROM 
        YearlySales
)
SELECT 
    CustomerID,
    SaleYear,
    GrowthPercentage
FROM 
    YearOverYearGrowth
ORDER BY 
    SaleYear, GrowthPercentage DESC;'''
}

# Recording execution times
execution_times = {}

for name, query in queries.items():
    start_time = time.time()
    cursor.execute(query)
    results = cursor.fetchall()
    execution_time = time.time() - start_time
    execution_times[name] = execution_time

# Plotting
plt.bar(execution_times.keys(), execution_times.values(), color=['red', 'yellow', 'green'])
plt.xlabel('Optimization Level')
plt.ylabel('Execution Time (seconds)')
plt.title('Query Execution Time Analysis')
plt.xticks(rotation=0)
plt.show()

# Clean up
cursor.close()
conn.close()
