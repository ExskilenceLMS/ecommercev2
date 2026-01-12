# Task 6 – Subtask 6.2: Password Hashing

## 1. Goal of this task

In this task, you will implement **secure password hashing** using Werkzeug security utilities.  
Users' passwords will now be stored securely as hashed values instead of plaintext.

By the end of this task you will have:
- Password hashing methods in `Development/models/user.py`
- `generate_password_hash()` and `check_password_hash()` functions
- Updated registration route to hash passwords before "saving"
- Test coverage for password security functions

This adds security layer to your authentication system from Task 6.1.

---

## 2. What you should already have before this task

Before starting this subtask, you should:
- Have completed **Task 6.1** (`task_6_1_login_registration_forms` branch)
- Have working login/register form routes rendering UI templates
- Have `Development/blueprints/auth.py` with basic form handling
- Have Flask app running with form submission working (flash messages)

---

## 3. Files you will work with

**Main files:**
- `Development/models/user.py` – Add password hashing methods
- `Development/blueprints/auth.py` – Update register route to use hashing

**Test files:**
