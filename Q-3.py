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
    "Base Query": '''SELECT 
    pc.Name AS CategoryName,
    YEAR(soh.OrderDate) AS Year,
    MONTH(soh.OrderDate) AS Month,
    SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS TotalSales
FROM 
    Production.Product p
JOIN 
    Sales.SalesOrderDetail sod ON p.ProductID = sod.ProductID
JOIN 
    Sales.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
JOIN 
    Production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
JOIN 
    Production.ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
GROUP BY 
    pc.Name, YEAR(soh.OrderDate), MONTH(soh.OrderDate)
ORDER BY 
    pc.Name, Year, Month;



''',
"Optimized query": '''-- Step 1: Calculate and store monthly sales in a temporary table
SELECT 
    pc.ProductCategoryID,
    YEAR(soh.OrderDate) AS Year,
    MONTH(soh.OrderDate) AS Month,
    SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS TotalSales
INTO 
    #MonthlySales
FROM 
    Production.Product p
JOIN 
    Sales.SalesOrderDetail sod ON p.ProductID = sod.ProductID
JOIN 
    Sales.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
JOIN 
    Production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
JOIN 
    Production.ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
GROUP BY 
    pc.ProductCategoryID, YEAR(soh.OrderDate), MONTH(soh.OrderDate);

-- Step 2: Calculate month-over-month growth rate using the temporary table
SELECT 
    pc.Name AS CategoryName,
    ms.Year,
    ms.Month,
    ms.TotalSales,
    LAG(ms.TotalSales) OVER (PARTITION BY ms.ProductCategoryID ORDER BY ms.Year, ms.Month) AS PreviousMonthSales,
    (ms.TotalSales - LAG(ms.TotalSales) OVER (PARTITION BY ms.ProductCategoryID ORDER BY ms.Year, ms.Month)) / NULLIF(LAG(ms.TotalSales) OVER (PARTITION BY ms.ProductCategoryID ORDER BY ms.Year, ms.Month), 0) AS GrowthRate
FROM 
    #MonthlySales ms
JOIN 
    Production.ProductCategory pc ON ms.ProductCategoryID = pc.ProductCategoryID
ORDER BY 
    CategoryName, Year, Month;

-- Cleanup temporary table
DROP TABLE #MonthlySales;


'''
}

# Record execution times
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
