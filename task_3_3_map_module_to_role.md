# Task 3 – Subtask 3.3: RBAC intro - Map modules to roles

## 1. Goal of this task

In this task, you will create a **module mapping system** that connects your RBAC permissions to actual Flask blueprints and routes.  
This tells the system which pages and features belong to which roles (Admin, Seller, Customer).

By the end of this task you will have:
- `Development/module_mapping.py` with clear mappings of modules to roles
- Helper functions to check module access for any user role

This completes Task 3 by connecting your RBAC system (3.1) + decorators (3.2) to the actual Flask blueprint structure you'll build later.

---

## 2. What you should already have before this task

Before starting this subtask, you should:
- Have completed **Task 3.1** (RBAC class with roles/permissions)
- Have completed **Task 3.2** (decorators: @admin_required, etc.)
- Understand your Flask blueprint structure planned for Tasks 5-15

---

## 3. Files you will work with

- `Development/module_mapping.py` 