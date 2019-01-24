
// tag::nodes[]
// Create customers
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///customers.csv" AS row
CREATE (:Customer {companyName: row.CompanyName, customerID: row.CustomerID, fax: row.Fax, phone: row.Phone});

// Create products
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///products.csv" AS row
CREATE (:Product {productName: row.ProductName, productID: row.ProductID, unitPrice: toFloat(row.UnitPrice)});

// Create suppliers
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///suppliers.csv" AS row
CREATE (:Supplier {companyName: row.CompanyName, supplierID: row.SupplierID});

// Create employees
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///employees.csv" AS row
CREATE (:Employee {employeeID:row.EmployeeID,  firstName: row.FirstName, lastName: row.LastName, title: row.Title});

// Create categories
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///categories.csv" AS row
CREATE (:Category {categoryID: row.CategoryID, categoryName: row.CategoryName, description: row.Description});

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///orders.csv" AS row
MERGE (order:Order {orderID: row.OrderID}) ON CREATE SET order.shipName =  row.ShipName;
// end::nodes[]

// tag::indexes[]
CREATE INDEX ON :Product(productID);
CREATE INDEX ON :Product(productName);
CREATE INDEX ON :Category(categoryID);
CREATE INDEX ON :Employee(employeeID);
CREATE INDEX ON :Supplier(supplierID);
CREATE INDEX ON :Customer(customerID);
CREATE INDEX ON :Customer(customerName);
// end::indexes[]


// tag::constraints[]
CREATE CONSTRAINT ON (o:Order) ASSERT o.orderID IS UNIQUE;
// end::constraints[]


//schema await

// tag::rels_orders[]   构建关系
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///orders.csv" AS row
MATCH (order:Order {orderID: row.OrderID})
MATCH (product:Product {productID: row.ProductID})
MERGE (order)-[pu:PRODUCT]->(product)
ON CREATE SET pu.unitPrice = toFloat(row.UnitPrice), pu.quantity = toFloat(row.Quantity);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///orders.csv" AS row
MATCH (order:Order {orderID: row.OrderID})
MATCH (employee:Employee {employeeID: row.EmployeeID})
MERGE (employee)-[:SOLD]->(order);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///orders.csv" AS row
MATCH (order:Order {orderID: row.OrderID})
MATCH (customer:Customer {customerID: row.CustomerID})
MERGE (customer)-[:PURCHASED]->(order);
// end::rels_orders[]

// tag::rels_products[]
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///products.csv" AS row
MATCH (product:Product {productID: row.ProductID})
MATCH (supplier:Supplier {supplierID: row.SupplierID})
MERGE (supplier)-[:SUPPLIES]->(product);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///products.csv" AS row
MATCH (product:Product {productID: row.ProductID})
MATCH (category:Category {categoryID: row.CategoryID})
MERGE (product)-[:PART_OF]->(category);
// end::rels_products[]

// tag::rels_employees[]
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///employees.csv" AS row
MATCH (employee:Employee {employeeID: row.EmployeeID})
MATCH (manager:Employee {employeeID: row.ReportsTo})
MERGE (employee)-[:REPORTS_TO]->(manager);
// end::rels_employees[]


