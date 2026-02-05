# Task 8 – Subtask 8.1: Admin Routes

## 1. Overview

This subtask introduces the **Admin Dashboard route**, which serves as the entry point for all administrator-level functionality within the system.  
It establishes a dedicated route and view accessible only to users with the **Admin role**.

This subtask focuses strictly on **routing, access control, and dashboard rendering**, while detailed admin operations are implemented in later subtasks.

---

## 2. Purpose

The purpose of this subtask is to:

- Create a centralized dashboard for administrators
- Enforce admin-only access to sensitive routes
- Provide a foundation for future admin features
- Maintain clear separation between user roles

---

## 3. Prerequisites

Before completing this subtask, the following should already be in place:

- User authentication using Flask-Login
- Role-based access control for Admin users
- Base layout template for consistent UI rendering
- Admin blueprint structure initialized

---

## 4. Admin Dashboard Route

- **URL Path:** `/admin/dashboard`
- **Blueprint:** `admin`
- **HTTP Method:** `GET`
- **Access Level:** Admin only

This route acts as the **primary landing page** for all administrative actions.

---

## 5. Access Control

- The dashboard route is protected using an **admin-only access mechanism**
- Unauthorized or unauthenticated users are prevented from accessing the page
- Role validation occurs before rendering the dashboard

This ensures that administrative functionality remains secure and isolated.

---

## 6. Implementation Summary

- Admin routes are organized under a dedicated blueprint
- The dashboard view extends the shared base layout
- Static placeholders are used where dynamic data will be added later
- Code sections related to this subtask are clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Admin dashboard route
- Admin-only access enforcement
- Dashboard template rendering

**Not included in this subtask:**
- Seller management
- Category management
- Order overview
- Analytics or reporting logic

These features are implemented in subsequent Task 8 subtasks.

---

## 8. Outcome

After completing this subtask:

- Administrators have a secure entry point into the system
- Role-based access control is actively enforced
- The application structure supports scalable admin features
- The groundwork is laid for advanced administrative operations

---

## 9. Related Tasks

- Task 7 – Role-Based Access Control
- Task 8.2 – Seller Management
- Task 8.3 – Category Management
- Task 8.4 – Order Overview

---
