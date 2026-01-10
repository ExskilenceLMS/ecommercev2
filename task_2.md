# Task 2: Database Design

## 1. Goal of this commit

In this commit, you will design and create the **database** for your e‑commerce application using MySQL.  
You will think about which real-world things you need to store (like users, products, orders) and then convert that thinking into actual tables and columns in a SQL file.  

By the end of this commit:

- You will have a complete database schema for the project in `Development/database/schema.sql`.  
- You will have a seed data file to insert sample data into the database: `Development/database/seed_data.sql`.  
- You will have a test validation script: `Development/database/test_database_validation.sql`.  
- You will have tests ready to check your database: `Testing/tests/test_database_schema.py` and `Testing/test_configs/task_02.json`.  

This commit turns your ideas from Task 1 (roles and features) into a **real database structure** that your Flask code will use later.  

---

## 2. What you should already have before Task 2

Before starting this commit, you should:

- Have finished **Task 1** and clearly documented Admin, Seller, and Customer roles and their features.  
- Have your project folder set up similar to the structure shown in `README.md` (at least the `Development/` and `Testing/` folders created).  
- Have MySQL installed and running on your machine (you will need it soon, even if you only write SQL files in this step).  

You still do **not** need Flask routes or templates to be complete; this commit focuses only on the database.  

---

## 3. Overview of files you will work with

In this commit, you will work mainly inside the `Development/database/` and `Testing/` folders.  

You will create or update these files:

- `Development/database/schema.sql` – contains all `CREATE TABLE` statements for your e‑commerce database.  
- `Development/database/seed_data.sql` – contains `INSERT` statements to add example users, products, categories, etc.  
- `Development/database/test_database_validation.sql` – optional SQL script to help validate schema/test data.  
- `Testing/tests/test_database_schema.py` – Python tests that check if your database schema is correct.  
- `Testing/test_configs/task_02.json` – configuration file for tests of Task 2.  

Make sure the `Development/database/` folder exists; if not, create it and then add these files inside it.  

---

## 4. Step-by-step instructions

### 4.1 List the entities (tables) you need

First, think again about the features and roles you described in Task 1 and the tasks listed in the main README.  

Write down the main **entities** (tables) you need, for example:

- `users` – stores admin, seller, and customer details.  
- `products` – stores product information (name, price, description, stock, etc.).  
- `categories` – stores categories to group products.  
- `orders` – stores each order placed by a customer.  
- `order_items` – stores which products are included in each order.  
- `payments` – stores payment information related to orders.  
- You may also need tables like `addresses`, `roles`, or `user_roles`, depending on your design.  

You can write this list in a planning section at the top of `schema.sql` as comments so students can see the thought process:

```sql
-- Entities:
-- users, roles, products, categories, orders, order_items, payments, addresses, etc.
