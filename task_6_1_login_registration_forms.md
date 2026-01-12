# Task 6 – Subtask 6.1: Login Registration Forms Jinja

## 1. Goal of this task

In this task, you will implement **login and registration form handling** in the auth blueprint using Jinja2 templates.  
The routes will render the UI templates created in Task 4.1 and handle basic GET/POST form submissions.

By the end of this task you will have:
- `Development/blueprints/auth.py` with working login/register routes
- Proper form rendering using Task 4.1 templates (`login.html`, `register.html`)
- Basic form validation structure ready for real authentication (Task 6.2+)
- Blueprint routes connected to your professional UI design

This connects your Task 4 UI wireframes to the Flask blueprint system from Task 5.5.

---

## 2. What you should already have before this task

Before starting this subtask, you should:
- Have completed **Task 5.5** with blueprint structure (`task_5_5_blueprint_structure` branch)
- Have Task 4.1 UI templates (`login.html`, `register.html`) from UI wireframes
- Have Flask app running with `base.html` layout from Task 5.4
- Understand blueprint route structure from Task 5.5 placeholders

---

## 3. Files you will work with

**Main files:**
- `Development/blueprints/auth.py` – Login/register routes with form handling
