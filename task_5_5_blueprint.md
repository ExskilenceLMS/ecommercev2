# Task 5 – Subtask 5.5: Blueprint Structure

## 1. Goal of this task

In this task, you will create the **Flask Blueprint system** that organizes your app into modular components.  
Instead of putting all routes in `app.py`, you'll create separate blueprint files for auth, admin, seller, customer, etc.

By the end of this task you will have:
- `Development/blueprints/` folder with `__init__.py` and blueprint registration
- Blueprint structure ready for all modules (auth, admin, seller, customer, product, cart, etc.)
- Routes properly organized by feature/module
- Centralized blueprint registration in `app.py`

This completes **Task 5** and makes your app scalable for all 15 tasks.

---

## 2. What you should already have before this task

Before starting this subtask, you should:
- Have completed **Task 5.1-5.4** with working Flask app, database, environment, base template
- Have Flask app running successfully with proper layout
- Understand MVC structure from Task 5.1
- Have all UI templates from Task 4 ready to connect to blueprints

---