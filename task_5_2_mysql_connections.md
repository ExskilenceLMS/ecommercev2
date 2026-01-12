# Task 5 – Subtask 5.2: MySQL Connection & Config

## 1. Goal of this task

In this task, you will add **MySQL database connection** to your Flask app so it can read/write data from the database you designed in Task 2.  
The app will now be able to connect to your `ecommerce_db` and execute SQL queries.

By the end of this task you will have:
- MySQL configuration added to `Development/app.py`
- Database connection helper function in `Development/utils.py` 
- Working database connection that your app can use
- Test route to verify database connectivity

This connects your Flask app to the actual database schema from Task 2.

---

## 2. What you should already have before this task

Before starting this subtask, you should:
- Have completed **Task 5.1** with working Flask app structure (`app.py`, models, utils)
- Have MySQL running locally with `ecommerce_db` created from Task 2 schema
- Have your `Development/database/schema.sql` and `seed_data.sql` files from Task 2 ready
- Have basic Flask app running on `localhost:5001`

---

## 3. Files you will work with

- `Development/app.py` – Add MySQL configuration section
- `Development/utils.py` – Add database connection helper functions
