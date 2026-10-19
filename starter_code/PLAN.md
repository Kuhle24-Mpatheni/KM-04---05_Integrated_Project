# Thabo's Corner Store — Project Plan

## 1. Project Objective

Develop a Python sales-management system that cleans product and sales data, stores the data in a relational SQLite database, analyses sales performance, generates charts and protects access to reports with password verification.

## 2. Decomposition

I will divide the project into the following smaller tasks:

1. Inspect the product and sales CSV files and identify data-quality problems.
2. Clean missing, duplicated, inconsistent and invalid records, documenting each decision.
3. Create a relational SQLite database with appropriate tables and relationships.
4. Write and test five SQL queries, including a JOIN and an aggregation.
5. Analyse sales data using plain Python.
6. Generate a bar chart and a monthly sales line chart.
7. Implement SHA-256 password verification and reflect on the CIA triad.
8. Document setup instructions, cleaning decisions, query results, charts and business insights in README.md.
9. Test the complete application, record meaningful Git commits and prepare the submission ZIP.

## 3. Expected Data Problems

I will inspect the CSV files for missing values, duplicate records, inconsistent category names, invalid product IDs, incorrect data types and inconsistent date formats. I will verify which problems actually exist before deciding how to handle them. I will document each cleaning decision and its reason.

## 4. Computational Thinking

- **Decomposition:** Break the project into manageable tasks.
- **Pattern recognition:** Identify repeated data-quality issues and patterns in sales.
- **Abstraction:** Focus on relevant information, such as products, quantities, dates and sales totals, to answer business questions.
- **Algorithm design:** Define a repeatable sequence for cleaning data, creating database tables, querying records, analysing results, generating charts and verifying access.

## 5. Development Order

I will follow the sequence in the project brief, completing and testing each stage before moving on. I will use Git commits to document meaningful progress and changes.

## 6. Testing and Evidence

I will verify that the cleaned data is consistent, database relationships work correctly, all five SQL queries return sensible results, Python calculations are accurate, charts are generated successfully and password verification behaves as expected. I will record cleaning decisions, results, chart descriptions, security reflections and business insights in README.md.

## 7. Final Deliverables

The final submission will include the Python source files, PLAN.md, README.md, generated charts, the SQLite database, SUBMISSION.txt and the required project ZIP.