# Task 3 – Subtask 3.2: Restrict seller/admin/customer actions

## 1. Goal of this task

In this task, you will create **role-based decorators** that use your RBAC logic to protect Flask routes.
A decorator will check the logged‑in user’s role before allowing access to a view function (route).  

By the end of this task:

- You will have decorators: `@admin_required`, `@seller_required`, `@customer_required`, and `@permission_required`.
- Unauthorized users will be redirected or blocked instead of seeing pages they should not access.  

This makes your authorization design from Task 3 truly usable inside the Flask app, supporting the “Role-Based Access Control” part mentioned in the main README (`Development/rbac.py`)

---

## 2. What you should already have before this task

Before starting this subtask, you should:

- Have completed **Task 3.1**, where you created the `RBAC` class with roles and permissions in `Development/rbac.py`.
- Have basic Flask project structure ready as described in the main README (an `app.py` file and login system planned for later tasks).[README.md]  
- Have `flask_login` integrated or at least planned, so you can use `current_user` to know which user is logged in (this is part of later “Login & Session Management” work, but the decorators are prepared now).[README.md]  

You do **not** need all blueprints or dashboards yet; you are only building the decorators that will be used by those blueprints later (Tasks 7, 8, 9, 10).[README.md]

---

## 3. Files you will work with in this task

You will focus on these files:

- `Development/rbac.py`  
  - Add a new section for **Subtask 3.2** that defines decorators.  

