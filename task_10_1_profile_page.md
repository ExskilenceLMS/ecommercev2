# Task 10 – Subtask 10.1: Profile Page

## 1. Overview

This subtask introduces the **Customer Profile Page**, allowing customers to **view and update their personal information** within the application.  
It serves as the primary interface for customers to manage their account details.

This subtask marks the beginning of **customer-specific dashboard functionality**.

---

## 2. Purpose

The purpose of this subtask is to:

- Provide customers with access to their profile information
- Allow updates to personal account details
- Improve user experience through self-service account management
- Maintain separation between customer and admin/seller operations

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Customer dashboard route
- User authentication using Flask-Login
- Role-based access control for Customer users
- Customer blueprint structure
- Base layout template

---

## 4. Profile Management Features

This subtask includes the following customer capabilities:

- View personal profile information
- Access a profile update form
- Update allowed account details
- Ensure profile data is user-specific and secure

---

## 5. Access Control

- Profile routes are **restricted to authenticated Customer users**
- Customers can access **only their own profile**
- Unauthorized or unauthenticated users are prevented from accessing profile pages
- User identity validation occurs before rendering profile data

This ensures profile information remains private and secure.

---

## 6. Implementation Summary

- Profile routes are defined within the customer blueprint
- Profile view and update logic is encapsulated for clarity
- Templates extend the shared base layout for UI consistency
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Profile information display
- Profile update functionality
- Customer-only access enforcement

**Not included in this subtask:**
- Password change functionality
- Address management
- Profile image upload
- Account deletion

These features are implemented in separate tasks.

---

## 8. Outcome

After completing this subtask:

- Customers can manage their own profile information
- Account data remains secure and role-isolated
- User experience is improved through self-service access
- The system supports future customer-centric features

---

## 9. Related Tasks

- Task 9 – Seller Dashboard
- Task 10.2 – Order History
- Task 6 – Login & Session Management

---
