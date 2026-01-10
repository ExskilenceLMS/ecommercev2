# Task 5 – Subtask 5.1: Flask Project Structure (MVC style)

## 1. Goal of this task

In this task, you will set up the **basic Flask project structure** using an MVC-style layout.  
Instead of writing all code in one file, you will organize your app into folders like `models`, `blueprints`, `templates`, and `static` so that future tasks stay clean and easy to maintain.

By the end of this task you will have:
- A working `Development/app.py` with Flask app initialization and a simple home route.  
- A proper `Development/models/` package with `__init__.py` and `user.py` created (even if user model is still basic in this subtask).
- A `Development/utils.py` file ready for common helper functions.
- A folder structure that matches the project layout described in the main README and commit history.

This prepares the foundation for later subtasks in Task 5 (database config, env setup, base template, blueprints).

---

## 2. What you should already have before this task

Before starting this subtask, you should:

- Have the **project root** created, similar to what is shown in `README.md` (with `Development/`  directory planned).
- Have completed Tasks 1–4 (requirements, DB design, RBAC planning, UI wireframes) so you know what the app will eventually do.
- Have a Python virtual environment and dependencies planned (to be fully used in later subtasks).

You do **not** need login, dashboards, or business logic working yet; this task is about **structure**, not full features.

---

## 3. Files and folders you will work with

In this subtask you will mainly touch the `Development/` folder:

You will create or update:

- `Development/app.py` – Flask application entry point (basic initialization and one test route).  
- `Development/models/__init__.py` – makes `models` a Python package.  
- `Development/models/user.py` – placeholder for the User model used later by auth tasks.  
- `Development/utils.py` – helper functions (for now, simple placeholders to be expanded later). 

Your folder structure after this subtask should start looking like the structure described under **Project Structure** in the README.md

