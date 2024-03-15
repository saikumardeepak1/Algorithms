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

# Define
# queries from worst to best case scenario
queries = {
    "Base Query": '''SELECT 
    p.ProductID,
    p.Name AS ProductName,
    SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS TotalSales
FROM 
    Production.Product p
JOIN 
    Sales.SalesOrderDetail sod ON p.ProductID = sod.ProductID
GROUP BY 
    p.ProductID, p.Name
ORDER BY 
    TotalSales DESC;

''',
"Optimized query": '''SELECT 
    i.name AS IndexName,
    OBJECT_NAME(i.object_id) AS TableName,
    COL_NAME(ic.object_id, ic.column_id) AS ColumnName
FROM 
    sys.indexes i
INNER JOIN 
    sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
WHERE 
    i.name IN ('idx_SalesOrderDetail_ProductID', 'idx_Production_Product_ProductID');
'''
}

# Recordingg execution times
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
plt.ylabel('Execution Time ()')
plt.title('Query Execution Time Analysis')
plt.xticks(rotation=0)
plt.show()

# Clean up
cursor.close()
conn.close()
