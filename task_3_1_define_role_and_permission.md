# Commit 3.1: Task 3 – Subtask 3.1: Define roles & permissions

## 1. Goal of this commit

In this commit, you will create the **core RBAC system** that understands roles and permissions.  
RBAC stands for "Role-Based Access Control" – it is the system that decides "who can do what" in your app.  

By the end of this commit:

- You will have an `RBAC` class in `Development/rbac.py` that knows all roles and permissions.  
- The system will understand that Admin > Seller > Customer (role hierarchy).  
- You will have methods to check if a user has permission to do something.  


This commit creates the "permission brain" that later commits will use to protect pages and features.  

---

## 2. What you should already have before Commit 3.1

Before starting this commit, you should:

- Have finished **Task 2** and have a working database with `users` table that has a `role` column.  
- Have your project folder with `Development/`.  
- Understand the three roles (Admin, Seller, Customer) you documented in Task 1.  

You still do **not** need any Flask routes or UI pages; this commit is about creating the permission logic that will be used later.  

---

## 3. Overview of files you will work with

In this commit, you will work with these files:

- `Development/rbac.py` – 

```python

class RBAC:
    """Role-Based Access Control class"""
    
    # Define all possible roles (hierarchy: admin > seller > customer)
    ROLES = {
        'admin': 3,
        'seller': 2, 
        'customer': 1
    }
    
    # Define all permissions that exist in the system
    PERMISSIONS = {
        'manage_users': ['admin'],
        'manage_categories': ['admin'],
        'manage_products': ['admin', 'seller'],
        'view_orders': ['admin', 'seller', 'customer'],
        'update_order_status': ['admin', 'seller'],
        'view_products': ['admin', 'seller', 'customer'],
        'add_to_cart': ['customer'],
        'place_orders': ['customer']
    }